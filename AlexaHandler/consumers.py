''' making the consumers '''

from channels.handler import AsgiHandler
from channels import Group
# maybe define __all__ in models for private objects/funcs
from AlexaHandler.models import *
import json
from django.forms.models import model_to_dict
from django.db.models.fields.related import ManyToManyField

from .Block.BlockChain import *

import pickle

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
    global SessChain
    block = MessageBlock(name="[user] " + str(message.reply_channel),
                         session="alexa",
                         msg=message.content['text'])
    # add to Chain
    SessChain.addBlock(block)
    # "autosave"
    SessChain.Chain_pickle()

    print("BLOCK", block)
    #pickle.dump(block, open("cache/block.p", "wb"), -1)
    Group("alexa").send({
        "text": block.GetNode()
    })


def ws_add(message):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})

    # Add them to the chat group (again implement different )
    Group("alexa").add(message.reply_channel)
    # TODO: change when more than one Session
    global SessChain

    # boolean
    oldSess = BlockChainModel.objects.all().filter(Sess='alexa').exists()
    print("New: ", oldSess)

    # Generating new Blockchain, looking up in active variables or from pickle_cache

    if not oldSess:
        print("new Session")
        SessModel = BlockChainModel(name = "alexa", Sess = 'alexa', pickle="cache/alexa.p")
        SessModel.save()
        SessChain = BlockChain(name="alexa", session="alexa")
        print(SessChain)
    else:

        SessModel = BlockChainModel.objects.get(Sess='alexa')

        try:
            SessChain
        except NameError:
            print("reload from Cache")
            SessChain = pickle.load(open(SessModel.pickle, "rb"))
            print(SessChain)
        else:
            print("was already in active memory")

        print(SessModel)
        print("got old Session")
        print(SessChain)


    # serve BlockChain Contents to client

    for block in SessChain.getBlockList():
        Group("alexa").send({
            "text": block.GetNode()
        })


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("alexa").discard(message.reply_channel)
