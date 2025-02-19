import redis
import traceback
from typing import Any, Tuple, Union
from ierror import *
from datetime import timedelta


class RedisClass:
    _pool = None

    def __init__(self, host: str, port: int, password: str = None, db: str = "0", socket_timeout: int = 5,
                 socket_connect_timeout: int = 10, max_connections: int = 30):
        """
        @param host: redis 主机地址
        @param port: redis 端口
        @param password: redis密码
        @param db: redis 库
        @param socket_timeout: 请求redis等待响应时长，默认 5s
        @param socket_connect_timeout: 建立redis连接等待时长，默认10s
        @param max_connections: redis连接池，默认 30
        """
        if RedisClass._pool is None:
            RedisClass._pool = redis.ConnectionPool(
                host=host,
                port=port,
                password=password,
                db=db,
                socket_timeout=socket_timeout,
                socket_connect_timeout=socket_connect_timeout,
                max_connections=max_connections
            )
        self.conn = redis.Redis(connection_pool=RedisClass._pool, decode_responses=True)

    def Ping(self) -> Tuple[int, Union[Exception, bool]]:
        """
        @return: Redis 状态检测结果
            True is ok
        """
        try:
            value = self.conn.ping()
            return WXSuccess, value
        except redis.exceptions.TimeoutError:
            return RedisErrorConn, traceback.format_exc()
        except redis.exceptions.RedisError:
            return RedisErrorPing, traceback.format_exc()

    def KeySelect(self, key: str) -> Tuple[int, Any]:
        """
        @param key: 查询的目标key
        @return: key的value
            key not exists: None
        """
        try:
            value = self.conn.get(key)
            return WXSuccess, value
        except redis.exceptions.TimeoutError:
            return RedisErrorConn, traceback.format_exc()
        except redis.exceptions.RedisError:
            return RedisErrorGetkey, traceback.format_exc()

    def KeyTTL(self, key: str) -> Tuple[int, Any]:
        """
        @param key: 查询的目标key
        @return: key的存活时长
            key not exists: -2
        """
        try:
            value = self.conn.ttl(key)
            return WXSuccess, value
        except redis.exceptions.TimeoutError:
            return RedisErrorConn, traceback.format_exc()
        except redis.exceptions.RedisError:
            return RedisErrorTTLKey, traceback.format_exc()

    def KeyDelete(self):
        pass

    def KeyCreate(self, key: str, value: Any, ttl: Union[int, timedelta] = 7200) -> Tuple[int, Union[Exception, None]]:
        """
        @param key: 创建的目标key
        @param value: key的value
        @param ttl: key的存活时长
        @return: key创建结果
        """
        try:
            self.conn.set(
                name=key,
                value=value,
                ex=ttl
            )
            return WXSuccess, None
        except redis.exceptions.TimeoutError:
            return RedisErrorConn, traceback.format_exc()
        except redis.exceptions.RedisError:
            return RedisErrorSetKey, key + "\n" + traceback.format_exc()