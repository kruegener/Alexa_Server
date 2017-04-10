from .BaseBlock import BaseBlock

class MessageBlock (BaseBlock):

    def __init__(self, name="message", session="", msg=""):
        self.name = name
        self.type = "message"
        self.session = session
        self.msg = msg

    # Node builder
    def GetNode(self):
        import json
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "content_type": "text",
                "msg": self.msg,
                }
        return json.dumps(data)