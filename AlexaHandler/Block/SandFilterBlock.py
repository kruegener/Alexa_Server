from .BaseBlock import BaseBlock
import json
from django.conf import settings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
from scipy import ndimage
import os
from channels import Group
from .. import consumers
from .IO_Block import IO_Block

class SandFilterBlock (BaseBlock):
    def __init__(self, var_name, data, name="SandFilter", session=""):
        self.name = var_name + ".Filter"
        self.file_name = var_name + ".Filter.png"
        self.type = "rich_image"
        self.session = session
        self.options = ["sand", "glass", "void"]
        self.vars = []
        self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.file_name
        print("Inside SandFilter")

        self.data = data["data"]

        # local processing
        dat = self.data
        dat = dat[:-60]
        filtdat = ndimage.median_filter(dat, size=(7, 7))
        self.void = filtdat <= 50
        self.sand = np.logical_and(filtdat > 50, filtdat <= 114)
        self.glass = filtdat > 114
        phases = self.void.astype(np.int) + 2 * self.glass.astype(np.int) + 3 * self.sand.astype(np.int)
        plt.imsave(self.cache_path, phases)
        #self.filterParameter("sand")


    def getOption(self, para):
        SessChain = consumers.getSessChain()
        if para == "sand":
            set = self.sand
        elif para == "glass":
            set = self.glass
        elif para == "void":
            set = self.void
        else:
            raise NameError("not a valid option")

        set_op = ndimage.binary_opening(set, iterations=2)
        set_labels, set_nb = ndimage.label(set_op)
        set_areas = np.array(ndimage.sum(set_op, set_labels, np.arange(set_labels.max() + 1)))
        mask = set_areas > 100
        subset = mask[set_labels.ravel()].reshape(set_labels.shape)


        sub_file_name = ".subset." + para + ".jpg"
        further_cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.file_name + sub_file_name
        plt.imsave(further_cache_path, subset)

        IO = IO_Block(sub_file_name, session=self.session, abs_path=further_cache_path)
        SessChain.addBlock(IO)

        Group("alexa").send({
            "text": IO.GetNode()
        })

        SessChain.Chain_pickle()

    def showBlock(self, num=""):
        print("showBlock");
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.file_name
        data = {"type": "cmd",
                "block_id": num,
                "cmd": "show",
                "call_path": call_path,
                }
        print("executing showPCAblock")
        Group("alexa").send({
            "text": json.dumps(data)
        })

    # Node builder
    def GetNode(self):
        print("get Filter Node")
        add_data = [self.name]
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "file_name": self.file_name,
                "content_type": "PCA",
                "call_path": settings.CACHE_URL + "/" + self.session + "/" + self.file_name,
                "add_data": add_data,
                "options": self.options,
                "vars": self.vars,
                }
        return json.dumps(data)

    def delBlock(self):
        try:
            os.remove(self.cache_path)
            print("removed from cache")
        except:
            print("\033[93m couldnt remove image block cache \033[0m")

        del self