from .BaseBlock import BaseBlock



class Outlier(BaseBlock):
    def __init__(self, data, name='Outlier', session=""):
        self.name = name
        self.type = ""
        self.session = session
        self.options = []
        self.vars = []


        self.data = data["data"]
        self.titles = data["titles"]