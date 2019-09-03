#!/usr/bin/env python 
# -*- coding:utf-8 -*-
""""自动爬虫入口"""
import time
import logging
from cnnvd import auto_cnnvd_data
from libs.logging import init_logging
from datetime import datetime
from libs.datetime import get_date, get_datetime


LOG = logging.getLogger(__file__)
count = 1


def start():
    spider_count = {'cnnvd': '',
                    'nvd': '',
                    'cve': '',
                    'cnvd': ''}
    # 爬虫起始时间 默认今天
    # now_date = get_date()
    now_date = '2019-01-01'
    spider_count['cnnvd'] = auto_cnnvd_data(now_date)
    spider_count['nvd'] = {}
    spider_count['cve'] = {}
    spider_count['cnvd'] = {}
    LOG.info('auto_statistics starting...')
    # auto_statistics(spider_count)
    time.sleep(60)


def autotime(h=0, m=0):
    # h表示设定的小时，m为设定的分钟
    while True:
        while True:
            now = datetime.now()
            if now.hour == h and now.minute == m:
                break
            time.sleep(60)
        start()


if __name__ == '__main__':
    init_logging(log_name='spider.log')
    LOG.info('auto_spider starting...')
    while True:
        try:
            LOG.info("spider plan:"+get_date())
            # autotime(23, 30)
            start()
            # 每天23:30执行
        except Exception as error:
            LOG.error('[spider]-[自动更新异常]-[%s]', error)
