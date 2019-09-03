#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from libs import datetime
import requests
import re
import numpy as np
from pylab import *
from libs.elastic import ES
from libs.datetime import get_date2, get_datetime, get_custom_time
from esdata import statistics_run
from libs.es_search_range_time import get_count
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys


mpl.rcParams['font.size'] = 15
custom_font = mpl.font_manager.FontProperties(fname='ttf/仿宋GB2312.ttf')
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


def tiaoxing_chart(index, value):
    """条形统计图"""
    # 中文显示
    # value = [22, 13, 34]
    # index = ["root", "admin", "lyshark"]
    # index=np.arange(5)
    plt.bar(left=index, height=value, color="green", width=0.5)
    plt.show()


def zhexian_chart():
    """折线统计图"""
    x = np.linspace(-10, 10, 100)
    y = x ** 3
    plt.plot(x, y, linestyle="--", color="green", marker="<")

    plt.show()


def bingzhuang_chart(labels, fracs):
    """饼状统计图"""
    # labels = "cangjingkong", "jizemingbu", "boduoyejieyi", "xiaozemaliya"
    # fracs = [45, 10, 30, 15]

    plt.axes(aspect=1)

    explode = [0, 0, 0, 0]
    plt.pie(x=fracs, labels=labels, autopct="%.2f%%", explode=explode)
    plt.show()


def level_chart():
    index = []
    value = []
    level_id = get_date2()
    search_result = ES.search(index='te-level', doc_type='te-level', q='_id:"%s"' % level_id)
    if search_result['hits']['hits']:
        datas = search_result['hits']['hits'][0]['_source']['data']
        for data in datas:
            if data['key'] == '合计':
                break
            index.append(data['key'])
            value.append(int(data['doc_count']))
    print(index)
    print(value)
    bingzhuang_chart(index, value)


if __name__ == '__main__':
    zhexian_chart()
    level_chart()