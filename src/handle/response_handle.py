import time
from typing import Tuple, Dict

from src.common.utility import Dict2Obj
from src.crypto.encryption import EncryptionClass
from ierror import *


class ResponseToQYWXHandle:
    def __init__(self, cropid: str, token: str, key: str) -> None:
        """
        @param cropid: 企业微信 cropid
        @param token: 企业微信应用 token
        @param key: 企业微信应用 EncodingAESKey
        """
        self.id = cropid
        self.token = token
        self.key = key
        self.timestamp = str(int(time.time()))
        self.etc = EncryptionClass(self.id, self.key, self.token)

    def EncryptWithBase64Response(self, rspBody: str) -> Tuple[int, Union[bytes, None], Union[Exception, None]]:
        """
        @param rspBody: 明文响应消息
        @return: 编码加密后的响应消息
            Tuple[int, bytes|None, Exception|None]
        """
        ret, xml, err = self.etc.EncryptResponseMsg(rspBody)
        if ret != WXSuccess:
            return ret, None, err
        return ret, xml, None

    def CreateResponseSignature(self, xmlBody: str, nonce: str) -> Tuple[int, Union[str, None], Union[Exception, None]]:
        """
        @param xmlBody:  解码后的密文响应消息
        @param nonce: 随机字符串
        @return: 响应安全签名
            Tuple[int, str|None, Exception|None]
        """
        ret, rsp_signature, err = self.etc.EncryptRequestSignature(self.timestamp, nonce, xmlBody)
        if ret != WXSuccess:
            return ret, None, err
        return ret, rsp_signature, None

    def CreateResponseBody(self, xmlBody: str, signature: str, nonce: str) -> str:
        """
        @param xmlBody: 解码后的密文响应消息
        @param signature: 响应安全签名
        @param nonce: 随机字符串
        @return: 响应消息
        """
        response = self.etc.ResponseBody(xmlBody, signature, self.timestamp, nonce)
        return response


def NewResponseToQYWXHandle(data: Dict[str, str]) -> Tuple[int, Union[str, None], Union[Exception, None]]:
    """
    生成 程序返回的消息
    @param data: 请求参数
    @return: 响应消息
        Tuple[int, str|None, Exception|None]
    """
    data_dict = Dict2Obj(data)
    rtqh = ResponseToQYWXHandle(data_dict.cropid, data_dict.token, data_dict.key)
    ret, encrypt_base64_xml, err = rtqh.EncryptWithBase64Response(data_dict.response)
    if ret != WXSuccess:
        return ret, None, err
    xml_content = encrypt_base64_xml.decode("utf8")
    ret, rsp_signature, err = rtqh.CreateResponseSignature(xml_content, data_dict.nonce)
    if ret != WXSuccess:
        return ret, None, err

    response = rtqh.CreateResponseBody(xml_content, rsp_signature, data_dict.nonce)
    return WXSuccess, response, None
