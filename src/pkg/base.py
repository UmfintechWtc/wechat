import requests
from typing import Tuple, Union, Dict, List
import traceback
from ierror import *

class BaseClass:
    def __init__(self, id: int, secret: str, cropid: str, msgtype: str , safe: int = 0) -> None:
        """
        Reference: https://developer.work.weixin.qq.com/document/path/90236#%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89
        @param id: 企业微信应用 agentid
        @param secret: 企业微信应用 secret
        @param cropid: 企业微信 cropid
        @param msgtype: 消息类型
        @param safe: 消息是否加密
        """
        self.url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={cropid}&corpsecret={secret}"
        self.send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
        self.redis_access_token_key = "qywx_app_access_token"
        self.msgtype = msgtype
        self.safe = safe
        self.id = id
        self.special_receiver = "@all"

    def GetAccessToken(self, timeout: int = 30) -> Union[str, int]:
        """
        @return: access_token
        """
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
        if isinstance(receiver, str):
            return  receiver
        elif isinstance(receiver, list):
            if self.special_receiver in receiver:
                return  self.special_receiver
            else:
                return "|".join(map(lambda x: str(x), receiver))

    def SendMessageApi(self, at: str) -> str:
        """
        @param at: access_token
        @return: 企业微信发送消息API接口
        """
        url = self.send_url + at
        return url
