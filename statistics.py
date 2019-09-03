#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
统计数据：日、周、月、年
author: fisher
date: 2019.8.13
todo:
字段值是否有不合常规的：受影响实体以及补丁
issue:
统计漏洞数据
"""
import pandas as pd
import datetime
import calendar
import json
import logging
import re
import time
import requests
from pyquery import PyQuery as pq
from libs.elastic import ES
from libs.datetime import get_date2, get_datetime, get_week, get_month, days_cur_month, get_year
from esdata import statistics_run


LOG = logging.getLogger(__file__)
datalists = ['cnnvd', 'nvd', 'cve', 'cnvd']
now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))


def up_type(date):
    try:
        year_id = get_year()
        search_result = ES.search(index='te-type', doc_type='te-type', q='_id:"%s"' % year_id)
        # 判断数据是否存在
        if search_result['hits']['hits']:
            result = ES.update(
                index='te-type',
                doc_type='te-type',
                id=year_id,
                body={"doc": date})
        else:
            result = ES.create(
                index='te-type',
                doc_type='te-type',
                id=year_id,
                body=date)
        if result['_shards']['successful'] == 1:
            LOG.info('[up_type]-[day_id: %s]-更新完成', year_id)
    except Exception as error:
        LOG.error('up_type_更新错误-[%s]', error)


def up_level(date):
    try:
        year_id = get_year()
        search_result = ES.search(index='te-level', doc_type='te-level', q='_id:"%s"' % year_id)
        # 判断数据是否存在
        if search_result['hits']['hits']:
            result = ES.update(
                index='te-level',
                doc_type='te-level',
                id=year_id,
                body={"doc": date})
        else:
            result = ES.create(
                index='te-level',
                doc_type='te-level',
                id=year_id,
                body=date)
        if result['_shards']['successful'] == 1:
            LOG.info('[up_level]-[day_id: %s]-更新完成', year_id)
    except Exception as error:
        LOG.error('up_level_更新错误-[%s]', error)


def up_total(date):
    try:
        year_id = get_year()
        search_result = ES.search(index='te-total', doc_type='te-total', q='_id:"%s"' % year_id)
        # 判断数据是否存在
        if search_result['hits']['hits']:
            result = ES.update(
                index='te-total',
                doc_type='te-total',
                id=year_id,
                body={"doc": date})
        else:
            result = ES.create(
                index='te-total',
                doc_type='te-total',
                id=year_id,
                body=date)
        if result['_shards']['successful'] == 1:
            LOG.info('[up_total]-[day_id: %s]-更新完成', year_id)
    except Exception as error:
        LOG.error('up_total_更新错误-[%s]', error)


def up_vendor(date):
    try:
        year_id = get_year()
        search_result = ES.search(index='te-vendor', doc_type='te-vendor', q='_id:"%s"' % year_id)
        # 判断数据是否存在
        if search_result['hits']['hits']:
            result = ES.update(
                index='te-vendor',
                doc_type='te-vendor',
                id=year_id,
                body={"doc": date})
        else:
            result = ES.create(
                index='te-vendor',
                doc_type='te-vendor',
                id=year_id,
                body=date)
        if result['_shards']['successful'] == 1:
            LOG.info('[up_vendor]-[day_id: %s]-更新完成', year_id)
    except Exception as error:
        LOG.error('up_vendor_更新错误-[%s]', error)


def up_all(date):
    try:
        year_id = get_year()
        search_result = ES.search(index='te-stat', doc_type='te-stat', q='_id:"%s"' % year_id)
        # 判断数据是否存在
        if search_result['hits']['hits']:
            result = ES.update(
                index='te-stat',
                doc_type='te-stat',
                id=year_id,
                body={"doc": date})
        else:
            result = ES.create(
                index='te-stat',
                doc_type='te-stat',
                id=year_id,
                body=date)
        if result['_shards']['successful'] == 1:
            print('[up_alldate]-[day_id: %s]-更新完成', year_id)
            LOG.info('[up_alldate]-[day_id: %s]-更新完成', year_id)
    except Exception as error:
        LOG.error('up_alldate_更新错误-[%s]', error)


def auto_statistics(date):
    try:
        day_id = get_date2()
        up_level(date['severity'])
        up_total(date['count'])
        up_type(date['type'])
        up_vendor(date['vendor'])
        up_all(date)
        LOG.info('[up_statistics]-[day_id: %s]-更新完成', day_id)
    except Exception as error:
        LOG.error('up_statistics_更新错误-[%s]', error)