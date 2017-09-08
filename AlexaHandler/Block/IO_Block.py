from .BaseBlock import BaseBlock
import json
import csv
from django.conf import settings
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pylab as pl
from shutil import copyfile
import sys
import os

# make new block right here
from channels import Group
from .. import consumers
from .HistogramBlock import HistogramBlock


class IO_Block(BaseBlock):
    def __init__(self, file_name, name="IO", session="", abs_path=""):
        self.name = name
        self.type = "IO"
        self.session = session
        self.vars = []

        self.file_name = file_name

        #self.vars = [".".join(self.file_name.split(".")[:-1])]
        self.data_name = ".".join(self.file_name.split(".")[:-1])
        self.file_type = ".".join(self.file_name.split(".")[-1:])
        self.display_type = ""
        self.call_path = ""
        self.block_num = ""
        self.options = []

        if abs_path == "":
            self.path = settings.IMPORT_DIR + "/" + self.file_name
        else:
            self.path = abs_path


        print("Inside IO")
        print(self.path)

        if self.file_type in ["csv", "txt", "dat"]:
            self.data = np.genfromtxt(self.path, delimiter=",", dtype=None, names=True)
            self.titles = self.data.dtype.names
            self.display_type = "matrix"
            self.type = "matrix"
            self.options.append("SCATTER")
            self.options.append("PCA")
            self.options.append("PLOT")
            self.options.append("statistics")
            self.options.append("TRAIN/TEST")
            print (self.options)
            print self.data[0]
            print self.data[0]["SUBJECT_ID"]


        elif self.file_type in ["png", "jpg", "jpeg"]:
            self.data = pl.imread(self.path)
            print("loaded")
            self.display_type = "image"
            self.type = "image"
            self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.file_name
            self.call_path = settings.CACHE_URL + "/" + self.session + "/" + self.file_name
            self.options.append("PROCESS")
            self.options.append("SHOW")
            print("copying to cache")
            print("PATHS: ", self.path, self.cache_path)
            try:
                copyfile(self.path, self.cache_path)
            except:
                print("\033[93m Errror importing:", sys.exc_info(), "\033[0m")

        else:
            raise NameError("unsupported format")

        print("read")
        print(self.display_type)

    def getOption(self, para):
        SessChain = consumers.getSessChain()
        if para in "histogram":
            histo = HistogramBlock()
            SessChain.addBlock(histo)
            Group("alexa").send({
                "text": histo.GetNode()
            })
            SessChain.Chain_pickle()
        else:
            raise NameError("wrong option")


    def showBlock(self, num=""):
        print("showBlock");
        if self.type == "image":
            call_path = settings.CACHE_URL + "/" + self.session + "/" + self.file_name
            data = {"type": "cmd",
                    "block_num": num,
                    "cmd": "show",
                    "call_path": call_path,
                    }
            print("executing showPCAblock")
            Group("alexa").send({
                "text": json.dumps(data)
            })
        else:
            raise NameError("Function not available for non-Image IO")

    def getData(self):
        data = {"name": self.data_name, "type": self.file_type, "data": self.data, "titles":self.titles}
        return data

    def getTitles(self):
        return self.titles

    # Node builder
    def GetNode(self):
        print("get IO Node")
        IO_data = ["Variable Name:", self.vars, "Dimensions:", str(len(self.data))+ "x"+ str(len(self.data[0])), "Type:", self.display_type]
        data = {"type": "block",
                "block_type": self.type,
                "block_num": self.block_num,
                "file_name": self.file_name,
                "content_type": "IO_data",
                "IO_data": IO_data,
                "options": self.options,
                "vars": self.vars,
                "call_path": self.call_path,
                }
        return json.dumps(data)

    def delBlock(self):
        try:
            os.remove(self.cache_path)
            print("removed from cache")
        except:
            print("\033[93m couldnt remove image block cache", sys.exc_info(), "\033[0m")

        del self


