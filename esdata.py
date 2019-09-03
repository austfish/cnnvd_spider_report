#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from libs.elastic import ES
import datetime
import time
from report import auto_report_data
from libs.datetime import get_datetime, get_year
from libs.es_search_range_time import get_es_zdquery, mon, get_count, get_type, get_severity, mon_list, get_top_vendor

nowday = datetime.datetime.now()


def ld_statisyics(year_count):
    """漏洞数量统计"""
    # mon_count默认比统计月份大一
    list_count = {'year': str(year_count), 'modified': get_datetime(), 'data': {}}
    for value in range(1, 13):
        list_count['data'][mon_list[value]] = get_count(mon_list[value])
    return list_count


def ld_type(year_count):
    """漏洞类型匹配"""
    type_year_list = {
        '01': [],
        '02': [],
        '03': [],
        '04': [],
        '05': [],
        '06': [],
        '07': [],
        '08': [],
        '09': [],
        '10': [],
        '11': [],
        '12': [],
    }
    count = get_count(year_count)
    mon_counts = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for mon_count in mon_counts:
        type_year_list[mon_count] = get_type(mon_count)

    # for data in datas:
    #     data['count_rate'] = format(int(data['doc_count'])/int(count)*100, '.2f')
    # type_list = datas
    list_type = {'year': str(year_count), 'modefied': get_datetime(), 'data': type_year_list}
    return list_type


def ld_severity(year_count):
    """漏洞威胁等级统计"""
    # 漏洞修复参数
    # mon_count = 8
    # count = 0
    # repair_count = 0
    # repair_rate = ''
    all_field = 'cnnvd_id'
    exists_field = 'patch'
    #
    # ld_list = get_severity(mon_list[mon_count], all_field)
    # for i in range(0, 4):
    #     ld_list[i]['repair'] = get_severity(mon_list[mon_count], exists_field)[i]['doc_count']
    #     ld_list[i]['repair_rate'] = str(format(int(ld_list[i]['repair'])/int(ld_list[i]['doc_count'])*100, '.2f'))+'%'
    #     count = count + ld_list[i]['doc_count']
    #     repair_count = repair_count + ld_list[i]['repair']
    # repair_rate = str(format(int(repair_count)/int(count)*100, '.2f'))+'%'
    # severity_count = {'key': '合计', 'doc_count': count, 'repair': repair_count, 'repair_rate': repair_rate}
    # ld_list.append(severity_count)
    # severity = {'now': get_datetime(), 'type': "等级统计", 'mon': mon_list[mon_count], 'data': ld_list}

    ld_list = {
        '01': {},
        '02': {},
        '03': {},
        '04': {},
        '05': {},
        '06': {},
        '07': {},
        '08': {},
        '09': {},
        '10': {},
        '11': {},
        '12': {},
    }
    mon_counts = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for mon in mon_counts:
        ld_list[mon] = get_severity(mon, all_field)
    list_severity = {'year': str(year_count), 'modified': get_datetime(), 'data': ld_list}
    return list_severity


def ld_vendor(year_count):
    """漏洞厂商统计"""
    vendor_year_list = {
        '01': [],
        '02': [],
        '03': [],
        '04': [],
        '05': [],
        '06': [],
        '07': [],
        '08': [],
        '09': [],
        '10': [],
        '11': [],
        '12': [],
    }
    mon_counts = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for mon_count in mon_counts:
        vendor_year_list[mon_count] = get_top_vendor(mon_count)
    list_vendor = {'year': str(year_count), 'modefied': get_datetime(), 'data': vendor_year_list}
    return list_vendor


def statistics_run(year_num):
    stat = {'type': ld_type(year_num), 'count': ld_statisyics(year_num), 'severity': ld_severity(year_num), 'vendor': ld_vendor(year_num)}
    # auto_report_data()
    print(ld_severity(year_num))
    print(ld_type(year_num))
    print(ld_statisyics(year_num))
    print(ld_vendor(year_num))
    return stat
