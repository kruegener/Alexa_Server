from .BaseBlock import BaseBlock
import json
import matplotlib as mpl
mpl.use("agg")
import matplotlib.pyplot as plt
from django.conf import settings


class Boxplot(BaseBlock):
    def __init__(self, data, session="", name=""):
        self.name = name
        self.type = "plot"
        self.session = session
        self.options = ["show"]
        self.cache_path=""
        self.vars = ""


        self.data = data["train_data"]
        print (self.data)

        fig = plt.figure(1, figsize=(9, 6))
        ax = fig.add_subplot(111)
        bp = ax.boxplot(self.data)  #creates boxplot


        fig.savefig('cache/alexa'+self.name+'.png', bbox_inches='tight')
        plt.close()


    def showBlock(self, num=""):
        print("showBlock");
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name
        data = {"type": "cmd",
                "block_num": num,
                "cmd": "show",
                "call_path": call_path,
                }
        Group("alexa").send({
            "text": json.dumps(data)
        })


    def GetNode(self):
        print("get image Node")
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name
        data = {"type": "block",
                "block_type": self.type,
                #"block_num": self.block_num,
                "content_type": "plot",
                "call_path": call_path,
                "options": self.options,
                "vars": self.vars,
                }
        return json.dumps(data)