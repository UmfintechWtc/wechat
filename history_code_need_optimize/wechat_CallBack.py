#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:wtc
"""
    Created on 2021/7/9 15:19
"""
import hashlib
import history_code_need_optimize.ierror as ierror
import xml.etree.cElementTree as et
from flask import Flask,request
from history_code_need_optimize.WXBizMsgCrypt3 import WXBizMsgCrypt
from check_host_information.tcp_port import *
from ssh_login_template.SSHLogin import *
# http://tcandyj.top:8888/sms

app = Flask(__name__)
@app.route('/sms',methods=['GET','POST'])
def sms():
    """
    @return: 消息体签名校验
    """
    sToken = '*'
    sEncodingAESKey = '*'
    sCorpID = '*'
    wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
    sVerifyMsgSig = request.args.get('msg_signature')
    sVerifyTimeStamp = request.args.get('timestamp')
    sVerifyNonce = request.args.get('nonce')
    sVerifyEchoStr = request.args.get('echostr')
    # 验证url
    if request.method == "GET":
        return_api_status, return_sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        if return_api_status == 0 :
            return return_sEchoStr
        else:
            print ("ERR: VerifyURL ret: " + str(return_api_status))
            exit()
    # 接口客户端消息，并触发事件
    if request.method == "POST":
        ret, sMsg = wxcpt.DecryptMsg(request.data, sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce)
        xml_tree = et.fromstring(sMsg)
        content = xml_tree.find("Content").text
        if content == "检测端口":
            cmd_result = check_tcp_port_PG()
            print (cmd_result)
        else:
            cmd_result = "执行失败"
        # 企业微信将触发事件结果返回给客户端(https://work.weixin.qq.com/api/doc/90000/90135/90241)
        sRespData = "<xml>" \
                    "<ToUserName><![CDATA[消息接收人]]></ToUserName>" \
                    "<FromUserName><![CDATA[CropID]]></FromUserName>" \
                    "<CreateTime>创建时间</CreateTime>" \
                    "<MsgType><![CDATA[text]]></MsgType>" \
                    "<Content><![CDATA[{}]]></Content></xml>".format(cmd_result)
        ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, sVerifyNonce, sVerifyTimeStamp)
        return sEncryptMsg

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=80)

