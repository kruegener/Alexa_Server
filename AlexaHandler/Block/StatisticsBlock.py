from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import statistics as stat




class StatisticsBlock(BaseBlock):
    def __init__(self, data, name="Statistics", session="", msg = ""):
        self.name = name
        self.type = "message"
        self.session = session
        self.options = ["read"]
        self.vars =[]
        self.cache_path = ""
        self.msg = msg


        self.data = data
        column = []
        mean = []
        median = []
        mode = []
        stdev = []
        variance = []
        index = 0
        while index < 4:
            for e in data:
                column.append(e[index])

            mean += stat.mean(column)
            median += stat.median(column)
            mode += stat.mode(column)
            stdev += stat.pstdev(column)
            variance += stat.pvariance(column)
            index += 1
        print mean, median, mode, variance




    def getData(self):
        return self.data


    def GetNode(self):
        print("get Statistics Node")
        Stats_data = ["Variable Name: ", self.name, "Means : ", mean, "Medians : ", median, "Modes : ", mode, "Standard deviations : ", stdev, "Variances : ", variance]
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "file_name": self.name,
                "content_type": "Stats_data",
                "Stats_data": Stats_data,
                "options": self.options,
                "vars": self.vars,
                    }
        return json.dumps(data)



    def readBlock(self):
        print("reading")
        return self.msg





