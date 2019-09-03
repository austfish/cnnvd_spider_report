
"""
爬取CNNVD漏洞库
author: conan
date: 20181220
todo:
字段值是否有不合常规的：受影响实体以及补丁
issue:
1, cnnvd网站的漏洞的受影响实体和补丁字段的"更多"按钮存在bug,初始返回为5项,第二次为55项,第三次为105项,也就是说参数为+5,但实际上为+50,而且后面的点击返回结果将包含前面的结果,导致页面重复
重复出现:http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201105-261
越来越少:http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201106-147
解决办法:一直点更多按钮,直到弹出没有更多了,然后统计最后一次返回的数据.但仍有随机返回的问题;更新:该api返回有问题,无法解决
"""

import datetime
import json
import logging
import re
import time
import requests

from pyquery import PyQuery as pq

from libs.elastic import ES
from libs.datetime import get_date, get_datetime


LOG = logging.getLogger(__file__)


# cnnvd漏洞爬取
def spider_cnnvd(cnnvd_es_time):
    cnnvd_url = 'http://www.cnnvd.org.cn/web/vulnerability/querylist.tag'
    cnnvd_host = 'http://www.cnnvd.org.cn'
    cnnvd_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'cnnvd.org.cn',
        'Referer': 'http://cnnvd.org.cn/web/vulnerability/querylist.tag',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }

    crawler_session = requests.session()

    # 计数
    spider_count = 0
    total_count = 0
    vuln_list = []

    # 爬虫主循环
    while True:
        try:
            crawler_res = crawler_session.get(cnnvd_url, headers=cnnvd_headers, timeout=5)

            # 解析返回的页面
            cnnvd_list_doc = pq(crawler_res.text)
            # 列表中的漏洞链接
            page_flag = False
            cnnvd_list = cnnvd_list_doc('.list_list')('li')
            for li_item in cnnvd_list.items():
                cnnvd_time = li_item('div').eq(1).text()
                cnnvd_time = datetime.datetime.strptime(cnnvd_time, '%Y-%m-%d')
                cnnvd_time = time.mktime(cnnvd_time.timetuple())

                if cnnvd_time >= cnnvd_es_time:
                    row = li_item('div').eq(0)('p a')
                    vuln_info = dict()

                    # 获取漏洞链接并爬取子页面
                    vuln_url = cnnvd_host + row.attr('href')

                    vuln_info.update(analysis_vul(vuln_url, cnnvd_host, cnnvd_headers, crawler_session))
                    vuln_info['cnnvd_id'] = row.text()

                    spider_count += 1
                    LOG.info('[CNNVD爬取数量]-[%d]', spider_count)
                    page_flag = True

                    # # 关键字匹配
                    # if not re.search('|'.join(TAGS), json.dumps(vuln_info)):
                    #     continue

                    total_count += 1
                    vuln_list.append(vuln_info)
                    LOG.info('[关键字过滤后CNNVD漏洞总量]-[%d]', total_count)

            if page_flag:
                # 爬取下一页
                next_page = cnnvd_list_doc('.page')('a').eq(-2)

                if next_page.text() == '下一页':
                    next_page_url = next_page.attr('onclick')[9:-2]
                    cnnvd_url = cnnvd_host + next_page_url
                else:
                    break
            else:
                break
        except Exception as error:
            LOG.error('[CNNVD漏洞数据爬取异常]-[%s]', error)
            LOG.info('[CNNVD]-[sleeping now....]')
            time.sleep(120)

    LOG.info('[CNNVD漏洞数据爬取完成]')
    return {
        'status': 'yes',
        'data': {
            'spider': spider_count,
            'total': total_count,
            'cnnvd': vuln_list
        }
    }


