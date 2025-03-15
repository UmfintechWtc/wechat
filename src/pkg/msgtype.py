from collections import defaultdict

class RequestBody:
    def __init__(self, agentid, touser, toparty, totag, access_token) -> None:
        self.agentid = agentid
        self.user = touser
        self.party = toparty
        self.tag= totag
        self.tk = access_token
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
        self.template_base_url = "https://qyapi.weixin.qq.com/cgi-bin/message/update_template_card?access_token="
        self.send_url = self.base_url + self.tk
        self.tempalte_update_url = self.template_base_url + self.tk

    def Text(self, content):
        request_body = {
            "agentid": self.agentid,
            "msgtype": "text",
            "safe": 0,
            "touser": self.user,
            "toparty": self.party,
            "totag": self.tag,
            "text": {
                "content": content
            },
        }
        return request_body, self.send_url

    def Markdown(self, content):
        request_body = {
            "agentid": self.agentid,
            "msgtype": "markdown",
            "touser": self.user,
            "toparty": self.party,
            "totag": self.tag,
            "markdown": {
                "content": content
            },
        }
        return request_body, self.send_url

    def TemplateCard(self, content):
        request_body = {
            "agentid": self.agentid,
            "msgtype": "template_card",
            "touser": self.user,
            "toparty": self.party,
            "totag": self.tag,
            "template_card": content
        }
        return request_body, self.send_url
    
    def UpdateCard(self, response_code):
        request_body = {
            "userids" : ["TianCiwang"],
            "atall" : 0,
            "agentid" : 1000006,
            "response_code": response_code,
            "button":{
                "replace_name": "woosa已忽略"
            }
        }
        return request_body, self.tempalte_update_url