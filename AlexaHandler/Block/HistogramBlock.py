from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import matplotlib.pyplot as plot
from django.conf import settings

class HistogramBlock (BaseBlock):

    def __init__(self, name="Histogram", session=""):
        self.name = name
        self.type = "histogram"
        self.session = session
        self.options = ["plot"]
        self.cache_path = ""


        # load data
        # from /import

        #make histogram
        file = open('import/firstdata.csv', 'rb')
        reader = csv.reader(file)
        a = []
        for row in reader:
            for e in row:
                if e == '':
                    pass
                else:
                    a.append(int(e))

        plot.hist(a, bins=30)
        plot.xlabel('protein numbers')
        print("saving")
        plot.savefig("cache/alexa/plot.png")
        self.name = "plot.png"


        # save /cache path in self.cache_path

    def showBlock(self, num=""):
        print("showBlock");
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name
        data = {"type": "cmd",
                "block_id": num,
                "cmd": "show",
                "call_path": call_path,
                }
        print("executing showImageBlock")
        Group("alexa").send({
            "text": json.dumps(data)
        })

    # Node builder
    def GetNode(self):
        #if not self.cached:
        #    self.makeCached()
        print("get image Node")
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "content_type": "image",
                "call_path": call_path,
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