import base64
import traceback
from typing import Tuple

from Crypto.Cipher import AES

from src.crypto.base import BaseClass
from ierror import *


class DecryptionClass(BaseClass):
    def __init__(self, cropid: str, aeskey: str, token: str) -> None:
        """
        @param cropid: 企业微信 CropID
        @param aeskey: 企业微信应用 EncodingAESKey
        @param token:  企业微信应用 Token
        """
        super().__init__(cropid, aeskey, token)

    def DecryptRequestEchoStr(self, msg_signature: str) -> Tuple[
        int, Union[bytes, None], Union[Exception, None]]:
        """
        解密 echostr
            (加密的字符串。需要解密得到消息内容明文，解密后有random、msg_len、msg、receiveid四个字段
                msg为消息内容明文
                receivedid为企业微信cropid明文
            )
        @return: 解密后的echostr
            Tuple[int, bytes|None, Exception|None]
        """
        # 使用BASE64对密文进行解密
        ret, base64Key, err = super().AesKeyWithBase64
        if ret != WXSuccess:
            return ret, None, err
        crypt = AES.new(base64Key, self.mode, base64Key[:16])
        try:
            xml_bytes = crypt.decrypt(base64.b64decode(msg_signature))
            return WXSuccess, xml_bytes, None
        except Exception:
            return WXErrorEncodeEchoStr, None, traceback.format_exc()

