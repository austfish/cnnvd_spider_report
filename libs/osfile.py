import os
import zipfile
import shutil
import hashlib
import logging
from logging.handlers import RotatingFileHandler
from libs.constants import YAML_CONFIG, LOGGING_DIR


def init_mylog(log_name="mylog.log"):
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


def compression_file_zip(src_dir, dst_file):
    """ 压缩文件 """
    try:
        zip_path_obj = zipfile.ZipFile(dst_file, 'w', zipfile.ZIP_DEFLATED)
        for parent, dirs, filenames in os.walk(src_dir):
            for filename in filenames:
                zip_path_obj.write(os.path.join(parent, filename), filename)
        zip_path_obj.close()
        return True
    except IOError as error:
        print(error)
        return False


def decompression_file_zip(src_file, dst_dir):
    """ 解压文件 """
    if zipfile.is_zipfile(src_file):
        zf = zipfile.ZipFile(src_file, 'r')
        for name in zf.namelist():
            zf.extract(name, dst_dir)
        zf.close()


def move_directory(src_dir, dst_dir):
    """ 移动文件 """
    try:
        create_directory(dst_dir)
        for parent, dirs, filenames in os.walk(src_dir):
            for filename in filenames:
                shutil.move(os.path.join(parent, filename), os.path.join(dst_dir, filename))
        return 1
    except IOError as error:
        print(error)
        return 0


def move_file(src_file, dst_dir):
    """ 移动文件到目录"""
    shutil.move(src_file, dst_dir)


def create_directory(mydir):
    """ 创建目录 """
    if not os.path.isdir(mydir):
        os.makedirs(mydir)


def str_salt_calc_sha1(obj_str):
    """ 字符串加盐sha1 """
    sha1obj = hashlib.sha1()
    sha1obj.update('%s.%s' % (obj_str, YAML_CONFIG['Salt']))
    return sha1obj.hexdigest()


def file_calc_sha1(obj_file_path):
    """ 文件sha1 """
    with open(obj_file_path, 'rb') as obj_file:
        sha1obj = hashlib.sha1()
        sha1obj.update(obj_file.read())
        return sha1obj.hexdigest()
