from .BaseBlock import BaseBlock
import os
from shutil import copyfile
from django.conf import settings

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
        path = settings.CACHE_DIR + "/" + self.session
        file_name = self.img_path.rsplit('/', 1)[1]
        print("filename: ", file_name)
        new_path = path + "/" + file_name
        print("copying to cache")
        # TODO check if filename alreay exists
        print("PATHS: ", self.img_path, new_path)
        try:
            copyfile(self.img_path, new_path)
        except:
            print("ERROR importing file")
        self.cached = True
        self.img_path = new_path


    def export(self):
        path = "/home/alexa_server/Alexa_Server/export/" + self.session
        # checking if dir already exists
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = self.img_path.rsplit('/', 1)[1]
        try:
            copyfile(self.img_path, path + self.name)
        except:
            print("ERROR exporting file")
        print("exporting", self.name)


    def delBlock(self):
        try:
            os.remove(self.img_path)
            print("removed from cache")
        except:
            print("couldnt remove image block cache")

        del self

    # Node builder
    def GetNode(self):
        if not self.cached:
            self.makeCached()
        print("get image Node")
        import json
        call_path = settings.CACHE_URL + "/" + self.session + "/" + self.name
        data = {"type": "block",
                "block_type": self.type,
                "block_id": self.name,
                "content_type": "image",
                "call_path": call_path,
                }
        return json.dumps(data)