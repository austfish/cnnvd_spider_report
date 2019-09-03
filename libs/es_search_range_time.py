#!/usr/bin/python3
# -*- coding:utf-8 -*-
""" es 时间范围查询 """
from libs.datetime import get_year
from libs.elastic import ES

year = "2019"
next_year = "2020"

mon_list = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13"]

mon = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    'Aug': "08",
    'Sep': "09",
    'Oct': "10",
    "Nov": "11",
    "Dec": "12",
}

zd_time_0 = {
    "match_all": {}
}

zd_time_1 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-01-01T00:00:00.000000+0800",
            "lte": year + "-02-01T00:00:00.000000+0800"
        }
    }
}

zd_time_2 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-02-01T00:00:00.000000+0800",
            "lte": year + "-03-01T00:00:00.000000+0800"
        }
    }
}

zd_time_3 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-03-01T00:00:00.000000+0800",
            "lte": year + "-04-01T00:00:00.000000+0800"
        }
    }
}

zd_time_4 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-04-01T00:00:00.000000+0800",
            "lte": year + "-05-01T00:00:00.000000+0800"
        }
    }
}

zd_time_5 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-05-01T00:00:00.000000+0800",
            "lte": year + "-06-01T00:00:00.000000+0800"
        }
    }
}

zd_time_6 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-06-01T00:00:00.000000+0800",
            "lte": year + "-07-01T00:00:00.000000+0800"
        }
    }
}

zd_time_7 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-07-01T00:00:00.000000+0800",
            "lte": year + "-08-01T00:00:00.000000+0800"
        }
    }
}

zd_time_8 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-08-01T00:00:00.000000+0800",
            "lte": year + "-09-01T00:00:00.000000+0800"
        }
    }
}

zd_time_9 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-09-01T00:00:00.000000+0800",
            "lte": year + "-10-01T00:00:00.000000+0800"
        }
    }
}

zd_time_10 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-10-01T00:00:00.000000+0800",
            "lte": year + "-11-01T00:00:00.000000+0800"
        }
    }
}

zd_time_11 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-11-01T00:00:00.000000+0800",
            "lte": year + "-12-01T00:00:00.000000+0800"
        }
    }
}

zd_time_12 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-12-01T00:00:00.000000+0800",
            "lte": next_year + "-01-01T00:00:00.000000+0800"
        }
    }
}

zd_time_13 = {
    "range": {
        "cnnvd.published": {
            "gte": year + "-01-01T00:00:00.000000+0800",
            "lte": next_year + "-01-01T00:00:00.000000+0800"
        }
    }
}


def get_es_zdquery(mon):
    """ mon=01/02/.../12/13:全年 """
    if mon == "01":
        return zd_time_1
    elif mon == "02":
        return zd_time_2
    elif mon == "03":
        return zd_time_3
    elif mon == "04":
        return zd_time_4
    elif mon == "05":
        return zd_time_5
    elif mon == "06":
        return zd_time_6
    elif mon == "07":
        return zd_time_7
    elif mon == "08":
        return zd_time_8
    elif mon == "09":
        return zd_time_9
    elif mon == "10":
        return zd_time_10
    elif mon == "11":
        return zd_time_11
    elif mon == "12":
        return zd_time_12
    elif mon == "13":
        return zd_time_13
    else:
        return zd_time_0


def get_es_exists(field):
    doc = {
        "exists": {
            "field": "cnnvd." + field
        }
    }
    return doc


def get_type(flag):
    """漏洞类型：跨站脚本"""
    type_list = []
    type_mon_list = []
    num_count = 0
    body_type = {
        "query":
            get_es_zdquery(flag),
        "aggs": {
            "sum_logtype": {
                "terms": {
                    "field": "cnnvd.type",
                    "size": 40
                }
            }
        }
    }
    search_result = ES.search(index='te-cnnvd', doc_type='te-cnnvd', body=body_type)
    type_list = search_result['aggregations']['sum_logtype']['buckets']
    for list in type_list:
        type_mon_list.append({'type': list['key'], 'value': list['doc_count']})
        num_count = num_count + list['doc_count']
    # 数据补充
    count = get_count(flag)
    uunknow = count - num_count
    type_mon_list.append({'type': '未知', 'value': uunknow})
    return type_mon_list


def get_severity(flag, exists):
    """漏洞等级：高危"""
    num_count = 0
    body_severity = {
        "query":
            {
                "bool": {
                    "filter": [get_es_zdquery(flag),
                               get_es_exists(exists)]
                }
            }
        ,
        "aggs": {
            "sum_logtype": {
                "terms": {
                    "field": "cnnvd.severity",
                    "size": 40
                }
            }
        }
    }
    data_list = {
        "unknow": 0,
        "low": 0,
        "medium": 0,
        "height": 0,
        "sdanger": 0
    }
    search_result = ES.search(index='te-cnnvd', doc_type='te-cnnvd', body=body_severity)
    count = search_result['hits']['total']
    severity_list = search_result['aggregations']['sum_logtype']['buckets']
    for severity in severity_list:
        if severity['key'] == '低危':
            data_list['low'] = severity['doc_count']
        if severity['key'] == '高危':
            data_list['height'] = severity['doc_count']
        if severity['key'] == '中危':
            data_list['medium'] = severity['doc_count']
        if severity['key'] == '超危':
            data_list['sdanger'] = severity['doc_count']
        num_count = num_count + severity['doc_count']
    data_list['unknow'] = count - num_count
    return data_list


def get_count(flag):
    body_type = {
        "query":
            get_es_zdquery(flag)
    }

    search_result = ES.search(index='te-cnnvd', doc_type='te-cnnvd', body=body_type)
    count = search_result['hits']['total']
    return count


def get_top_vendor(flag):
    top_list = {}
    mon_top_list = []
    aa = {}
    venders = ['gitlab',
               'zoneminder',
               'qualcomm',
               'glyphandcog',
               'primasystems',
               'acdsee',
               'txjia',
               'redhat',
               'Google',
               'apple',
               'nec',
               'sap',
               'oracle',
               'lfdycms',
               'croogo',
               'ibm',
               'eventum_project',
               'macpaw',
               'creditease-sec',
               'webassembly',
               'nasm',
               'nortekcontrol',
               'nedi',
               'juniper',
               'trendnet',
               'xnview',
               'joomla',
               'canonical',
               'identicard',
               'jenkins',
               'ucms_project',
               'linux',
               'moxa',
               'microsoft',
               'atlassian',
               'mozilla',
               'fasterxml',
               'mailenable',
               'dlink',
               'foxitsoftware',
               'gnu',
               'jetbrains',
               'elfutils_project',
               'cisco',
               'brocade',
               'gnuboard',
               'zohocorp',
               'adobe',
               'Apache',
               'mz-automation',
               'odoo',
               'f5',
               'cacti',
               'imagemagick',
               'wireshark',
               'linaro',
               'dolibarr',
               'rdbrck',
               'jpcert'
               ]
    for vender in venders:
        search_body = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "cnnvd.descript": vender
                        }
                    },
                    "filter": get_es_zdquery(flag)
                }
            },
            "size": 10000
        }
        search_result = ES.search(index='te-cnnvd', body=search_body)
        hits = search_result['hits']
        total = hits['total']
        aa[vender] = total
    sorted_dict = sorted(aa.items(), key=lambda item: item[1], reverse=True)
    for k in sorted_dict:
        if k[1] != 0:
            top_list[k[0]] = k[1]
    for key, value in top_list.items():
        mon_top_list.append({'vendor': key, 'value': value})
    return mon_top_list
