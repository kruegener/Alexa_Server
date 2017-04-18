from .BaseBlock import BaseBlock
import json
from channels import Group

class HistogramBlock (BaseBlock):

    def __init__(self, name="Histogram", session=""):
        self.name = name
        self.type = "histogram"
        self.session = session
        self.options = ["plot"]
        self.cache_path = ""


        # load data
        # from /import


        # make histogram




        # save image to /cache




        # save /cache path in self.cache_path


    # Node builder
    def GetNode(self):
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
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