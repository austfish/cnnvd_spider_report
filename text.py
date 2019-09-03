#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import time
import logging
import csv
from csvdate import auto_updata_csv
from cnnvd import auto_cnnvd_data
from libs.elastic import ES
from libs.logging import init_logging
from datetime import datetime
from libs.datetime import get_date, get_datetime, get_custom_time, getoldday, get_year, get_onlymonth
from statistics2 import auto_statistics2
# 统计结果存入工控数据库
from esdata import statistics_run
from libs.es_search_range_time import get_type, get_top_vendor, get_severity
from esdata import ld_type, ld_vendor, ld_statisyics, ld_severity


def csvdata(headers, rows):
    # headers = ['class', 'name', 'sex', 'height', 'year']

    # rows = [
    #     {'class': 1, 'name': 'xiaoming', 'sex': 'male', 'height': 168, 'year': 23},
    #     {'class': 1, 'name': 'xiaohong', 'sex': 'female', 'height': 162, 'year': 22},
    #     {'class': 2, 'name': 'xiaozhang', 'sex': 'female', 'height': 163, 'year': 21},
    #     {'class': 2, 'name': 'xiaoli', 'sex': 'male', 'height': 158, 'year': 21},
    # ]

    with open('test2.csv', 'w', newline='')as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)


if __name__ == '__main__':
    auto_updata_csv()
    # doc = {
    #     "query":
    #         {
    #             "bool": {
    #                 "should": [
    #                     {
    #                         "term": {
    #                             "cnnvd.severity": ""
    #                         }
    #                     },
    #                     {
    #                         "bool": {
    #
    #                             "must": {
    #                                 "exists": {
    #                                     "field": "cnnvd.severity"
    #                                 }
    #                             },
    #                             "filter": [{
    #                                 "range": {
    #                                     "cnnvd.published": {
    #                                         "gte": "2019-08-01T00:00:00.000000+0800",
    #                                         "lte": "2019-09-01T00:00:00.000000+0800"
    #                                     }
    #                                 }
    #                             }]
    #                         }
    #                     }
    #                 ]
    #
    #             }
    #         },
    #     "size": 10000
    # }
    # count = 0
    # count_repaire = 0
    # search_result = ES.search(index='te-cnnvd', doc_type='te-cnnvd', body=doc)
    # severity_list = search_result['hits']['hits']
    # print(severity_list)
    # for severity in severity_list:
    #     if severity['_source']['cnnvd']['severity'] == '中危':
    #         count = count + 1
    #     if severity['_source']['cnnvd']['severity'] == '中危' and severity['_source']['cnnvd']['patch'] != []:
    #         count_repaire = count_repaire + 1
    # print(count)
    # print(count_repaire)