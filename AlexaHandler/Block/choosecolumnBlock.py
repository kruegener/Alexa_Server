from .BaseBlock import BaseBlock
from django.conf import settings
import json

class chooseColumn(BaseBlock):
    def __init__(self,data, columns="SOFA", name="chooseColumn", session=""):
        self.name=name
        self.session=session
        self.options=[]
        self.vars=[]

        self.data = data["train_data"]
        self.titles = data["titles"]

        if columns == "sofa":
            self.columns.remove()



