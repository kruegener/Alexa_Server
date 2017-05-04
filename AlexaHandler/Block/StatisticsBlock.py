from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import statistics as stat




class StatisticsBlock(BaseBlock):
    def __init__(self, data, name="Statistics", session="", msg = ""):
        self.name = name
        self.type = "stat"
        self.session = session
        self.options = ["read"]
        self.vars =[]
        self.cache_path = ""
        self.msg = msg


        self.data = data
        self.column = []
        self.mean = []
        self.median = []
        self.mode = []
        self.stdev = []
        self.variance = []
        index = 0
        while index < 4:
            for e in data:
                self.column.append(float(e[index]))

            self.mean.append("%.2f" % stat.mean(self.column))
            self.median.append("%.2f" % stat.median(self.column))
            self.mode.append("%.2f" % stat.mode(self.column))
            self.stdev.append("%.2f" % stat.pstdev(self.column))
            self.variance.append("%.2f" % stat.pvariance(self.column))
            index += 1
        print self.mean, self.median, self.mode, self.variance




    def getData(self):
        return self.data


    def GetNode(self):
        print("get Statistics Node")
        Stats_data = ["Variable Name: ", self.name, "Means : ", self.mean, "Medians : ", self.median, "Modes : ", self.mode, "Standard deviations : ", self.stdev, "Variances : ", self.variance]
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "file_name": self.name,
                "content_type": "Stats_data",
                "Stats_data": Stats_data,
                "options": self.options,
                "msg": self.msg,
                "vars": self.vars,
                 }
        return json.dumps(data)



    def readBlock(self):
        print("reading")
        return self.msg





