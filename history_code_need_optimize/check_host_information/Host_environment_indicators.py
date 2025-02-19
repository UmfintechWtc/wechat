#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:wtc
"""
    Created on 2021/7/10 11:31
"""

import os
import re

tcp_port_dict={}
cmd_tcp_port_list = os.popen("netstat -tnlp").readlines()

def check_tcp_port_PG():
    """
    @return: 返回目标服务器进程号\t进程ID\tcp端口
    """
    return_res = '{:<15}'.format("PG_ID")+'{:<15}'.format("PG_NAME")+'{:<15}'.format("TCP_PORT")
    for tcp_item in cmd_tcp_port_list[2:]:
        tmp_tcp_item = re.sub(r'\s+', ' ', tcp_item.strip()).split(" ")
        tcp_port = re.sub(r'.*:', '', tmp_tcp_item[3])
        tcp_port_PG_info = tmp_tcp_item[-1]
        progress_name = tcp_port_PG_info.split("/")[1]
        progress_id = tcp_port_PG_info.split("/")[0]
        return_res += "\n" + ('{:<15}'.format(progress_id)+'{:<15}'.format(progress_name)+'{:<15}'.format(tcp_port))
    return return_res
