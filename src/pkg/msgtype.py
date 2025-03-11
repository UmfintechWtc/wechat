from collections import defaultdict

class RequestBody:
    def __init__(self, agentid, touser, toparty, totag) -> None:
        self.agentid = agentid
        self.user = touser
        self.party = toparty
        self.tag= totag

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
        return request_body

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
        return request_body