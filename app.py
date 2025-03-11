from flask import request, Flask, jsonify
from ierror import *
from src.handle.reply_handle import NewReplyMsgWithQYWXHandle
from src.handle.response_handle import NewResponseToQYWXHandle
from src.handle.verify_handle import NewVerifyQywxHandle
from src.pkg.alarm import AlarmClass
from src.common.log import XLogger
from src.config.wechat_config import Config


def Msg(content: str):
    msg = (
        "<xml>"
        "<ToUserName><![CDATA[消息接收人]]></ToUserName>"
        "<FromUserName><![CDATA[CropID]]></FromUserName>"
        "<CreateTime>创建时间</CreateTime>"
        "<MsgType><![CDATA[text]]></MsgType>"
        f"<Content><![CDATA[{content}]]></Content></xml>"
    )
    return msg


def openapi(config: Config) -> Flask:
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    @app.route("/sign", methods=["GET", "POST"])
    def verify_signature():
        args = {
            "token": config.qywx.application.openapi.token,
            "key": config.qywx.application.openapi.key,
            "cropid": config.qywx.cropid,
            "signature": request.args.get('msg_signature'),
            "timestamp": request.args.get('timestamp'),
            "nonce": request.args.get('nonce'),
            "echo": request.args.get('echostr'),
        }
        if request.method == "GET":
            ret, xml_content, err = NewVerifyQywxHandle(args)
            if ret != WXSuccess:
                XLogger().fatal(CustomException(ret, err))
            XLogger().info(CustomException(WXSuccess))
            return xml_content

        if request.method == "POST":
            args["request_data"] = request.data
            ret, content, err = NewReplyMsgWithQYWXHandle(args)
            if ret != WXSuccess:
                XLogger().fatal(CustomException(ret, err))
            if content:
                if content == "tianciwang":
                    replyMsg = "tianciwang"
                    msg = Msg(replyMsg)
                else:
                    msg = Msg(f"Unknown operation type:  {content}")
                args["response"] = msg
                ret, response, err = NewResponseToQYWXHandle(args)
                if ret != WXSuccess:
                    XLogger().fatal(CustomException(ret, err))
                else:
                    return response
            else:
                return "200"

    return app


def alarm(config: Config) -> Flask:
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    @app.route('/alarm', methods=['POST'])
    def http_alarm():
        _response = None
        from src.common.utility import Dict2Obj
        body = Dict2Obj(request.json)
        if not body.agentid:
            _response = jsonify(ResponseBody(AlarmErrorAgentId))

        if not body.secret:
            _response = jsonify(ResponseBody(AlarmErrorSecret))

        if not body.receiver:
            _response = jsonify(ResponseBody(AlarmErrorReceiver))

        if not body.receiver.touser:
            _response = jsonify(ResponseBody(AlarmErrorToAim))

        if body.msgtype and body.msgtype not in ["text", "markdown"]:
            _response = jsonify(ResponseBody(AlarmErrorMsgType))

        if _response:
            XLogger().error(f"{request.remote_addr} - {request.method} - {request.json} - {_response.json}")
            return _response, 400

        XLogger().info(f"{request.remote_addr} - {request.method} - {request.json}")
        alarm = AlarmClass(
            dict(config.redis.map_),
            body.agentid,
            body.secret,
            config.qywx.cropid,
            "text" if not body.msgtype else body.msgtype
        )

        rsp = alarm.SendAlarmRequest(
            body.content if body.content else "Hi, thanks for using qywx alarm",
            body.receiver.touser if body.receiver.touser else "",
            body.receiver.toparty if body.receiver.toparty else "",
            body.receiver.totag if body.receiver.totag else ""
        )
        if isinstance(rsp, int):
            return jsonify(str(CustomException(rsp))), 500
        return jsonify(rsp), 200

    return app
