from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import statistics as stat




class StatisticsBlock(BaseBlock):
    def __init__(self, data, para="all", name="Statistics", session=""):
        self.name = name
        self.type = "stat"
        self.session = session
        self.options = ["read","show"]
        self.vars =[]
        self.cache_path = ""
        self.para = para


        self.data = data["data"]
        self.column = []
        self.mean = []
        self.median = []
        self.mode = []
        self.stdev = []
        self.variance = []

        if type(self.para) is int:
            for row in self.data:
                self.column.append(float(row[para]))
            self.mean.append("%.2f" % stat.mean(self.column))
            self.median.append("%.2f" % stat.median(self.column))
            self.mode.append("%.2f" % stat.mode(self.column))
            self.stdev.append("%.2f" % stat.pstdev(self.column))
            self.variance.append("%.2f" % stat.pvariance(self.column))


        else:
            index = 0
            while index < len(self.data[0]):
                for row in self.data:
                            self.column.append(float(row[index]))
                self.mean.append("%.2f" % stat.mean(self.column))
                self.median.append("%.2f" % stat.median(self.column))
                self.mode.append("%.2f" % stat.mode(self.column))
                self.stdev.append("%.2f" % stat.pstdev(self.column))
                self.variance.append("%.2f" % stat.pvariance(self.column))
                index += 1
        print self.mean, self.median, self.mode, self.variance


    def GetNode(self):
        print("get Statistics Node")
        if type(self.para) is int:
            Stats_data = ["Variable Name: ", self.name, "Column :", self.para, "Mean : ", self.mean, "Median : ", self.median, "Mode : ", self.mode, "Standard deviation : ", self.stdev, "Variance :", self.variance ]
        else:
            Stats_data = ["Variable Name: ", self.name, "Means : ", self.mean, "Medians : ", self.median, "Modes : ", self.mode, "Standard deviations : ", self.stdev, "Variances : ", self.variance]
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "file_name": self.name,
                "content_type": "stats_data",
                "Stats_data": Stats_data,
                "options": self.options,
                "para": self.para,
                "vars": self.vars,
                 }
        return json.dumps(data)