def analysis_vul(vul_url, cnnvd_host, cnnvd_headers, crawler_session):
    vul = {
        'cnnvd_id': '',
        'name': '',
        'severity': '',
        'cve_id': '',
        'type': '',
        'published': '',
        'thrtype': '',
        'modified': '',
        'vendor': '',
        'source': '',
        'descript': '',
        'solution': '',
        'software': [],
        'refs': [],
        'patch': []
    }
    try:
        #time.sleep(random.randint(3, 10))
        vul_content = crawler_session.get(vul_url, headers=cnnvd_headers, timeout=5)
        vul_doc = pq(vul_content.text)
        vul_maindiv = vul_doc('.fl.w770')

        # 漏洞信息详情
        vul_div_detal = vul_maindiv('.detail_xq.w770')
        vul['name'] = vul_div_detal('h2').text()
        vul_div = vul_div_detal('li')
        # CNNVD编号信息已在外面添加过了，所以从1开始
        # 危害等级 severity
        vul['severity'] = vul_div.eq(1)('a').text()
        # CVE编号 cve_id
        vul['cve_id'] = vul_div.eq(2)('a').text()
        # 漏洞类型 type
        vul['type'] = vul_div.eq(3)('a').text()
        # 发布时间 published
        vul['published'] = vul_div.eq(4)('a').text()
        # 威胁类型 thrtype
        vul['thrtype'] = vul_div.eq(5)('a').text()
        # 更新时间 modified
        vul['modified'] = vul_div.eq(6)('a').text()
        # 厂商 vendor
        vendor_div = vul_div.eq(7)
        vendor_link = vendor_div('a')
        if vendor_link:
            vendor_value = vendor_link.text()
        else:
            vendor_value = vendor_div.clone().children().remove().end().text()
        vul['vendor'] = vendor_value
        # 漏洞来源 source
        source_div = vul_div.eq(8)
        source_link = source_div('a')
        if source_link:
            source_value = source_link.attr('onmouseover')[14:-3]
        else:
            source_value = source_div.clone().children().remove().end().text()
        vul['source'] = source_value

        # 漏洞简介,漏洞公告,参考网址
        vul_div_rest = vul_maindiv('.d_ldjj')
        # 漏洞简介 descript
        vul['descript'] = vul_div_rest.eq(0)('p').text()
        # 漏洞公告 solution
        vul['solution'] = vul_div_rest.eq(1)('p').text()
        # 参考网址 refs
        ref = vul_div_rest.eq(2)('p').text()
        sources = ref.split('来源:')
        refs = []
        for source in sources:
            link = source.split('链接:')
            if len(link) == 2:
                refs.append({'ref_url': link[1].strip(), 'ref_source': link[0].strip()})
        vul['refs'] = refs

        # 受影响实体,需要ajax获取更多数据,api存在问题,暂未处理
        tempdiv = vul_div_rest.eq(3)
        tempvullist = tempdiv('.vulnerability_list')('li')

        if tempvullist:
            items = []
            for i in range(0, len(tempvullist)):
                items.append(tempvullist.eq(i).text())
            vul['software'] = items
        else:
            vul['software'] = []

        # 补丁，需要再爬一个子网页,api存在问题,暂未处理
        tempdiv = vul_div_rest.eq(4)
        tempvullist = tempdiv('.vulnerability_list')('li')
        # api存在问题,暂未处理
        if tempvullist:
            items = []
            for i in range(0, len(tempvullist)):
                items.append({'title': tempvullist.eq(i).text(), 'url': cnnvd_host + tempvullist.eq(i)('a').attr('href')})
            vul['patch'] = items
        else:
            vul['patch'] = []
    except Exception as error:
        LOG.error('[爬取单个CNNVD漏洞信息失败]-[%s]-[%s]', error, vul_url)
    return vul


