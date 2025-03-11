#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:wtc
"""
    Created on 2021/6/10 11:46
"""
import paramiko

class SSHLogin():
    """
        创建ssh登录对象
    """
    def __init__(self,host,user,port,password):
        self.host = host
        self.user = user
        self.password = password
        self.login_Port = port
        self.ssh_conn = paramiko.SSHClient()
        self.ssh_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_conn.connect(hostname=self.host, username=self.user, password=self.password, port=self.login_Port, allow_agent=True)

    def ExecuteCmd(self,command):
        """
        @param command: 需要执行命令
        @return: 执行命令返回结果
        """
        stdin, stdout, stderr = self.ssh_conn.exec_command(command)
        cmd_result = stdout.read().decode()
        return cmd_result
