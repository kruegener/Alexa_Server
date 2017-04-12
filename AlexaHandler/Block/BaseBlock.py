class BaseBlock:

    def __init__(self, name="base", type="base", session="", content_type=""):
        self.name = name
        self.type = type
        self.session = session
        self.content_type = content_type

    # name (has to be unique or does it get an id from models?)
    def GetName(self):
        return self.name
    def SetName(self, name):
        self.name = name

    # Session
    def GetSession(self):
        return self.session
    def SetSession(self, session):
        self.name = session

    # type IO/Processing etc.
    def GetType(self):
        return self.type
    def SetType(self, type):
        self.type = type

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
                "text": "",
                }
        return json.dumps(data)

    def delBlock(self):
        del self

    def executeBlock(self):
        # MUST OVERRIDE
        print("execute not defined")

    # str
    def __str__(self):
        return "{0}: type {1}".format(self.name, self.type)