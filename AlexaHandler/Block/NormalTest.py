from .BaseBlock import BaseBlock
import json
from django.conf import settings
from scipy.stats.mstats import normaltest

class NormalTest(BaseBlock):
    def __init__(self, data, para="", session="alexa", name="NormalTest"):
        self.name = name
        self.session = session
        self.para = para
        self.type = "Normal"
        #self.block_type = "message"
        self.data = data["data"]
        self.type = "message"
        self.vars = ""
        self.options = []

        if type(self.para) is int:
            self.titles = data["titles"]
            self.normal = normaltest(self.data[self.titles[self.para]])
        else:
            self.normal = normaltest(self.data)

        print self.normal

    def GetNode(self):
        data = {"type": "block",
                "block_type": self.type,
                #"block_num": self.block_num,
                "content_type": "Normal",
                "name": self.name,
                "data": self.normal,
                "options": self.options,
                "vars": self.vars,
                }
        return json.dumps(data)


