from .BaseBlock import BaseBlock
import json
from channels import Group

class MessageBlock (BaseBlock):

    def __init__(self, name="message", session="", msg=""):
        self.name = name
        self.type = "message"
        self.session = session
        self.msg = msg
        self.options = ["execute", "read"]

    # Node builder
    def GetNode(self):
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "content_type": "text",
                "msg": self.msg,
                "options": self.options,
                }
        return json.dumps(data)

    def executeBlock(self, num):
        data = {"type": "cmd",
                "block_id": num,
                "cmd": "light_up",
                }
        print("executing MessageBlock")
        Group("alexa").send({
            "text": json.dumps(data)
        })

    def readBlock(self):
        print("reading")
        return self.msg