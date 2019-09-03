
# cnnvd_spider_report

 - 自动话爬取cnnvd漏洞信息，
 - 存储到elasticsearch数据库 
 - 并对数据库数据进行分析 
 - 按月生成csv文件的漏洞报告

```
 "severity": {
                                "type": "text",
                                "analyzer": "whitespace",
                                "search_analyzer": "whitespace",
                                "fielddata": true,
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                            },
```
ps:需要对分词的索引mapping进行修改，这是部分修改实例，主要修改以下参数

```
"analyzer": "whitespace",
 "search_analyzer": "whitespace",
 "fielddata": true,
```

> www.austfish.cn
