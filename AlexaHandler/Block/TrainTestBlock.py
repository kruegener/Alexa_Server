from .BaseBlock import BaseBlock
from django.conf import settings
import json
from sklearn.model_selection import train_test_split

class TrainTest(BaseBlock):
    def __init__(self, data, name="TrainTest", session="", u=0.5):
        self.name = name
        self.session = session
        self.block_num = ""
        self.type = "matrix"
        self.options = ["boxplot", "histogram", "statistics"]
        self.vars = ""
        self.data = data["data"]
        self.train, self.test = train_test_split(self.data, train_size=u)

        print (len(self.train), len(self.test))


    def getData(self):
        #separar train de test per poder triar
        data = {"name":self.name, "type": self.type, "data": self.data, "train_data": self.train, "test_data": self.train}
        return data


    def GetNode(self):
        print("get Train Test Node")
        TT_data = ["Variable Name:", self.name, "Type:", self.type, "Train Dimensions:", self.train.shape, "Test Dimensions", self.test.shape]
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