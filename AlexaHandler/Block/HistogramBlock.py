from .BaseBlock import BaseBlock
import json
from channels import Group
import matplotlib
import os
matplotlib.use("Agg")
import matplotlib.pyplot as plot
from shutil import copyfile
from django.conf import settings

class HistogramBlock (BaseBlock):

    def __init__(self, data,para="default", name="Histogram", session=""):
        self.name = name
        self.type = "plot"
        self.session = session
        self.options = ["show","Test normality"]
        self.cache_path = ""
        self.vars = [""]
        self.block_num = ""
        self.data = data["data"]
        self.para = para


        #plot.cla()
        #plot.clf()
        if type(self.para) is int:
            self.titles = data["titles"]
            #fig = plot.figure()
            print "inside int"
            self.data = self.data[self.titles[self.para]]
            plot.hist(self.data, bins=30)
            plot.xlabel(self.titles[self.para])
        elif self.para == "default":
            print "inside default"
            self.title = data["title"]
            print self.title
            plot.hist(self.data, bins=30)
            plot.xlabel(self.title)
        print("saving")
        plot.savefig("cache/alexa/"+self.name)
        plot.close()

        # save /cache path in self.cache_path

    def showBlock(self, num=""):
        print("showBlock");
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name +'.png'
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
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name +'.png'
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
        print("executing HistogramBlock")
        Group("alexa").send({
            "text": json.dumps(data)
        })

    def getData(self):
        data = {"name":self.name, "type":self.type, "data":self.data}
        return data

    def export(self):
        cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.name   #"/home/ignacio/Alexa_Server/cache/alexa/plot.png"
        export_path = settings.EXPORT_DIR + "/" + self.session + "/" + self.name  #"/home/ignacio/Alexa_Server/export/alexa/plot.png"

        copyfile(cache_path, export_path)


    def delBlock(self):
        try:
            os.remove(self.cache_path)
            print("removed from cache")
        except:
            print("\033[93m couldnt remove image block cache \033[0m")

        del self