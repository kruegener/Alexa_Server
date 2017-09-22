from .BaseBlock import BaseBlock
from django.conf import settings
import json

class SOFABlock(BaseBlock):
    def __init__(self, data, subject="", name="SOFA",session=""):
        self.name = name
        self.session=session
        self.subject=subject

        self.titles=data["titles"]
        self.data=data["test_data"]






