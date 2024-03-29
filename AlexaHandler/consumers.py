''' making the consumers '''
from __future__ import print_function
from channels import Group
# maybe define __all__ in models for private objects/funcs
from .models import *
import json
import time
from django.db.models.fields.related import ManyToManyField

from django.conf import settings
from django.core.cache import cache

# import watchdog
from os import listdir
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# TODO enforced ordering
from channels.sessions import channel_session, enforce_ordering
from channels.auth import channel_session_user, channel_session_user_from_http
# block Import
from .Block.MessageBlock import MessageBlock
from .Block.ImageBlock import ImageBlock
from .Block.HistogramBlock import HistogramBlock


from .Block.BlockChain import BlockChain
import pickle
import sched

SessChain = "init"
# initial fileList
fileList = listdir(settings.IMPORT_DIR)
# monitoring import folder

class Event(LoggingEventHandler):
    def on_any_event(self, event):
        global fileList
        fileList = listdir(settings.IMPORT_DIR)
        data = {"type": "cmd",
                "cmd": "file_list_update",
                "files": fileList}
        Group("alexa").send({
            "text": json.dumps(data)
        })

logging.basicConfig(level=logging.INFO,
                        format='\033[1;33m %(asctime)s - %(message)s \033[0m',
                        datefmt='%Y-%m-%d %H:%M:%S')
event_handler = Event()
observer = Observer()
observer.schedule(event_handler, settings.IMPORT_DIR, recursive=True)
observer.start()


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
    global fileList

    from .Block.IO_Block import IO_Block

    if SessChain == "init" or SessChain is None:
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(type(SessChain))
        print("loading from cache for message")
        oldT = time.time()
        SessChain = cache.get("alexa", "doesn't exist")
        if SessChain == "doesn't exist":
            SessChain = BlockChain(name="alexa", session="alexa")
            print("\033[93m made a new session \033[0m")
        print("done after: ", (time.time() - oldT), "seconds")
        print(type(SessChain))
        print("Session:", SessChain)

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

    elif data['type'] == "cmd" :
        if data['cmd'] == "reset":
            SessChain.delBlocksAll()
            data = {"type": "cmd",
                    "cmd": "reset"}
            Group("alexa").send({
                "text": json.dumps(data)
            })

        elif data['cmd'] == "init":
            print("init config ordered")
            # artificial sleep to show off loading
            # time.sleep(1)
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

            # send import list
            data = {"type": "cmd",
                    "cmd": "file_list",
                    "files": fileList}
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
            if "show" in str(data['opt']):
                SessChain.getBlock(data['num']).showBlock(data['num'])
            elif data['opt'] == 'execute':
                SessChain.getBlock(data['num']).executeBlock(data['num'])
            elif "del" in str(data['opt']):
                print("deleting:", data['num'])
                SessChain.delBlockByIndex(data['num'])
                data = {"type": "cmd",
                        "cmd": "del_block",
                        "block_num": data['num']}
                Group("alexa").send({
                    "text": json.dumps(data)
                })

        elif data['cmd'] == "load":
            IO = IO_Block(file_name=data['file'], session="alexa")
            print("NEW IO BLOCK")
            SessChain.addBlock(IO)
            print("IO added")
            Group("alexa").send({
                "text": IO.GetNode()
            })

        elif data['cmd'] == "minimize":
            data = {"type": "cmd",
                    "cmd": "minimize",
                    }
            Group("alexa").send({
                "text": json.dumps(data)
            })

        # needs active alexa session
        # TODO derive better system to add functions here automatically
        #if data['opt'] == 'read':
        #    msg = SessChain.getBlock(data['num']).readBlock(data['num'])


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
        SessModel = BlockChainModel(name = "alexa", Sess = 'alexa')
        SessModel.save()
        SessChain = BlockChain(name="alexa", session="alexa")
        cache.set("alexa", SessChain)
        print(SessChain)
    else:
        SessModel = BlockChainModel.objects.get(Sess='alexa')

        # first step in session handling
        if SessChain == "init":
            oldT = time.time()
            SessChain = cache.get("alexa", "not_loaded")
            if SessChain == "not_loaded":
                SessChain = BlockChain(name="alexa", session="alexa")
                # pickle.load(settings.CACHE_DIR + "session_save.p")
            print("\033[92m reload from Cache \033[0m")
            print("done after: ", (time.time() - oldT), "seconds")
            print(SessChain)
        else:
            print("\033[92mwas in active memory \033[0m")
            print("Session:", SessChain)

        print(SessModel)
        print("got old Session")
        print("Session:", SessChain)

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

    if SessChain != "init":
        return SessChain
    else:
        try:
            print("getSessChain loading:")
            oldT = time.time()
            SessChain = cache.get("alexa")
            print("done after: ", (time.time() - oldT), "seconds")
            return SessChain
        except NameError("getSessChain Error"):
            print("\033[91m SessChain currently not defined \033[0m")

# alexa / session wrapper
def getFileList():
    global fileList
    try:
        return fileList
    except NameError:
        print("\033[91m FileList currently not defined \033[0m")

def AlexaActive():
    print("\033[91m New Session \033[0m")
    data = {"type": "cmd",
            "cmd": "listening"}
    Group("alexa").send({
        "text": json.dumps(data)
    })

def AlexaEnded():
    print("\033[91m Session Ended \033[0m")
    data = {"type": "cmd",
            "cmd": "stopped_listening",
            }
    Group("alexa").send({
        "text": json.dumps(data)
    })

# periodic saving
# s = sched.scheduler(time.time, time.sleep)
# def save_cache(sc):
#     print("auto-saving")
#     oldT = time.time()
#     pickle.dump(SessChain, open(settings.CACHE_DIR + "session_save.p", "wb"))
#     print("done after: ", (time.time() - oldT), "seconds")
#     s.enter(60, 1, save_cache, (sc,))
#
# s.enter(60, 1, save_cache, (s,))
# s.run()