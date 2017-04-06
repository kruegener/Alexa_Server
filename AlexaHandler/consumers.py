''' making the consumers '''

from channels.handler import AsgiHandler
from channels import Group
# maybe define __all__ in models for private objects/funcs
from AlexaHandler.models import *
import json
from django.forms.models import model_to_dict
from django.db.models.fields.related import ManyToManyField

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data

def ws_message(message):
    print("incoming message: ", message.content['text'])

    data = {"msg" : "[user] %s" % message.content['text'],
            "optional" : 'chat', "type" : "content_update"}

    Group("alexa").send({
        "text": json.dumps(data),
    })

    #Group("alexa").send({
    #    "text": "[user] %s" % message.content['text'],
    #})

def ws_add(message):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})

    # Add them to the chat group (again implement different )
    Group("alexa").add(message.reply_channel)

    # check if session exists (add ?room= ...)
    oldCS = ClientSession.objects.all().filter(SessID='alexa').exists()
    print("NEW: ", oldCS)
    if not oldCS:
        print("new CS")
        CS = ClientSession(SessID = 'alexa')
        CS.save()
    else:
        CS = ClientSession.objects.get(SessID='alexa')
        print("got old CS")

    #data = {"msg" : "jo",
            #"optional" : 'asd'}

    # get Session nodeFlows
    NFs = NodeFlow.objects.filter(Sess = CS).iterator()
    NFs = [nf for nf in NFs]
    # hierarchical NodeFlow node list
    NsI = []
    # non-hierarchical
    Ns = []
    # get Nodes for NodeFlows
    for NF in NFs:
        NsI.append(Node.objects.filter(Flow = NF).iterator())
    # hierarchical Nodes in lists for flows
    NsI = [[to_dict(N) for N in nf] for nf in NsI]
    # all nodes unwrapped, easier to process client side
    for nf in NsI:
        for n in nf:
            Ns.append(n)
    # get SessionVars
    Vars = SessionVar.objects.filter(Sess = CS).iterator()
    Vars = [to_dict(var) for var in Vars]

    print("NodeFlows: ", NFs)
    print("Nodes: ", Ns)
    print("Vars: ", Vars)

    data = {"type": "init",
            "NodeFlows": [to_dict(nf) for nf in NFs],
            "Nodes": Ns,
            "Vars": Vars,
           }
    # get varNames
    message.reply_channel.send({
        "text": json.dumps(data),
    })
    # send reply_channel all variable_names and nodes as JSON


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("alexa").discard(message.reply_channel)
