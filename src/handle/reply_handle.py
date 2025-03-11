import traceback
import xml.etree.cElementTree as ET
from typing import Tuple, Dict

from src.crypto.decryption import DecryptionClass
from src.crypto.encryption import EncryptionClass
from ierror import *


class ReplyMsgWithQYWXHandle:
    def __init__(self,
                 cropid: str,
                 token: str,
                 key: str,
                 signature: str,
                 request_data: bytes,
                 timestamp: str,
                 nonce: str,
                 echo: str) -> None:
        """
        解析企业微信返回的消息
        @param cropid: 企业微信 cropid
        @param token: 企业微信应用 token
        @param key: 企业微信应用 EncodingAESKey
        @param signature: 安全签名
        @param data: 请求body
        @param timestamp: 时间戳
        @param nonce: 随机字符串
        @param echo: 密文
        """
        self.id = cropid
        self.token = token
        self.key = key
        self.request_data = request_data
        self.msg_signature = signature
        self.timestamp = timestamp
        self.nonce = nonce
        self.echostr = echo
        self.dtc = DecryptionClass(self.id, self.key, self.token)
        self.etc = EncryptionClass(self.id, self.key, self.token)

    @property
    def VerifySignature(self) -> Tuple[int, Union[str, None], Union[Exception, None]]:
        """
        @return: 企业微信回复的消息
            Tuple[int, str|None, Exception|None]
        """
        ret, body, err = self.dtc.ExtractRequestBody(self.request_data)
        if ret != WXSuccess:
            return ret, None, err
        ret, signature, err = self.etc.EncryptRequestSignature(self.timestamp, self.nonce, body)
        if ret != WXSuccess:
            return ret, None, err
        if self.msg_signature == signature:
            return WXSuccess, body, None
        return WXErrorInvalidSignature, None, signature + "\n" + traceback.format_exc()

    def VerifyCropID(self, body: str) -> Tuple[int, Union[bytes, None], Union[Exception, None]]:
        """
        @param body: 企业微信请求中的echostr密文
        @return: echostr解密后的msg
            Tuple[int, bytes|None, Exception|None]
        """
        ret, xml_bytes, err = self.dtc.DecryptRequestEchoStr(body)
        if ret != WXSuccess:
            return ret, None, err
        ret, cropid, err = self.dtc.ExtractCropID(xml_bytes)
        if ret != WXSuccess:
            return ret, None, err
        if self.id != cropid:
            return WXErrorInvalidCropID, None, cropid + "\n" + traceback.format_exc()
        ret, xml_text, err = self.dtc.ExtractReadXml(xml_bytes)
        if ret != WXSuccess:
            return ret, None, err
        return WXSuccess, xml_text, None


def NewReplyMsgWithQYWXHandle(data: Dict[str, str]) -> Tuple[int, Union[str, None], Union[Exception, None]]:
    """
    @param data: 请求参数
    @return: 企业微信回复的内容
        Tuple[int, str|None, Exception|None]
    """
    rmqh = ReplyMsgWithQYWXHandle(**data)
    ret, body, err = rmqh.VerifySignature
    if ret != WXSuccess:
        return ret, None, err
    ret, xml_content, err = rmqh.VerifyCropID(body)
    if ret != WXSuccess:
        return ret, None, err
    xml_tree = ET.fromstring(xml_content)
    if "Content" in xml_content.decode("utf8"):
        content = xml_tree.find("Content").text
        return ret, content, None
    else:
        return ret, None, None
