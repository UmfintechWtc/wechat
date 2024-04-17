from flask import Response, request, Flask, jsonify, make_response
import hashlib

def create_app() -> Flask:
	app = Flask(__name__)
	app.config['JSON_AS_ASCII'] = False

	@app.route("/sign", methods=["GET"])
	def verify_signature():
		print ("tianciwang")
		sVerifyMsgSig = request.args.get('msg_signature')
		sVerifyTimeStamp = request.args.get('timestamp')
		sVerifyNonce = request.args.get('nonce')
		sVerifyEchoStr = request.args.get('echostr')
		print(sVerifyMsgSig, 1)
		print(sVerifyTimeStamp, 2)
		print(sVerifyNonce, 3)
		print(sVerifyEchoStr, 4)
		sortlist = [sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr]
		sortlist.sort()
		sha = hashlib.sha1()
		sha.update("".join(sortlist).encode())
		sha.hexdigest()
		return Response("200", mimetype="text/plain")

	return app
