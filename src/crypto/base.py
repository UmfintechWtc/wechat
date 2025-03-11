import base64
import hashlib
import socket
import struct
import traceback
import xml.etree.cElementTree as ET
from typing import Tuple, List

from Crypto.Cipher import AES

from ierror import *


class BaseClass:
    def __init__(self, cropid: str, aeskey: str, token: str) -> None:
        """
        @param cropid: 企业微信 CropID
        @param aeskey: 企业微信应用 EncodingAESKey
        @param token:  企业微信应用 Token
        """
        self.id = cropid
        self.key = aeskey
        self.token = token
        self.sha = hashlib.sha1()
        self.mode = AES.MODE_CBC
        self.block_size = 32
        self.aes_text_response_template = """
            <xml>
            <Encrypt><![CDATA[%(msg_encrypt)s]]></Encrypt>
            <MsgSignature><![CDATA[%(msg_signaturet)s]]></MsgSignature>
            <TimeStamp>%(timestamp)s</TimeStamp>
            <Nonce><![CDATA[%(nonce)s]]></Nonce>
            </xml>
        """

    @property
    def AesKeyWithBase64(self) -> Tuple[int, Union[bytes, None], Union[Exception, None]]:
        """
        @return: base64 加密后的 EncodingAESKey
            Tuple[int, bytes|None, Exception|None]
        """
        key = base64.b64decode(self.key + "=")
        try:
            assert len(key) == 32
        except AssertionError:
            return WXErrorInvalidAESKey, None, self.key + "\n" + traceback.format_exc()
        return WXSuccess, key, None

    def DelteRandom(self, text: bytes) -> Tuple[int, Union[List[Union[bytes, int]], None], Union[Exception, None]]:
        """
        @param text: 解密后的echostr
        @return: msg_len、msg
            Tuple[int, List|None, Exception|None]
        """
        # 剔除16位随机字符串
        sl = []
        try:
            last_pad = text[-1]
            content = text[16:-last_pad]
            xml_len = socket.ntohl(struct.unpack("I", content[:4])[0])
            sl.append(content)
            sl.append(xml_len)
            return WXSuccess, sl, None
        except Exception:
            return WXErrorDeleteRandom, None, traceback.format_exc()

    def ExtractReadXml(self, text: bytes) -> Tuple[int, Union[bytes, None], Union[Exception, None]]:
        """
        @param text: 解密后的echostr
        @return: msg
            Tuple[int, bytes|None, Exception|None]
        """
        ret, sl, err = self.DelteRandom(text)
        if ret != WXSuccess:
            return ret, None, err
        xml_content = sl[0][4: sl[1] + 4]
        return WXSuccess, xml_content, None

    def ExtractCropID(self, text: bytes) -> Tuple[int, Union[str, None], Union[Exception, None]]:
        """
        @param text: 解密后的echostr
        @return: cropid
            Tuple[int, str|None, Exception|None]
        """
        ret, sl, err = self.DelteRandom(text)
        if ret != WXSuccess:
            return ret, None, err
        cropid = sl[0][sl[1] + 4:]
        return WXSuccess, cropid.decode("utf8"), None

    def ExtractRequestBody(self, data: bytes) -> Tuple[int, Union[str, None], Union[Exception, None]]:
        """

        @param data: 请求body
        @return: 提取数据包中的加密消息
            Tuple[int, str|None, Exception|None]
        """
        try:
            xml_tree = ET.fromstring(data)
            encrypt = xml_tree.find("Encrypt")
        except Exception:
            return WXErrorPostXMLData, None, traceback.format_exc()
        return WXSuccess, encrypt.text, None

    def ResponseBody(self, xml_content: str, signature: str, timestamp: str, nonce: str) -> str:
        """
        @param xml_content: 加密后的响应消息
        @param signature:  安全签名
        @param timestamp: 时间戳
        @param nonce: 随机字符串
        @return: 程序回复响应体
        """
        resp_dict = {
            'msg_encrypt': xml_content,
            'msg_signaturet': signature,
            'timestamp': timestamp,
            'nonce': nonce,
        }
        resp_xml = self.aes_text_response_template % resp_dict
        return resp_xml
