class BaseBlock:



    def __init__(self, name="base", type="base", session="", content_type=""):
        self.name = name
        self.type = type
        self.session = session
        self.content_type = content_type
        self.options = ["execute"]


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

    # can be first

    # Alexa Interface

    # Execute Options

    # Content_type


    # Node builder
    def GetNode(self):
        import json
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "content_type": self.content_type,
                "options": self.options,
                }
        return json.dumps(data)

    def delBlock(self):
        del self

    def executeBlock(self, *args):
        # MUST OVERRIDE
        print("execute not defined")

    # str
    def __str__(self):
        return "{0}: type {1}".format(self.name, self.type)