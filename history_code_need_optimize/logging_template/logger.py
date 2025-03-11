#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:wtc
"""
    Created on 2021/6/10 11:46
"""
import os
import logging

# base_dir = os.path.dirname(os.path.abspath(__file__))+"/logs/"
base_dir = os.path.abspath('')+"/logs/"
if os.path.exists(base_dir):
    pass
else:
    os.mkdir( base_dir, mode=0o755 )
def write_log(name,message):
    """
    日志记录，按月切割
    @param message: 记录日志
    @return:
    """
    log_dir = base_dir + str(time.strftime("%Y-%m")) + "_" + name + ".log"
    name = name
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_dir,encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(message)
    logger.removeHandler(file_handler)
