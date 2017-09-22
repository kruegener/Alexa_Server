from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.stats import pearsonr
from django.conf import settings
from .. import consumers

class Scatterplot(BaseBlock):

    def __init__(self, data, var1="", var2="", name="Scatterplot", session="", **kwargs):
        self.name = name
        self.var_name = "scatterplot"
        self.session = session
        self.type = "plot"
        self.options = ["show", "regression line"]
        self.vars = []
        self.file_name = self.var_name + ".png"
        self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.name + '.png'
        self.update = "false"

        self.block_num = ''

        if type(var1) is  int and type(var2) is int:
            self.data = data["data"]
            self.titles = data["titles"]
            self.var1 = var1
            self.var2 = var2
            self.x = self.data[self.titles[self.var1]]
            self.y = self.data[self.titles[self.var2]]
            plt.xlabel(self.titles[self.var1])
            plt.ylabel(self.titles[self.var2])
        else:
            self.data=data["bigdata"]
            self.titles = data["titles"]
            self.title=data["title"]
            self.var1=var1
            self.var2 = var2
            print self.var2
            self.x = data["data"]
            self.y = self.data[self.titles[self.var2]]
            plt.xlabel(self.title)
            plt.ylabel(self.titles[self.var2])

        plt.scatter(self.x, self.y, color='g')
        plt.savefig(self.cache_path)
        plt.close()


    def GetNode(self):
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name + '.png'
        data = {"type": "block",
                "block_type": self.type,
                "block_num": self.block_num,
                "file_name": self.file_name,
                "content_type": "image",
                "call_path": call_path,
                "options": self.options,
                "vars": self.vars,
                "update": self.update,
                 }
        return json.dumps(data)


    def showBlock(self, num=""):
        print("showBlock")
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name + '.png'
        data = {"type": "cmd",
                "block_num": num,
                "cmd": "show",
                "call_path": call_path,
                }
        print("executing showImageBlock")
        Group("alexa").send({
            "text": json.dumps(data)
        })


    def getOption(self, para, number):
        SessChain = consumers.getSessChain()

        if para == "regression":
            if type(self.var1) is int and type(self.var2) is int:
                m, n = np.polyfit(self.x, self.y, 1)
                plt.scatter(self.x, self.y, color='g')
                new_x = [m*x+n for x in self.x]
                plt.plot(self.x, new_x, '-', color='b')
                plt.xlabel(self.titles[self.var1])
                plt.ylabel(self.titles[self.var2])
                pearson = "Pearson Corr: " + str(pearsonr(self.x, self.y)[0])
                plt.text(200,20,pearson)
                print(m, n)
            else:
                m, n = np.polyfit(self.x, self.y, 1)
                plt.scatter(self.x, self.y, color='g')
                new_x = [m * x + n for x in self.x]
                plt.plot(self.x, new_x, '-', color='b')
                plt.xlabel(self.title)
                plt.ylabel(self.titles[self.var2])
                pearson = "Pearson Corr: " + str(pearsonr(self.x, self.y)[0])
                plt.text(200, 20, pearson)
                print(m, n)

            self.name = self.name + '.'+para
            # self.file_name = self.var_name + '.LR.png'
            self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.name + '.png'
            plt.savefig(self.cache_path)
            plt.close()

            self.options = ["show"]
            self.update = "true"
            self.block_num = number

            Group("alexa").send({
                "text": self.GetNode()
            })

            # reset state
            self.update = "false"

            SessChain.Chain_pickle()


        else:
            raise NameError("not a valid option")

    def getData(self):
        data = {"name": self.name, "type": self.type, "data": self.data}
        return data




