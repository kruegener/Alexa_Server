from .BaseBlock import BaseBlock
import os

class ImageBlock(BaseBlock):

    # TODO: cant pickle file objects -> only import the files to the cache and dont load them
    def __init__(self, name="image", session="", img_path=""):
        self.name = name
        self.type = "image"
        self.session = session
        self.img_path = img_path
        #self.img = open(img_path, "wb")
        self.cached = False
        self.makeCached()

    def setImgPath(self, img_path):
        self.img_path = img_path
    def getImgPath(self):
        return self.img_path


    def makeCached(self):
        # TODO make cache dir static variable in manage.py
        path = "/home/alexa_server/Alexa_Server/cache/" + self.session
        file_name = self.img_path.rsplit('/', 1)[1]
        print("filename: ", file_name)
        new_path = path + "/" + file_name
        print("copying to cache")
        # TODO directories not working
        print("PATHS: ", self.img_path, new_path)
        os.rename(self.img_path, new_path)
        self.cached = True
        self.img_path = new_path


    def export(self):
        path = "/home/alexa_server/Alexa_Server/export/" + self.session
        # checking if dir already exists
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = self.img_path.rsplit('/', 1)[1]
        os.rename(self.img_path, path + file_name)
        print("exporting", self.name)

    # Node builder
    def GetNode(self):
        if not self.cached:
            self.makeCached()

        import json
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "content_type": "image",
                "img_path": self.img_path,
                }
        return json.dumps(data)