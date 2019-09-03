#!/usr/bin/python3
# -*- coding:utf-8 -*-
""" 各种本地化时间 """
import time
import datetime
from datetime import date, timedelta, datetime


def getoldday(count):
    yesterday = (date.today() + timedelta(days=-count)).strftime("%Y-%m-%d")    # 昨天日期
    return yesterday


def get_time():
    """
    当前时间
        eg:10:10:10
    """
    return time.strftime('%X', time.localtime())


def get_datetime():
    """
    当前日期和时间
        eg:2018-10-10 10:10:10
    """
    return time.strftime('%Y-%m-%d %X', time.localtime())


def get_date():
    """
    当前日期
        eg:2018-10-10
    """
    return time.strftime('%Y-%m-%d', time.localtime())


def get_date2():
    """
        当前日期
            eg:20181010
        """
    return time.strftime('%Y%m%d', time.localtime())


def get_unixtime():
    """
    当前时间的unix时间戳
        eg: 1536218640
    """
    return int(time.time())


def get_week():
    """
    当前时间在所在年份的周数
    :return:1
    """
    return time.strftime("%W", time.localtime())


def get_month():
    """
    当前日期
        eg:201810
    """
    return time.strftime('%Y%m', time.localtime())


def get_onlymonth():
    """
    当前日期
        eg:10
    """
    return time.strftime('%m', time.localtime())


def get_year():
    """
    当前日期
        eg:2018
    """
    return time.strftime('%Y', time.localtime())


def get_custom_time(time_format):
    """
    自定义格式时间
    ~~~~~
        eg1:
        time_format: %a %b %d %Y %X
        return: Fri Sep 14 2018 16:48:13

        eg2: 当前日期和时间
        time_format: %Y-%m-%d %X
        return: 2018-10-10 10:10:10

        eg3: 年月
        time_format: %Y%m
        return: 201810
    """
    return time.strftime(time_format, time.localtime())


def days_cur_month():
    """
        输出当前月的所有日期
            eg:['20190701', '20190702', '20190703', '20190704', '20190705', '20190706', '20190707', '20190708',
             '20190709', '20190710', '20190711', '20190712', '20190713', '20190714', '20190715', '20190716', '20190717',
              '20190718', '20190719', '20190720', '20190721', '20190722', '20190723', '20190724', '20190725',
               '20190726', '20190727', '20190728', '20190729', '20190730', '20190731']
        """
    m = datetime.now().month
    y = datetime.now().year
    ndays = (date(y, m+1, 1) - date(y, m, 1)).days
    d1 = date(y, m, 1)
    d2 = date(y, m, ndays)
    delta = d2 - d1

    return [(d1 + timedelta(days=i)).strftime('%Y%m%d') for i in range(delta.days + 1)]