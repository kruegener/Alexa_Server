from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
from django.conf import settings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
from sklearn.decomposition import PCA
import os
from shutil import copyfile

class PCA_Block (BaseBlock):
    def __init__(self, var_name, data, name="PCA", session=""):
        self.name = var_name + ".PCA"
        self.file_name = var_name + ".PCA.png"
        self.type = "rich_image"
        self.session = session
        self.options = ["show larger", "save"]
        self.vars = []
        self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.file_name
        self.block_num = ""
        print("Inside PCA")

        self.data = data["data"]
        pca = PCA()
        X_reduced = pca.fit_transform(self.data)
        self.vars.append(self.name)

        plt.cla()
        plt.clf()
        fig = plt.figure(num=None, figsize=(20, 10), edgecolor='k')
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
        plt.subplot(gs[0])
        plt.scatter(X_reduced[:, 0], X_reduced[:, 1],
                    cmap=plt.cm.Paired)
        plt.xlabel("PC1", fontweight='bold', fontsize=20)
        plt.ylabel("PC2", fontweight='bold', fontsize=20)
        plt.title("First 2 Principal Components", fontweight='bold', fontsize=20)
        plt.grid(True)

        plt.subplot(gs[1])
        cumsum = plt.plot(np.cumsum(pca.explained_variance_ratio_))
        plt.setp(cumsum, linewidth=5)
        plt.xlabel("Number of principal components", fontweight='bold', fontsize=20)
        plt.ylim(0,1)
        plt.ylabel("% cummulative Variance explained", fontweight='bold', fontsize=20)
        plt.title("")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(self.cache_path)
        plt.close()

        print("PCA done")

    def getData(self):
        data = {"name": self.data_name, "type": self.file_type, "data": self.data}
        return data

    def showBlock(self, num=""):
        print("showBlock");
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

    # Node builder
    def GetNode(self):
        print("get IO Node")
        add_data = [self.name]
        data = {"type": "block",
                "block_type": self.type,
                "block_num": self.block_num,
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