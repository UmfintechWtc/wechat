from typing import Tuple, Union, Dict, List
from src.pkg.base import BaseClass
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

    def GetValidAccessToken(self) -> Union[int, str, None]:
        """
        @return: access_token
        """
        ret = super().KeySelect(self.redis_access_token_key)
        if not ret:
            """
            redis 未获取到 access_token
            """
            ctk = super().CreateAccessToken()
            if isinstance(ret, int):
                return ret
            return super().KeyCreate(self.redis_access_token_key, ret)         
        else:
            return ret
            

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
        # toparty: Union[str, List[str]],
        # totag: Union[str, List[str]],
        timeout: int = 30,
    ) -> int:
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
            # "toparty": f"{super().CheckSpecialReceiver(toparty)}",
            # "totag": f"{super().CheckSpecialReceiver(totag)}",
            f"{self.msgtype}": {
                "content": content
            },
        }
        ret = self.GetValidAccessToken()
        if ret:
            return ret
        # 发送消息
        try:
            response = self.SendRequestBody(
                super().SendMessageApi(ret),
                request_body,
                timeout
            )
        except Exception:
            return AlarmErrorSend

        # access_token 已过期、无权限，重新创建access_token并重试发送消息
        if response.get("errcode") in self.retry_code:
            ret= super().CreateAccessToken()
            if isinstance(ret, str):
                crk = super().KeyCreate(self.redis_access_token_key, ret)
                if isinstance(crk, int):
                    return ret

            atk = super().KeySelect(self.redis_access_token_key)
            if isinstance(atk, int):
                return atk
            elif isinstance(atk, None):
                return RedisGetKey
            elif isinstance(atk, str):
                atk = atk.decode("utf8")
            print (atk,'!11111111111111111111111111111111111')
            try:
                response = self.SendRequestBody(super().SendMessageApi(atk), request_body, timeout)
            except Exception:
                return AlarmErrorSend
            if response.get("errcode") != 0:
                return AlarmErrorSend
            return WXSuccess
        else:
            if response.get("errcode") != 0:
                return AlarmErrorSend
            return WXSuccess