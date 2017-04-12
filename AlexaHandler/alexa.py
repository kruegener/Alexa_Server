from __future__ import absolute_import
from django_alexa.api import fields, intent, ResponseBuilder

from AlexaHandler.models import Person

from channels import Group

import json

# Importing Alexa Functionality from Block Module
from .Block import Alexa

@intent(slots=None, app="AlexaHandler")
def LaunchRequest(session):
    """
    B 2 S Lab is a go
    ---
    Launch
    """

    return ResponseBuilder.create_response(message="open",
                                           reprompt="",
                                           end_session=False,
                                           launched=True)

@intent(slots=None, app="AlexaHandler")
def AddFileRequest(session):
    """
    File
    ---
    TEST
    """

    if "Test" in str(Person.objects.get(first_name__icontains="Test")):
        print("YAY")
        p = Person.objects.filter(first_name="Test").first()
        p.save_and_file("File1")
    else:
        p = Person(first_name="Test1")
        print("Request: ", p)
        p.save_and_file("File1")
    

    return ResponseBuilder.create_response(message="TEST!",
                                           reprompt="TEST!",
                                           end_session=False,
                                           launched=True)


NAMES = Person.objects.all()
print("NAMES: ", NAMES)

class Name(fields.AmazonSlots):
    name = fields.AmazonCustom(label="NAMES", choices=NAMES)

@intent(slots=Name, app="AlexaHandler")
def SetName(session, name="default"):
    """
    requesting the name
    ---
    my name is {name}
    {name}
    """

    NAMES = Person.objects.all()
    kwargs = {}
    if name in NAMES:
        kwargs['message'] = "Welcome back {0}!".format(name)
        msg = "Welcome back {0}!".format(name)
    else:
        kwargs['message'] = "So you are {0}. Haven't seen you before! Let's add you to the List.".format(name)
        msg = "Welcome back {0}!".format(name)
        p = Person(first_name=name)
        p.save()
        print("saved: ", name)

    data = {"msg" : msg,
            "optional" : 'JSON information'}

    Group("alexa").send({
        "text": json.dumps(data),
    })

    if session.get('launched'):
        kwargs['reprompt'] = "Try again."
        kwargs['end_session'] = False
        kwargs['launched'] = session['launched']
    return ResponseBuilder.create_response(**kwargs)