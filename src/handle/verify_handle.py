import traceback
from typing import Dict
from typing import Tuple

from src.crypto.decryption import DecryptionClass
from src.crypto.encryption import EncryptionClass
from ierror import *


class VerifyQYWXHandler:
    def __init__(self,
                 cropid: str,
                 token: str,
                 key: str,
                 signature: str,
                 timestamp: str,
                 nonce: str,
                 echo: str) -> None:
        """
        校验企业微信签名、cropid
        @param cropid: 企业微信 cropid
        @param token: 企业微信应用 token
        @param key: 企业微信应用 EncodingAESKey
        @param key: 安全签名
        @param timestamp: 时间戳
        @param nonce: 随机字符串
        @param echo: 密文
        """
        self.id = cropid
        self.token = token
        self.key = key
        self.msg_signature = signature
        self.timestamp = timestamp
        self.nonce = nonce
        self.echostr = echo
        self.dtc = DecryptionClass(self.id, self.key, self.token)
        self.etc = EncryptionClass(self.id, self.key, self.token)

    @property
    def VerifyUrlSignature(self) -> Tuple[int, Union[Exception, None]]:
        """
        校验签名
        @return: 校验签名正确性
            Tuple[int, Exception|None]
        """
        ret, signature, err = self.etc.EncryptRequestSignature(self.timestamp, self.nonce, self.echostr)
        if ret != WXSuccess:
            return ret, err
        if self.msg_signature == signature:
            return WXSuccess, None
        return WXErrorInvalidSignature, signature + "\n" + traceback.format_exc()

    @property
    def VerifyCropID(self) -> Tuple[int, Union[bytes, None], Union[Exception, None]]:
        """
        校验企业微信 CropID
        @return:
            Tuple[int, bytes|None, Exception|None]
        """
        ret, xml_bytes, err = self.dtc.DecryptRequestEchoStr(self.echostr)
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


def NewVerifyQywxHandle(data: Dict[str, str]) -> Tuple[int, Union[bytes, None], Union[Exception, None]]:
    """
    @param data: 请求参数
    @return: 响应企业微信消息体
    """
    vwxh = VerifyQYWXHandler(**data)
    ret, err = vwxh.VerifyUrlSignature
    if ret != WXSuccess:
        return ret, None, err
    ret, xml, err = vwxh.VerifyCropID
    if ret != WXSuccess:
        return ret, None, err
    return ret, xml, None
