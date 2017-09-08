from .BaseBlock import BaseBlock
from django.conf import settings
import json

class ComparePatients(BaseBlock):
    def __init__(self,data,title, para1,para2="", session="alexa", name="ViewPatient"):
        self.para1 = para1
        self.session = session
        self.name = name
        self.options = []
        self.vars = []
        self.data = data["data"]
        self.titles = data["titles"]
        self.type = "message"

        self.para1=para1
        self.para2=para2
        self.title=self.titles[title]

        n=0
        self.patient=[]
        self.id = []
        count=0
        found = False
        while found==False:
            if self.data[n]["SUBJECT_ID"] == self.para1 or self.data[n]["SUBJECT_ID"] == self.para2:
                self.patient = self.patient + [self.data[n][self.title]]
                self.id= self.id + [self.data[n]["SUBJECT_ID"]]
                count+=1
            n+=1
            if count == 2:
                found = True

        self.patientA=self.patient[0]
        self.patientB=self.patient[-1]



    def GetNode(self):
         data ={"type": "block",
                "block_type": self.type,
                "content_type": "Patient",
                "data": self.patient,
                "call_path": settings.CACHE_URL + "/" + self.session + "/" + self.name,
                "options": self.options,
                "vars": self.vars,
               }
         return json.dumps(data)

    def getData(self):
        data = {"data": self.data, "patients": self.patient, "title":self.title, "IDs": self.id}






