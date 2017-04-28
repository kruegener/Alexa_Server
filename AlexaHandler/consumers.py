''' making the consumers '''
from __future__ import print_function
from channels import Group
# maybe define __all__ in models for private objects/funcs
from .models import *
import json
import time
from django.db.models.fields.related import ManyToManyField


# TODO enforced ordering
from channels.sessions import channel_session, enforce_ordering
from channels.auth import channel_session_user, channel_session_user_from_http
# block Import
from .Block.MessageBlock import MessageBlock
from .Block.ImageBlock import ImageBlock
from .Block.HistogramBlock import HistogramBlock
from .Block.BlockChain import BlockChain
import pickle

SessChain = "init"

# TODO not really using this anymore
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
    # TODO if more than one Session not feasible
    global SessChain
    data = json.loads(message.content['text'])
    # print("JSON: ", data, "DATA: ", message.content['text'])
    if data['type'] == "msg" :
        block = MessageBlock(name="[user] ",
                             session="alexa",
                             msg=data['msg'])
        # add to Chain
        SessChain.addBlock(block)
        # send to group
        Group("alexa").send({
            "text": block.GetNode()
        })
        print("\033[95m BLOCK \033[0m", block)

    elif data["type"] == "histogram":
        block = HistogramBlock(name="Histogram", session="alexa")
        # add to Chain
        SessChain.addBlock(block)
        Group("alexa").send({
            "text": block.GetNode()
        })

    elif data['type'] == "command" :
        # print(data['cmd'], file = sys.stderr)
        if data['cmd'] == "del_all":
            SessChain.delBlocksAll()
            data = {"type": "cmd",
                    "cmd": "reset"}
            Group("alexa").send({
                "text": json.dumps(data)
            })

        elif data['cmd'] == "init":
            print("init config ordered")
            # artificial sleep to show off loading
            time.sleep(1)
            # serve BlockChain Contents to client
            if SessChain.getBlockListLength() != 0:
                for block in SessChain.getBlockList():
                    message.reply_channel.send({
                        "text": block.GetNode()
                    })
            else:
                data = {"type": "cmd",
                        "cmd": "init_done"}
                message.reply_channel.send({
                    "text": json.dumps(data)
                })

        elif data['cmd'] == "img":
            print("img ordered")
            block = ImageBlock(name="test.jpg",
                                 session="alexa",
                                 img_path="/home/alexa_server/Alexa_Server/import/test.jpg")
            # add to Chain
            SessChain.addBlock(block)
            # send to group
            Group("alexa").send({
                "text": block.GetNode()
            })
            print("\033[95m BLOCK \033[0m", block)

        elif data['cmd'] == "alexa":
            print("alexa called")

        elif data['cmd'] == "click":
            print("\033[95m CLICK \033[0m")
            print(data['num'], data['opt'])
            if data['opt'] == 'show':
                SessChain.getBlock(data['num']).showBlock(data['num'])
            if data['opt'] == 'execute':
                SessChain.getBlock(data['num']).executeBlock(data['num'])
            # needs active alexa session
            # TODO derive better system to add functions here automatically
            #if data['opt'] == 'read':
            #    msg = SessChain.getBlock(data['num']).readBlock(data['num'])


    # "autosave"
    SessChain.Chain_pickle()

def addBlock(block):
    global SessChain
    # add to Chain
    SessChain.addBlock(block)
    # send to group
    Group("alexa").send({
        "text": block.GetNode()
    })
    print("\033[95m BLOCK \033[0m", block)

    # "autosave"
    SessChain.Chain_pickle()


def ws_add(message):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})

    # Add them to the chat group (again implement different )
    Group("alexa").add(message.reply_channel)
    # TODO: change when more than one Session
    global SessChain

    # boolean
    oldSess = BlockChainModel.objects.all().filter(Sess='alexa').exists()
    print("Old Session: ", oldSess)

    # Generating new Blockchain, looking up in active variables or from pickle_cache

    if not oldSess:
        print("new Session")
        # TODO pickle field
        SessModel = BlockChainModel(name = "alexa", Sess = 'alexa', pickle="cache/alexa/alexa.p")
        SessModel.save()
        SessChain = BlockChain(name="alexa", session="alexa")
        print(SessChain)
    else:

        SessModel = BlockChainModel.objects.get(Sess='alexa')

        try:
            SessChain
            # first step in session handling
            if type(SessChain) != BlockChain:
                SessChain = pickle.load(open(SessModel.pickle, "rb"))
        except NameError:
            print("\033[92m reload from Cache \033[0m")
            SessChain = pickle.load(open(SessModel.pickle, "rb"))
            print(SessChain)
        else:
            print("\033[92m was already in active memory \033[0m")

        print(SessModel)
        print("got old Session")
        print(SessChain)

    # TODO: add timestamp, because if server reboots, the whole thing is sent again
    data = {"type": "cmd",
            "cmd": "ready"}
    message.reply_channel.send({"text": json.dumps(data)})
    print("\033[94m ready sent \033[0m")

# Connected to websocket.disconnect
def ws_disconnect(message):
    # TODO implement longer timeout (say days) or put a timestamp check in the exchanged data
    Group("alexa").discard(message.reply_channel)


# alexa / session wrapper
def getSessChain():

    global SessChain

    try:
        SessChain
        return SessChain
    except NameError:
        print("\033[91m SessChain currently not defined \033[0m")
