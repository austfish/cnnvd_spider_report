""" 项目运行常量参数 """

import os
import yaml

# 当前文件路径
_CURRENT_DIR = os.path.abspath(os.path.dirname('__file__'))
# 项目根路径
PROJECT_ROOT = os.path.normpath(_CURRENT_DIR)
# 配置文件路径
CONFIG_DIR = os.path.join(PROJECT_ROOT, 'config')
# 日志文件路径
LOGGING_DIR = os.path.join(PROJECT_ROOT, 'logs')
# 配置文件
YAML_CONFIG = yaml.load(open(os.path.join(CONFIG_DIR, 'config.yml')), Loader=yaml.FullLoader)


# 资源目录
RESOURCE_DIR = os.path.join(PROJECT_ROOT, 'resource')
# 漏洞xml文件
ZIP_DIR = os.path.join(RESOURCE_DIR, 'zip')
# 漏洞xml文件
XML_DIR = os.path.join(RESOURCE_DIR, 'xml')
# 漏洞JSON文件
JSON_DIR = os.path.join(RESOURCE_DIR, 'json')
