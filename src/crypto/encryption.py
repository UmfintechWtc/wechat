import base64
import socket
import struct
import traceback
from typing import Tuple

from Crypto.Cipher import AES

from src.common.utility import RandomStr
from src.crypto.base import BaseClass
from ierror import *


class EncryptionClass(BaseClass):
    def __init__(self, cropid: str, aeskey: str, token: str) -> None:
        """
        @param cropid: 企业微信 CropID
        @param aeskey: 企业微信应用 EncodingAESKey
        @param token:  企业微信应用 Token
        """
        super().__init__(cropid, aeskey, token)

    def EncryptRequestSignature(self, timestamp: str, nonce: str, encrypt: str) -> Tuple[
        int, Union[str, None], Union[Exception, None]]:
        """
        @param encrypt: 密文
        @param timestamp: 时间戳
        @param nonce: 随机字符串
        @return: 安全签名
            Tuple[code, signature|None, exception|None]
        """
        ttne = [self.token, timestamp, nonce, encrypt]
        ttne.sort()
        try:
            self.sha.update("".join(ttne).encode())
            return WXSuccess, self.sha.hexdigest(), None
        except Exception:
            return WXErrorInvalidToken, None, traceback.format_exc()

    def EncryptResponseMsg(self, rspBody: str) -> Tuple[int, Union[bytes, None], Union[Exception, None]]:
        """
        @param rspBody: 程序明文响应消息
        @return: 编码后的密文消息
            Tuple[int, bytes|None, Exception|None]
        """
        ret, base64Key, err = super().AesKeyWithBase64
        if ret != WXSuccess:
            return ret, None, err
        rsp_content = rspBody.encode()
        xml_content = RandomStr() + struct.pack("I", socket.htonl(len(rsp_content))) + rsp_content + self.id.encode()
        text_length_length = len(xml_content)
        amount_to_pad = self.block_size - (text_length_length % self.block_size)
        # 计算差异进行补位
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        pad = chr(amount_to_pad)
        xml_content = xml_content + (pad * amount_to_pad).encode()
        cryptos = AES.new(base64Key, self.mode, base64Key[:16])
        try:
            ciphertext = cryptos.encrypt(xml_content)
            # 使用BASE64对加密后的字符串进行编码
            return WXSuccess, base64.b64encode(ciphertext), None
        except Exception:
            return WXErrorEncodeReplyMsg, None, traceback.format_exc()
