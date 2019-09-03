#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import logging
import os
import csv
from cnnvd import auto_cnnvd_data
from libs.elastic import ES
from libs.logging import init_logging
from datetime import datetime
from libs.datetime import get_date, get_datetime, get_custom_time, getoldday, get_year
from statistics2 import auto_statistics2
# 统计结果存入工控数据库
from esdata import statistics_run
from libs.es_search_range_time import get_type, get_top_vendor, get_severity, get_count, mon_list
from esdata import ld_type, ld_vendor, ld_statisyics, ld_severity


def csvdata(filename, headers, rows):
    """
    :param filename:存入文件名
    :param headers: 数据头
    :param rows: 数据列表
    :return: None
    """
    # headers = ['class', 'name', 'sex', 'height', 'year']
    # rows = [
    #     {'class': 1, 'name': 'xiaoming', 'sex': 'male', 'height': 168, 'year': 23},
    #     {'class': 1, 'name': 'xiaohong', 'sex': 'female', 'height': 162, 'year': 22},
    #     {'class': 2, 'name': 'xiaozhang', 'sex': 'female', 'height': 163, 'year': 21},
    #     {'class': 2, 'name': 'xiaoli', 'sex': 'male', 'height': 158, 'year': 21},
    # ]

    with open(filename, 'w', newline='')as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)
    print(filename + "csv写入成功")


def type_csv_data(datas, count):
    """
    :param datas: es数据库数据
    :param count: 数据总量
    :return: csv要求数据
    """
    type_list = []
    for data in datas:
        type_list.append({'漏洞类型': data['type'], '数量': data['value'], '百分比': format(data['value'] / count * 100, '.2f')})
    return type_list


def vendor_csv_data(datas):
    """
        :param datas: es数据库数据
        :return: csv要求数据
        """
    vendor_list = []
    for data in datas:
        vendor_list.append({'厂商名称': data['vendor'], '数量': data['value']})
    return vendor_list


def total_csv_data(datas, mon_id):
    """
    :param datas: es数据库数据
    :return: csv要求数据
    """
    mon_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    total_list = []
    for mon in mon_list:
        total_list.append({'月份': get_year() + mon, '数量': datas[mon]})
        if mon == mon_id:
            break
    return total_list


def level_csv_data(datas, count, mon_id):
    """
    :param datas: es数据库数据
    :param count: 数据总量
    :param mon_id: 当前月份
    :return: csv要求格式
    """
    levels = ['sdanger', 'height', 'medium', 'low', 'unknow']
    levelname = {'sdanger': '超危', 'height': '高危', 'medium': '中危', 'low': '低危', 'unknow': '未知'}
    level_repair = get_severity(mon_id, 'patch')
    repair_count = 0
    for level in levels:
        repair_count = repair_count + level_repair[level]
    level_list = []
    for level in levels:
        level_list.append(
            {'等级': levelname[level],
             '数量': datas[level],
             '修复数量': level_repair[level],
             '修复率': format(level_repair[level] / datas[level] * 100, '.2f')})
    # 合计
    level_list.append({'等级': '合计',
                       '数量': count,
                       '修复数量': repair_count,
                       '修复率': format(repair_count / count * 100, '.2f')})
    return level_list


def file_exit(file_name):
    if os.path.exists(file_name) is False:
        os.makedirs(file_name)


def auto_updata_csv(mon_id):
    """
    自动更新
    H:\\Adate\\loudong\\201908内
    csv文件内容
    :return:
    """
    year_id = get_year()
    count = get_count(mon_id)
    file_flag = str(year_id) + mon_id

    # csv文件名
    file_type = 'H:\\Adate\\loudong\\' + file_flag + '\\漏洞类型分布' + file_flag + '至' + file_flag + '.csv'
    file_vendor = 'H:\\Adate\\loudong\\' + file_flag + '\\厂商排名' + file_flag + '至' + file_flag + '.csv'
    file_level = 'H:\\Adate\\loudong\\' + file_flag + '\\漏洞安全等级分布' + file_flag + '至' + file_flag + '.csv'
    file_total = 'H:\\Adate\\loudong\\' + file_flag + '\\漏洞数量统计201901至' + file_flag + '.csv'
    file_dir = 'H:\\Adate\\loudong\\' + file_flag
    # 检测文件是否存在，不存在自动创建
    file_exit(file_dir)

    # csv文件头
    headers_type = ['漏洞类型', '数量', '百分比']
    headers_vendor = ['厂商名称', '数量']
    headers_level = ['等级', '数量', '修复数量', '修复率']
    headers_total = ['月份', '数量']

    # 查询数据库
    type_search_result = ES.search(index='te-type', doc_type='te-type', q='_id:"%s"' % year_id)
    vendor_search_result = ES.search(index='te-vendor', doc_type='te-vendor', q='_id:"%s"' % year_id)
    level_search_result = ES.search(index='te-level', doc_type='te-level', q='_id:"%s"' % year_id)
    total_search_result = ES.search(index='te-total', doc_type='te-total', q='_id:"%s"' % year_id)

    # es数据库查询分词聚类数据结果
    type_data = type_search_result['hits']['hits'][0]['_source']['data'][mon_id]
    vendor_data = vendor_search_result['hits']['hits'][0]['_source']['data'][mon_id]
    level_data = level_search_result['hits']['hits'][0]['_source']['data'][mon_id]
    total_data = total_search_result['hits']['hits'][0]['_source']['data']

    print(type_data)
    print(vendor_data)
    print(level_data)
    print(total_data)
    type_csv = []
    vendor_csv = []
    level_csv = []
    total_csv = []

    # 数据格式处理
    type_csv = type_csv_data(type_data, count)
    vendor_csv = vendor_csv_data(vendor_data)
    total_csv = total_csv_data(total_data, mon_id)
    level_csv = level_csv_data(level_data, count, mon_id)

    # 数据存入csv文件
    csvdata(file_type, headers_type, type_csv)
    csvdata(file_vendor, headers_vendor, vendor_csv)
    csvdata(file_total, headers_total, total_csv)
    csvdata(file_level, headers_level, level_csv)
    # for type in type_data:
    #     type['repair'] = format()
