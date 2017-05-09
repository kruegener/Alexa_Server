from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings

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


        self.data = data
        self.x = []
        self.y = []
        for row in data:
            self.x.append(row[0])
            self.y.append(row[1])

        #fit_fn = np.poly1d(fit)
        plt.scatter(self.x, self.y, color='g')

        plt.savefig(self.cache_path)
        plt.close()


    def GetNode(self):
        print("get LR Node")
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.file_name
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "file_name": self.file_name,
                "content_type": "image",
                "call_path": call_path,
                "options": self.options,
                "vars": self.vars,
                 }
        return json.dumps(data)


    def showBlock(self, num=""):
        print("showBlock")
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.file_name
        data = {"type": "cmd",
                "block_id": num,
                "cmd": "show",
                "call_path": call_path,
                }
        print("executing showImageBlock")
        Group("alexa").send({
            "text": json.dumps(data)
        })





