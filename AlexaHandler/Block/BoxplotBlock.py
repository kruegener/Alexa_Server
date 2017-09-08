from .BaseBlock import BaseBlock
import json
import matplotlib as mpl
mpl.use("agg")
import matplotlib.pyplot as plt
from django.conf import settings
from channels import Group

class Boxplot(BaseBlock):
    def __init__(self, data,para="default", session="", name=""):
        self.name = name
        self.type = "plot"
        self.session = session
        self.options = ["show"]
        self.cache_path=""
        self.vars = ""
        self.para = para

        self.data = data["data"]


        fig = plt.figure(1, figsize=(8, 5))
        ax = fig.add_subplot(111)
        if type(self.para) is int:
            self.titles = data["titles"]
            ax.boxplot(self.data[self.titles[self.para]]) #creates boxplot
            ax.set_xlabel(self.titles[para])
        else:
            self.title=data["title"]
            ax.boxplot(self.data)
            ax.set_xlabel(self.title)
        ax.set_ylabel('Mean')

        fig.savefig('cache/alexa/'+self.name+'.png', bbox_inches='tight')
        plt.close()


    def showBlock(self, num=""):
        print("showBlock");
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name +'.png'
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
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name+'.png'
        print call_path
        data = {"type": "block",
                "block_type": self.type,
                #"block_num": self.block_num,
                "content_type": "plot",
                "call_path": call_path,
                "options": self.options,
                "vars": self.vars,
                }
        return json.dumps(data)