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

class SandFilterBlock (BaseBlock):
    def __init__(self, var_name, data, name="SandFilter", session=""):
        self.name = var_name + ".Filter"
        self.file_name = var_name + ".Filter.png"
        self.type = "rich_image"
        self.session = session
        self.options = ["show", "save", "sand"]
        self.vars = []
        self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.file_name
        print("Inside SandFilter")

        self.data = data["data"]

        # local processing
        dat = self.data
        dat = dat[:-60]
        filtdat = ndimage.median_filter(dat, size=(7, 7))
        void = filtdat <= 50
        sand = np.logical_and(filtdat > 50, filtdat <= 114)
        glass = filtdat > 114
        phases = void.astype(np.int) + 2 * glass.astype(np.int) + 3 * sand.astype(np.int)
        plt.imsave(self.cache_path, phases)






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