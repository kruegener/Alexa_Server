from .BaseBlock import BaseBlock
import numpy as np


class Outlier(BaseBlock):
    def __init__(self, data, parameter = "SOFA", name='Outlier', session=""):
        self.name = name
        self.type = ""
        self.session = session
        self.options = []
        self.vars = []
        self.para=parameter

        self.titles = data["titles"]

        if "train_data" in data:
            self.data = data["train_data"]
        else:
            self.data = data["data"]

        if self.para == "SOFA":
            sofalist = []