def _save_cnnvd_data(values):
    create_count = 0
    update_count = 0
    for cnnvd_vuln in values:
        try:
            cnnvd_id = cnnvd_vuln['cnnvd_id']
            cve_id = cnnvd_vuln['cve_id']
            if cve_id:
                search_result = ES.search(index='te-cnnvd', doc_type='te-cnnvd', q='code:"%s"' % cve_id)
                if search_result['hits']['hits']:
                    vuln = search_result['hits']['hits'][0]['_source']
                    vuln_id = search_result['hits']['hits'][0]['_id']

                    vuln['cnnvd'] = cnnvd_vuln
                    vuln['code'].append(cnnvd_id)
                    vuln['code'] = list(set(vuln['code']))
                    update_result = ES.update(
                        index='te-cnnvd',
                        doc_type='te-cnnvd',
                        id=vuln_id,
                        body={"doc": vuln})
                    if update_result['_shards']['successful'] == 1:
                        update_count += 1
                        LOG.info('[CNNVD]-[vuln_id: %s]-更新完成', vuln_id)
                    continue

            if cnnvd_id:
                search_result = ES.search(index='te-cnnvd', doc_type='te-cnnvd', q='code:"%s"' % cnnvd_id)
                if search_result['hits']['hits']:
                    vuln = search_result['hits']['hits'][0]['_source']
                    vuln_id = search_result['hits']['hits'][0]['_id']

                    vuln['cnnvd'] = cnnvd_vuln
                    if cve_id:
                        vuln['code'].append(cve_id)
                    vuln['code'] = list(set(vuln['code']))
                    update_result = ES.update(
                        index='te-cnnvd',
                        doc_type='te-cnnvd',
                        id=vuln_id,
                        body={"doc": vuln})
                    if update_result['_shards']['successful'] == 1:
                        update_count += 1
                        LOG.info('[CNNVD]-[vuln_id: %s]-更新完成', vuln_id)
                    continue

            date = cnnvd_vuln['published'].split('-')
            year = date[0]
            month = date[1]
            nowdate = get_date()
            week = time.strftime("%W")
            weeknow = time.strftime("%A")

            # # 新增数据是生成CTTL编号
            # get_result = ES.get(
            #     index="te-total",
            #     doc_type='te-total',
            #     id=year,
            #     ignore=[404, 400])
            # if get_result['found']:
            #     # 依据数据库现有的漏洞数量生成CTTL编号
            #     source = get_result['_source']
            #     count = source['data'][month] + 1
            #     num = ('000%d' % count)[-4:]
            #     cttl_id = 'CTTL-%s%s-%s' % (year, month, num)
            #
            #     source['data'][month] = count
            #     update_result = ES.update(
            #         index='te-total',
            #         doc_type='te-total',
            #         id=year,
            #         body={"doc": source})
            #     if update_result['_shards']['successful'] == 1:
            #         LOG.error('[CNNVD]-[cttl_id: %s]-数量统计加1完成', cttl_id)
            # else:
            #     # 使用初始化数据量统计数据，生成CTTL编号
            #     total = {
            #         'year': year,
            #         'modified': get_datetime(),
            #         'data': {
            #             '01': 0,
            #             '02': 0,
            #             '03': 0,
            #             '04': 0,
            #             '05': 0,
            #             '06': 0,
            #             '07': 0,
            #             '08': 0,
            #             '09': 0,
            #             '10': 0,
            #             '11': 0,
            #             '12': 0
            #         }
            #     }
            #     count = 1
            #     num = ('000%d' % count)[-4:]
            #     cttl_id = 'CTTL-%s%s-%s' % (year, month, num)
            #
            #     total['data'][month] = count
            #     create_result = ES.create(
            #         index='te-total', doc_type='te-total', id=year, body=total)
            #     if create_result['_shards']['successful'] == 1:
            #         LOG.info('[CNNVD]-[cttl_id: %s]-数量统计生成完成', cttl_id)
            #     else:
            #         LOG.info('[CNNVD]-[cttl_id: %s]-数量统计生成失败', cttl_id)
            #
            if cve_id:
                vuln = {'code': [cve_id, cnnvd_id], 'cnnvd': cnnvd_vuln}
            else:
                vuln = {'code': [cnnvd_id], 'cnnvd': cnnvd_vuln}

            create_result = ES.create(
                index="te-cnnvd", doc_type='te-cnnvd', id=cnnvd_id, body=vuln)
            if create_result['_shards']['successful'] == 1:
                create_count += 1
                LOG.info('[CNNVD]-[cnnvd_id: %s]-[cve_id: %s]-新增完成', cnnvd_id, cve_id)
            else:
                LOG.info('[CNNVD]-[cnnvd_id: %s]-[cve_id: %s]-新增失败', cnnvd_id, cve_id)
        except Exception as error:
            LOG.info('[CNNVD]-存入数据库异常-[%s]-[%s]', cnnvd_vuln, error)

    LOG.info('CNNVD漏洞数据存储成功')
    return {
        'status': 'yes',
        'result': {
            'update': update_count,
            'create': create_count,
            'total': len(values)
        }
    }


def auto_cnnvd_data(cnnvd_es_time):
    """ 更新cnnvd数据 """
    try:
        # # 依据时间判断是否爬去
        # plan_info = ES.get(
        #     index='te-plan', doc_type='te-plan', id=1, ignore=[404, 400])
        # if plan_info['found']:
        #     cnnvd_es_time = plan_info['_source']['cnnvd']
        #     cnnvd_es_time = datetime.datetime.strptime(cnnvd_es_time, '%Y-%m-%d')
        #     cnnvd_es_time = time.mktime(cnnvd_es_time.timetuple())
        # else:
        #     LOG.info('[CNNVD]-[没有更新是数据库存储的比对时间，更新结束]')
        #     return {'status': 'no', 'msg': 'view log'}

        # 获取今天的日期
        cnnvd_es_time = datetime.datetime.strptime(cnnvd_es_time, '%Y-%m-%d')
        cnnvd_es_time = time.mktime(cnnvd_es_time.timetuple())

        analysis_data = spider_cnnvd(cnnvd_es_time)
        if analysis_data['status'] == 'yes':
            save_result = _save_cnnvd_data(analysis_data['data']['cnnvd'])
            if save_result['status'] == 'yes':
                LOG.info('CNNVD数据已写入数据库')
                # plan_info['_source']['cnnvd'] = get_date()
                # rres = ES.update(
                #     index='te-plan',
                #     doc_type='te-plan',
                #     id=1,
                #     body={'doc': plan_info['_source']},
                #     ignore=[404, 400])
                # if rres['_shards']['successful'] == 1:
                #     LOG.info('CNNVD最后更新日期更新成功')
                # else:
                #     LOG.info('CNNVD最后更新日期未更新')
                print('-cnnvd-' * 12)
                print(save_result['result'])
                return save_result['result']
            else:
                LOG.info('CNNVD写入数据库失败')
    except Exception as error:
        LOG.error('CNNVD自动整合错误-[%s]', error)

    return {'update': 0, 'create': 0, 'total': 0}
