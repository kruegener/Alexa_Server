from .BaseBlock import BaseBlock
import json
from channels import Group
import csv
from django.conf import settings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

class PCA_Block (BaseBlock):
    def __init__(self, var_name, data, name="PCA", session=""):
        self.name = var_name + ".PCA.png"
        self.type = "plot"
        self.session = session
        self.options = []
        self.vars = []
        self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.name
        print("Inside PCA")

        self.data = data
        fig = plt.figure(1, figsize=(8, 6))
        X_reduced = PCA(n_components=2).fit_transform(self.data)
        plt.scatter(X_reduced[:, 0], X_reduced[:, 1],
                   cmap=plt.cm.Paired)
        # plt.set_title("First two PCA directions")

        plt.savefig(self.cache_path)
        # plt.set_xlabel("1st eigenvector")
        # plt.set_ylabel("2nd eigenvector")
        print(self.data)

    def getData(self):
        return self.data

    # Node builder
    def GetNode(self):
        print("get IO Node")
        add_data = ["more info:", "info"]
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "file_name": self.name,
                "content_type": "PCA",
                "call_path": settings.CACHE_URL + "/" + self.session + "/" + self.name,
                "add_data": add_data,
                "options": self.options,
                "vars": self.vars,
                }
        return json.dumps(data)