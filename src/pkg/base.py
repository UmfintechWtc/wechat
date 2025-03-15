import requests
from typing import Tuple, Union, Dict, List
from src.common.const import QYWX_APPLICATION_ACCESS_TOKEN
from ierror import *

class BaseClass:
    def __init__(self, id: int, secret: str, cropid: str, msgtype : str = "text") -> None:
        """
        Reference: https://developer.work.weixin.qq.com/document/path/90236#%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89
        @param id: 企业微信应用 agentid
        @param secret: 企业微信应用 secret
        @param cropid: 企业微信 cropid
        @param msgtype: 消息类型
        """
        self.url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={cropid}&corpsecret={secret}"
        self.redis_access_token_key = QYWX_APPLICATION_ACCESS_TOKEN
        self.msgtype = msgtype
        self.id = id
        self.special_receiver = "@all"

    def GetAccessToken(self, timeout: int = 30) -> Union[str, int]:
        """
        @return: access_token
        """
        print ("get access token", url)
        try:
            response = requests.get(
                self.url,
                timeout = timeout,
            )
            return response.json()["access_token"]
        except Exception:
            return WXErrorAccessToken

    def CheckSpecialReceiver(self, receiver: Union[str, List[str]]) -> str:
        """
        @param receiver: 接收消息对象
        @return: 校验后的接收对象
        """
        if len(receiver) == 0:
            return ""
        elif isinstance(receiver, str):
            return  receiver
        elif isinstance(receiver, list) and self.special_receiver in receiver:
            return  self.special_receiver
        else:
            return "|".join(map(lambda x: str(x), receiver))