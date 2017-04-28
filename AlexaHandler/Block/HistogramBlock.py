from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shutil import copyfile
from django.conf import settings

class HistogramBlock (BaseBlock):

    def __init__(self, name="Histogram", session=""):
        self.name = name
        self.type = "histogram"
        self.session = session
        self.options = ["plot", "show", "export"]
        self.cache_path = ""


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
        plt.hist(a, bins=30)
        plt.xlabel('protein numbers')
        print("saving")
        fig1 = plt.gcf()
        fig1.savefig("cache/alexa/plot.png", bbox_inches='tight', dpi=100)
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
        print("executing HistogramBlock")
        Group("alexa").send({
            "text": json.dumps(data)
        })


    def export(self):
        cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.name   #"/home/ignacio/Alexa_Server/cache/alexa/plot.png"
        export_path = settings.EXPORT_DIR + "/" + self.session + "/" + self.name  #"/home/ignacio/Alexa_Server/export/alexa/plot.png"

        copyfile(cache_path, export_path)










