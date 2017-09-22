from .BaseBlock import BaseBlock
from django.conf import settings
import json
import numpy as np
from sklearn import datasets
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
import matplotlib.pyplot as plt

class MultipleRegression(BaseBlock):
    def __init__(self, data, name="MR", session=""):
        print "inside MR"
        self.name = name
        self.session=session

        self.data = data["train_data"]
        self.titles=data["titles"]


        self.SOFAscore = self.data["ICUSTAY_ADMIT_SOFA"]


        lr = linear_model.LinearRegression()
        model=lr.fit(self.list,self.SOFAscore)

        print(model)




