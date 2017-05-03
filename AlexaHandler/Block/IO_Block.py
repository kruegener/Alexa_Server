from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
from django.conf import settings
import numpy as np

class IO_Block (BaseBlock):
    def __init__(self, file_name, name="IO", session=""):
        self.name = name
        self.type = "IO"
        self.session = session
        self.file_name = file_name
        self.options = ["plot", "PCA"]
        self.vars = [".".join(self.file_name.split(".")[:-1])]
        self.data_name = ".".join(self.file_name.split(".")[:-1])

        path = settings.IMPORT_DIR + "/" + self.file_name
        print("Inside IO")
        # if .csv then delimter =","
        # if .txt then delimter =" "
        self.data = np.genfromtxt(path, delimiter=",")
        print(self.data)
        print("read")


    def getData(self):
        data = {"name": self.data_name, "type": "matrix", "data": self.data}
        return data

    # Node builder
    def GetNode(self):
        print("get IO Node")
        IO_data = ["Variable Name:", self.vars, "Dimensions:", self.data.shape, "Type:", "Matrix"]
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "file_name": self.file_name,
                "content_type": "IO_data",
                "IO_data": IO_data,
                "options": self.options,
                "vars": self.vars,
                }
        return json.dumps(data)