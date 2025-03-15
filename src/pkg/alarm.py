from typing import Tuple, Union, Dict, List, Any
from src.pkg.base import BaseClass
from src.client.redis_client import RedisClass
from ierror import *
import requests
from src.common.log import log_method
from src.pkg.msgtype import RequestBody

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
        
    @property
    @log_method
    def GetValidAccessToken(self) -> Union[int, str]:
        """
        @return: access_token
        """
        ret = super().KeySelect(self.redis_access_token_key)
        if ret == RedisErrorConn:
            return ret
        if ret == RedisKeyIsNone:
            """
            get key's value is None from redis
            """
            wxgtk = super().GetAccessToken()
            if isinstance(wxgtk, int):
                return wxgtk
            rctkk = super().KeyCreate(self.redis_access_token_key, wxgtk)
            if rctkk != WXSuccess:
                return rctkk
            return wxgtk
        return ret            

    def SendRequestBody(self, url: str, body: Dict[str, Union[str, int, Dict[str, str]]], timeout: int) -> Dict[str, Union[int, str]]:
        send_response = requests.post(
            url=url,
            json=body,
            timeout=timeout
        ).json()
        return send_response

    @log_method
    def SendAlarmRequest(self,
        response_code: Any,
    ) -> Union[int, Dict[str, Any]]:
        """
        @param content: 发送内容
        @param touser: 指定用户接收
        @param toparty: 指定部门接收
        @param totag: 指定标签接收
        @param timeout: 等待服务端响应时间
        @return: 请求body
        """
        
        tk = self.GetValidAccessToken
        if isinstance(tk, int):
            return tk
        rbc = RequestBody(
            100006, 
            ['TianCiwang'], 
            "", 
            "", 
            tk,
        )
        print (rbc.agentid)
        request_body, url = rbc.UpdateCard(response_code)
        print (request_body)
        print (url)
        response = self.SendRequestBody(
            url,
            request_body,
            30
        )
        return response