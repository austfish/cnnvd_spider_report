""" 操作ES """

from elasticsearch import Elasticsearch
from libs.constants import YAML_CONFIG


ES = Elasticsearch([{"host": YAML_CONFIG['Elastic']['host']}])
ES2 = Elasticsearch([{"host": YAML_CONFIG['Elastic2']['host']}])