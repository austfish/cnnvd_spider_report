#!/usr/bin/env python 
# -*- coding:utf-8 -*-
""""自动爬虫入口"""
import time
import logging
from cnnvd import auto_cnnvd_data
from libs.logging import init_logging
from datetime import datetime
from libs.datetime import get_date, get_datetime, get_custom_time, getoldday, get_year, get_onlymonth, get_month
from statistics import auto_statistics
from statistics2 import auto_statistics2
from esdata import statistics_run
from csvdate import auto_updata_csv


LOG = logging.getLogger(__file__)
count = 1
# 获取当前月份，只统计当前月份
year_num = get_year()


def start():
    spider_count = {'cnnvd': ''}
    # 爬虫起始时间 默认今天
    now_time = get_date()
    # now_date = '2019-08-01'
    now_date = getoldday(2)
    spider_count['cnnvd'] = auto_cnnvd_data(now_date)
    LOG.info('[CNNVD]-Time:(%s-%s)-Date:[%s]', now_date, now_time, spider_count)

    time.sleep(10)

    LOG.info('auto_statistics starting...')
    auto_statistics(statistics_run(year_num))
    # 统计数据更新到docker-es
    auto_statistics2(statistics_run(year_num))
    # 统计更新到工控数据库
    time.sleep(10)
    # 自动更新月报数据csv文件
    auto_updata_csv(get_onlymonth())


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
    try:
        LOG.info("spider plan:" + get_date())
        # autotime(23, 30)
        start()
        # 每天23:30执行
    except Exception as error:
        LOG.error('[spider]-[自动更新异常]-[%s]', error)
