#!/usr/bin/python3
# -*- coding:utf-8 -*-
""" 日志配置 """

import os
import logging
from logging.handlers import RotatingFileHandler
from libs.constants import LOGGING_DIR


def init_logging(log_name="mylog.log"):
    """Initializes logging."""

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if not os.path.exists(LOGGING_DIR):
        os.makedirs(LOGGING_DIR)

    log_file = os.path.join(LOGGING_DIR, log_name)

    # fh = logging.FileHandler(LOG_FILE)
    # fh.setLevel(logging.DEBUG)

    # File size split log
    local_log = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=90)
    local_log.setLevel(logging.DEBUG)

    logging.getLogger("elasticsearch").setLevel(logging.WARNING)
    windows = logging.StreamHandler()
    windows.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s [%(name)s:%(lineno)d] %(levelname)s: %(message)s")
    local_log.setFormatter(formatter)
    windows.setFormatter(formatter)

    logger.addHandler(windows)
    logger.addHandler(local_log)
