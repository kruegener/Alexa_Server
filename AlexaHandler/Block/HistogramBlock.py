from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import matplotlib
import os
matplotlib.use("Agg")
import matplotlib.pyplot as plot

from django.conf import settings

class HistogramBlock (BaseBlock):

    def __init__(self, name="Histogram", session=""):
        self.name = name
        self.type = "histogram"
        self.session = session
        self.options = ["plot", "show"]
        self.cache_path = ""
        self.vars = ["data table"]
        self.block_num = ""

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

        #plot.cla()
        #plot.clf()
        fig = plot.figure()
        plot.hist(a, bins=30)
        plot.xlabel('protein numbers')
        print("saving")
        plot.savefig("cache/alexa/plot.png")
        self.name = "plot.png"
        plot.close()

        # save /cache path in self.cache_path

    def showBlock(self, num=""):
        print("showBlock");
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name
        data = {"type": "cmd",
                "block_num": num,
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
                "block_num": self.block_num,
                "content_type": "image",
                "call_path": call_path,
                "options": self.options,
                "vars": self.vars,
                }
        return json.dumps(data)

    def executeBlock(self, num):
        data = {"type": "cmd",
                "block_num": num,
                "cmd": "light_up",
                }
        print("executing MessageBlock")
        Group("alexa").send({
            "text": json.dumps(data)
        })

    def delBlock(self):
        try:
            os.remove(self.cache_path)
            print("removed from cache")
        except:
            print("\033[93m couldnt remove image block cache \033[0m")

        del self