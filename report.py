#!/usr/bin/env python
# -*- coding:utf-8 -*-


import time
import logging
from libs.elastic import ES
LOG = logging.getLogger(__file__)
TOTALS = []
LEVELS = []
VENDORS = []
VTYPE = []


def _tj_total(year, month):
    for total in TOTALS:
        if total['year'] == year:
            total['data'][month] = total['data'][month] + 1
            return
    total = {
        'year': year,
        'modified': time.strftime('%Y-%m-%d %X', time.localtime()),
        'data': {
            '01': 0,
            '02': 0,
            '03': 0,
            '04': 0,
            '05': 0,
            '06': 0,
            '07': 0,
            '08': 0,
            '09': 0,
            '10': 0,
            '11': 0,
            '12': 0
        }
    }
    total['data'][month] = total['data'][month] + 1
    TOTALS.append(total)


def _tj_level(year, month, level):
    for level_info in LEVELS:
        if level_info['year'] == year:
            level_info['data'][month][level] = level_info['data'][month][level] + 1
            return
    level_data = {
        'year': year,
        'modified': time.strftime('%Y-%m-%d %X', time.localtime()),
        'data': {
            '01': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '02': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '03': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '04': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '05': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '06': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '07': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '08': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '09': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '10': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '11': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0},
            '12': {'low': 0, 'medium': 0, 'height': 0, 'unknow': 0}
        }
    }
    level_data['data'][month][level] = level_data['data'][month][level] + 1
    LEVELS.append(level_data)


def _tj_vendor(year, month, vendor):
    for vendor_info in VENDORS:
        if vendor_info['year'] == year:
            for obj in vendor_info['data'][month]:
                if obj['vendor'] == vendor:
                    obj['value'] = obj['value'] + 1
                    break
            else:
                vendor_info['data'][month].append({'vendor': vendor, 'value': 1})
            return
    vendor_data = {
        'year': year,
        'modified': time.strftime('%Y-%m-%d %X', time.localtime()),
        'data': {
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
            '12': []
        }
    }
    vendor_data['data'][month].append({'vendor': vendor, 'value': 1})
    VENDORS.append(vendor_data)


def _tj_type(year, month, v_type):
    for type_info in VTYPE:
        if type_info['year'] == year:
            for obj in type_info['data'][month]:
                if obj['type'] == v_type:
                    obj['value'] = obj['value'] + 1
                    break
            else:
                type_info['data'][month].append({'type': v_type, 'value': 1})
            return
    type_data = {
        'year': year,
        'modified': time.strftime('%Y-%m-%d %X', time.localtime()),
        'data': {
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
            '12': []
        }
    }
    type_data['data'][month].append({'type': v_type, 'value': 1})
    VTYPE.append(type_data)


def _get_values(cnnvd):
    severity = 'unknow'
    vendor = 'unknow'
    v_type = 'unknow'
    t = cnnvd['cnnvd_id'].split('-')[1]
    year = t[0:4]
    month = t[4:6]
    severity = cnnvd['severity']
    if severity.find('高') != -1 or severity.find('超') != -1:
        severity = 'height'
    elif severity.find('中') != -1:
        severity = 'medium'
    elif severity.find('低') != -1:
        severity = 'low'
    else:
        severity = 'unknow'
    v_type = cnnvd['type']
    vendor = cnnvd['vendor']
    return ('%s,%s,%s,%s,%s' % (year, month, severity.lower(), vendor, v_type)).split(',')


def auto_report_data():
    """ doc """
    try:
        es_infos = ES.search(index='te-cnnvd', doc_type='te-cnnvd', size=10000)
        infos = es_infos['hits']['hits']
        print('infos length: %s' % len(infos))
        for info in infos:
            try:
                values = _get_values(info['_source']['cnnvd'])
                year = values[0]
                month = values[1]
                level = values[2]
                vendor = values[3]
                v_type = values[4]
                _tj_total(year, month)
                _tj_level(year, month, level)
                _tj_vendor(year, month, vendor)
                _tj_type(year, month, v_type)
            except Exception as error:
                LOG.error('[REPORT]-[cttl_id: %s]-[%s]', info['_id'], error)
        # for total in TOTALS:
        #     ES.index(index='te-total', doc_type='te-total', id=total['year'], body=total)
        # for level in LEVELS:
        #     ES.index(index='te-level', doc_type='te-level', id=level['year'], body=level)
        # for vendor in VENDORS:
        #     ES.index(index='te-vendor', doc_type='te-vendor', id=vendor['year'], body=vendor)
        # for v_type in VTYPE:
        #     ES.index(index='te-type', doc_type='te-type', id=v_type['year'], body=v_type)
        print(LEVELS)
    except Exception as error:
        LOG.error('统计数据自动整合错误-[%s]', error)
    return {'update': 0, 'create': 0, 'total': 0}


