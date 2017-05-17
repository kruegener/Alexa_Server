from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings
from .. import consumers

class LinearRegressionBlock(BaseBlock):

    def __init__(self, data, name="Linear Regression", session="", **kwargs):
        self.name = name
        self.var_name = "scatter"
        self.session = session
        self.type = "LR"
        self.options = ["show", "regression line"]
        self.vars = []
        self.file_name = self.var_name + ".LR.png"
        self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.file_name
        self.update = "false"
        self.sub_file_name = ""

        self.block_num = "2"

        self.data = data["data"]
        self.x = []
        self.y = []
        for row in self.data:
            self.x.append(row[0])
            self.y.append(row[3])

        #fit_fn = np.poly1d(fit)
        plt.scatter(self.x, self.y, color='g')

        plt.savefig(self.cache_path)
        plt.close()


    def GetNode(self):
        print("get LR Node")
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.file_name
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
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.file_name
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
            m, n = np.polyfit(self.x, self.y, 1)
            plt.scatter(self.x, self.y, color='g')
            new_x = [m*x+n for x in self.x]
            plt.plot(self.x, new_x, '-', color='b')
            print(m, n)

            self.var_name = para
            self.file_name = self.var_name + '.LR.png'
            self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.file_name
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




