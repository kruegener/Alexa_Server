import os
from shutil import copyfile


class BaseBlock:

    def __init__(self, name="base", type="base", session="", content_type=""):
        self.name = name
        self.type = type
        self.session = session
        self.content_type = content_type
        self.options = ["execute"]
        self.vars = []
        self.block_num = ""


    # name (has to be unique or does it get an id from models?)
    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name

    # Session
    def getSession(self):
        return self.session
    def setSession(self, session):
        self.name = session

    # type IO/Processing etc.
    def getType(self):
        return self.type
    def setType(self, type):
        self.type = type

    def getOptions(self):
        return self.options
    def addOption(self, s):
        self.options.append(s)



    # Node builder
    def GetNode(self):
        import json
        data = {"type": "block",
                "block_type": self.type,
                "block_num": self.block_num,
                "content_type": self.content_type,
                "options": self.options,
                "vars": self.vars,
                }
        return json.dumps(data)

    def delBlock(self):
        del self

    def executeBlock(self, *args):
        # MUST OVERRIDE
        print("execute not defined")

    def getData(self):
        pass

    def save(self):
        path = "/home/alexa_server/Alexa_Server/export/" + self.session + "/"
        # checking if dir already exists
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            copyfile(self.cache_path, path + self.file_name)
        except:
            print("\033[93m ERROR exporting file \033[0m")
        print("exporting", self.name)

    # str
    def __str__(self):
        return "{0}: type {1}".format(self.name, self.type)