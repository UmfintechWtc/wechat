from typing import Tuple, Union, Dict, List
from src.alarm.base import BaseClass
from src.client.redis_client import RedisClass
from ierror import *
import requests
import traceback

class AlarmClass(BaseClass, RedisClass):
    def __init__(self, data: Dict[str, Union[str, int]], agentid :int, secret: str, cropid: str, msgtype: str = "text"  ) -> None:
        """
        @param data: redis连接信息
        @param agentid: 企业微信应用 agentid
        @param secret: 企业微信应用 secret
        @param cropid: 企业微信应用 cropid
        @param msgtype: 发送消息类型 text or markdown
        """
        BaseClass.__init__(self, agentid, secret, cropid, msgtype)
        RedisClass.__init__(self, **data)
        self.redis_access_token_key = str(agentid) + "_qywx_app_access_token"
        # https://developer.work.weixin.qq.com/document/path/90313
        self.retry_code = [42001, 301002]

    def GetValidAccessToken(self) -> Tuple[int, Union[Exception, str]]:
        """
        @return: 有效的access_token
        """
        ret, at = super().KeySelect(self.redis_access_token_key)
        if ret != WXSuccess:
            return ret, at
        if isinstance(at, bytes):
            return ret, at.decode("utf8")
        elif isinstance(at, str):
            return ret, at
        elif not at:
            """
            在redis中未获取到access_token的key
            """
            ret, at = super().CreateAccessToken()
            if ret != WXSuccess:
                return ret, at
            ret, err = super().KeyCreate(self.redis_access_token_key, at)
            if ret != WXSuccess:
                return ret, err
            return ret, at

    def SendRequestBody(self, url: str, body: Dict[str, Union[str, int, Dict[str, str]]], timeout: int) -> Dict[str, Union[int, str]]:
        send_response = requests.post(
            url=url,
            json=body,
            timeout=timeout
        ).json()
        return send_response


    def SendAlarmRequest(self,
        content: str,
        touser: Union[str, List[str]],
        toparty: Union[str, List[str]],
        totag: Union[str, List[str]],
        timeout: int = 30,
    ) -> Tuple[int, Union[Exception, str]]:
        """
        @param content: 发送内容
        @param touser: 指定用户接收
        @param toparty: 指定部门接收
        @param totag: 指定标签接收
        @param timeout: 等待服务端响应时间
        @return: 请求body
        """
        request_body = {
            "agentid": self.id,
            "msgtype": self.msgtype,
            "safe": self.safe,
            "touser": f"{super().CheckSpecialReceiver(touser)}",
            "toparty": f"{super().CheckSpecialReceiver(toparty)}",
            "totag": f"{super().CheckSpecialReceiver(totag)}",
            f"{self.msgtype}": {
                "content": content
            },
        }
        ret, at = self.GetValidAccessToken()
        if ret != WXSuccess:
            return ret, at

        # 发送消息
        try:
            response = self.SendRequestBody(
                super().SendMessageApi(at),
                request_body,
                timeout
            )
        except Exception:
            return AlarmErrorSend, str(request_body) + "\n" + traceback.format_exc()

        # access_token 已过期、无权限，重新创建access_token并重试发送消息
        if response.get("errcode") in self.retry_code:
            ret, at = super().CreateAccessToken()
            if ret != WXSuccess:
                return ret, at
            ret, err = super().KeyCreate(self.redis_access_token_key, at)
            if ret != WXSuccess:
                return ret, err
            ret, at = super().KeySelect(self.redis_access_token_key)
            if ret != WXSuccess:
                return ret, at
            if isinstance(at, bytes):
                at = at.decode("utf8")
            elif isinstance(at, str):
                at = at
            try:
                response = self.SendRequestBody(super().SendMessageApi(at), request_body, timeout)
            except Exception:
                return AlarmErrorSend, str(request_body) + "\n" + traceback.format_exc()
            if response.get("errcode") != 0:
                return AlarmErrorSend, response
            return WXSuccess, response
        else:
            if response.get("errcode") != 0:
                return AlarmErrorSend, response
            return WXSuccess, response