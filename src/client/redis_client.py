import redis
import traceback
from typing import Any, Tuple, Union
from ierror import *
from datetime import timedelta
from src.common.log import log_method

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
        self.ping = self.Ping

    @property
    @log_method
    def Ping(self) -> bool:
        """
        @return: redis conn status. True or False
        """
        return self.conn.ping()
    
    @log_method
    def KeySelect(self, key: str) -> Union[str, int]:
        """
        @param key: redis key.
        @return: key's value. 
        """
        if not self.ping:
            return RedisErrorConn
        value = self.conn.get(key)
        return value.decode("utf8") if value else RedisKeyIsNone
                        
    def KeyTTL(self, key: str) -> Tuple[int, Any]:
        """
        @param key: select target key ttl
        @return: ttl
        """
        try:
            value = self.conn.ttl(key)
            return WXSuccess, value
        except redis.exceptions.TimeoutError:
            return RedisErrorConn, traceback.format_exc()
        except redis.exceptions.RedisError:
            return RedisErrorTTLKey, traceback.format_exc()

    def KeyCreate(self, key: str, value: Any, ttl: Union[int, timedelta] = 7200) -> int:
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
            return WXSuccess
        except redis.exceptions.RedisError:
            return RedisErrorSetKey