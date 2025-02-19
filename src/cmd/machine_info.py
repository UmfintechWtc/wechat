import traceback
import subprocess
from fabric import Connection
from typing import List, Dict, Union

# 创建 SSH 连接
class FabricConnection:
    _conn = None

    def __init__(self, host: str, user: str, password = str, port: int = 22):
        if FabricConnection._conn is None:
            FabricConnection._conn = Connection(
                host = host,
                user = user,
                port = port,
                connect_kwargs = {
                    'password': password
                }
            )
        self.ssh = FabricConnection._conn

    def disconnect(self):
        """
        关闭 SSH 连接
        """
        if self.ssh:
            self.ssh.close()

    def execute_command(self, command):
        """
        执行远程命令并捕获输出
        """
        result = self.ssh.run(command)
        print ("111111111111111111")
        return result.stdout  # 返回命令的标准输出



