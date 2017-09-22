from .BaseBlock import BaseBlock
from django.conf import settings
import json
from sklearn.model_selection import train_test_split
import numpy as np

class TrainTest(BaseBlock):
    def __init__(self, data, name="TrainTest", session="", u=0.5):
        self.name = name
        self.session = session
        self.block_num = ""
        self.type = "matrix"
        self.options = ["boxplot", "histogram", "statistics", "scatter","Multiple Regression","normal test"]
        self.vars = []
        self.data = data["data"]
        self.titles = data["titles"]

        self.train, self.test = train_test_split(self.data, train_size=u)

        for title in self.titles:
            i=0
            binary = True
            while i<len(self.train[title]) and binary==True:
                if self.train[title][i]!=0 and self.train[title][i]!=1:
                    binary = False
                else:
                    i+=1
            if binary == False:
                self.vars.append(title)
            else:
                newvar = title + ": Binary"
                self.vars.append(newvar)

    def getData(self):
        #separar train de test per poder triar
        data = {"name":self.name, "type": self.type, "data": self.train, "train_data": self.train, "test_data": self.test, "titles":self.titles, "vars":self.vars}
        return data


    def GetNode(self):
        print("get Train Test Node")
        TT_data = ["Variable Name:", self.name, "Type:", self.type, "Train Dimensions:", str(len(self.train))+"x"+str(len(self.train[0])), "Test Dimensions", str(len(self.test))+"x"+str(len(self.test[0]))]
        data = {"type": "block",
                "block_type": self.type,
                "block_num": self.block_num,
                "content_type": "TT_data",
                "TT_data": TT_data,
                "call_path": settings.CACHE_URL + "/" + self.session + "/" + self.name,
                "options": self.options,
                "vars": self.vars,
                }
        return json.dumps(data)

    #def getOption(self):
        # Choose train or test