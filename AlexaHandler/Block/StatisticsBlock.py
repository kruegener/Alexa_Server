from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
import statistics as stat

class StatisticsBlock (BaseBlock):
    def __init__(self, data, para="all", name="Statistics", session=""):
        self.name = name
        self.type = "stat"
        self.session = session
        self.options = ["histogram", "boxplot", "scatter", "max", "min"]
        self.vars =[]
        self.cache_path = ""
        self.para = para


        self.data = data["data"]
        self.titles = data["titles"]
        self.column = []
        self.mean = []
        self.median = []
        self.mode = []
        self.stdev = []
        self.variance = []

        if type(self.para) is int:
            self.column = self.data[self.titles[self.para]]
            self.mean.append("%.2f" % stat.mean(self.column))
            self.median.append("%.2f" % stat.median(self.column))
            self.mode.append("%.2f" % stat.mode(self.column))
            self.stdev.append("%.2f" % stat.pstdev(self.column))
            self.variance.append("%.2f" % stat.pvariance(self.column))
            self.maxvalue = max(self.column)
            self.minvalue = min(self.column)
        # else:
        #     for title in self.titles:
        #         i = 0
        #         binary = True
        #         while i < len(self.data[title]) and binary==True:
        #             if self.data[title][i] != 0. and self.data[title][i] != 1.:
        #                 binary = False
        #             else:
        #                 i+=1
        #         if binary == False:
        #             self.column = self.data[title]
        #             self.mean.append("%.2f" % stat.mean(self.column))
        #             self.median.append("%.2f" % stat.median(self.column))
        #             self.mode.append("%.2f" % stat.mode(self.column))
        #             self.stdev.append("%.2f" % stat.pstdev(self.column))
        #             self.variance.append("%.2f" % stat.pvariance(self.column))


    def GetNode(self):
        print("get Statistics Node")
        if type(self.para) is int:
            Stats_data = ["Variable Name: ", self.name, "Column :", str(self.para) + ": "+self.titles[self.para], "Mean : ", self.mean, "Median : ", self.median, "Mode : ", self.mode, "Standard deviation : ", self.stdev, "Variance :", self.variance, "MAX :", self.maxvalue, "MIN :", self.minvalue ]
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

    def getData(self):
        data = {"name":self.name, "type": self.type,"bigdata":self.data, "data": self.data[self.titles[self.para]],"titles": self.titles, "title": self.titles[self.para]}
        return data







