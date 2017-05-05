# django-alexa imports
from django_alexa.api import fields, intent, ResponseBuilder
# BlockChain import for SessChain Handling
from .BlockChain import BlockChain
from .IO_Block import IO_Block
from .PCA_Block import PCA_Block
from .SandFilterBlock import SandFilterBlock
from channels import Group
from .. import consumers
import sys
import json

# ALEXA PART


@intent(slots=None, app="AlexaHandler")
def LaunchRequest(session):
    """
    B 2 S Lab is a go
    ---
    Launch
    """
    consumers.AlexaActive()
    return ResponseBuilder.create_response(message="open",
                                           reprompt="",
                                           end_session=False,
                                           launched=True)


@intent(app="AlexaHandler")
def SessionEndedRequest(**kwargs):
    """
    Default End Session Intent
    ---
    quit
    end
    """
    print("End called")
    consumers.AlexaEnded()
    return ResponseBuilder.create_response()

# define slots
class Num(fields.AmazonSlots):
    num = fields.AmazonNumber()

OPTIONS = ["sand", "glass", "void", "histogram"]

class OPT(fields.AmazonSlots):
    alexa_option = fields.AmazonCustom(label="OPTIONS", choices=OPTIONS)
    number = fields.AmazonNumber()

# define intents
# execution Intent
@intent(slots=Num, app="AlexaHandler")
def executeBlock(session, num=0):
    """
        executing the block with number X
        ---
        execute block {num}
        execute {num}
        {num} execute
        execute
    """
    print("woop", num)
    SessChain = consumers.getSessChain()

    print("inside BLOCK: ")
    print(SessChain)

    if type(num) is int:
        if num < SessChain.getBlockListLength():
            try:
                SessChain.getBlock(num).executeBlock(num)
                msg = "Executed block " + str(num)
            except:
                msg = "Function not available for block " + str(num)
        else:
            msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength() - 1)

    else:
        msg = "Executed last block"
        print("\033[94m Amazon provided " + str(type(num)) + " type \033[0m")
        SessChain.getBlock(-1).executeBlock(SessChain.getBlockListLength()-1)

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)

# open new tab with image intent
@intent(slots=Num, app="AlexaHandler")
def showImg(session, num=0):
    """
        showing the block with number X in new tab
        ---
        show block {num}
        show {num}
        {num} show
        show
        show larger block {num}
        show larger {num}
        {num} show larger
        show larger
        larger
        enlarge
        enlarge block {num}
        enlarge {num}
        {num} enlarge
    """
    print("woop", num)
    SessChain = consumers.getSessChain()

    print("inside BLOCK: ")
    print(SessChain)

    if type(num) is int:
        if num < SessChain.getBlockListLength():
            msg = "showing block " + str(num)
            try:
                SessChain.getBlock(num).showBlock(num)
            except:
                msg = "function not available for block " + str(num)
        else:
            msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength() - 1)
    else:
        print("\033[94m Amazon provided " + str(type(num)) + " type \033[0m")
        try:
            SessChain.getBlock(-1).showBlock()
            msg = "showing last block"
        except:
            msg = "Function not available for last block"


    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)

# read message intent
@intent(slots=Num, app="AlexaHandler")
def readMsg(session, num=0):
    """
        reading the block with number X
        ---
        read block {num}
        read {num}
        {num} read
        read
    """
    print("woop", num)
    SessChain = consumers.getSessChain()

    print("inside BLOCK: ")
    print(SessChain)

    if type(num) is int:
        if num < SessChain.getBlockListLength():
            try:
                msg = SessChain.getBlock(num).readBlock()
            except:
                msg = "function not available for block " + str(num)
        else:
            msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength() - 1)
    else:
        print("\033[94m Amazon provided None type \033[0m")
        try:
            msg = SessChain.getBlock(-1).readBlock()
        except:
            msg = "function not available for last block"

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)


# load File intent
@intent(slots=Num, app="AlexaHandler")
def loadFile(session, num=0):
    """
        loading file with number {num}
        ---
        read file {num}
        read {num}
        {num} read
        load file {num}
        load {num}
        {num} load
        file {num}
        {num} file  
    """
    print("loading", num)
    FileList = consumers.getFileList()
    print(FileList)

    if type(num) is int:
        if num < len(FileList):
            try:
                SessChain = consumers.getSessChain()
                print("got Chain")
                IO = IO_Block(file_name=FileList[num], session="alexa")
                print("NEW IO BLOCK")
                SessChain.addBlock(IO)
                print("added to Chain:")

                print(SessChain)
                Group("alexa").send({
                    "text": IO.GetNode()
                })
                #SessChain.Chain_pickle()
                msg = FileList[num] + "successfully loaded"
            except:
                print("\033[93mUnexpected error:", sys.exc_info(), "\033[0m")
                msg = "error loading file  " + str(num)
        else:
            msg = "File with number " + str(num) + " does not exist. Maximum File number is " + str(len(FileList) - 1)
    else:
        print("\033[94m Amazon provided None type \033[0m")
        msg = "Please provide a number"

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)

# do a PCA intent
@intent(slots=Num, app="AlexaHandler")
def doPCA(session, num=0):
    """
        P.C.A. with data from block {num}
        ---
        block {num} P.C.A.
        {num} P.C.A.
        P.C.A. {num}
        perform a P.C.A. on block {num}
        do a P.C.A. on block {num}
        perform a P.C.A. on {num}
        do a P.C.A. on {num}
        P.C.A. on {num}
    """
    SessChain = consumers.getSessChain()
    if type(num) is int:
        if num < SessChain.getBlockListLength():
            block = SessChain.getBlock(num)
            try:
                PCA = PCA_Block(var_name=block.data_name, data=block.getData(), session="alexa")
                print("NEW PCA BLOCK")
                SessChain.addBlock(PCA)

                Group("alexa").send({
                    "text": PCA.GetNode()
                })
                SessChain.Chain_pickle()
                msg = "processed"
            except:
                print("\033[93mUnexpected error:", sys.exc_info(), "\033[0m")
                msg = "error processing block" + str(num)
        else:
            msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength() - 1)
    else:
        print("\033[94m Amazon provided None type \033[0m")
        msg = "Please provide a number"

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)

# (Sand) Image Filter intent
@intent(slots=Num, app="AlexaHandler")
def doSandFilter(session, num=0):
    """
        sand Filter on image {num}
        ---
        segment {num}
        {num} segment
        process {num}
        {num} process
        filter {num}
        {num} filter
        sand {num}
        {num} sand
    """
    SessChain = consumers.getSessChain()
    if type(num) is int:
        if num < SessChain.getBlockListLength():
            block = SessChain.getBlock(num)
            try:
                Filter = SandFilterBlock(var_name=block.data_name, data=block.getData(), session="alexa")
                print("NEW Sand BLOCK")
                SessChain.addBlock(Filter)

                Group("alexa").send({
                    "text": Filter.GetNode()
                })
                SessChain.Chain_pickle()
                msg = "processed"
            except:
                print("\033[93mUnexpected error:", sys.exc_info(), "\033[0m")
                msg = "error processing block" + str(num)
        else:
            msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength() - 1)
    else:
        print("\033[94m Amazon provided None type \033[0m")
        msg = "Please provide a number"

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)



# pass Option
@intent(slots=OPT, app="AlexaHandler")
def passOption(session, number=-1, alexa_option=""):
    """
         option passing
        ---
        pass option {alexa_option} to block {number}
        option {alexa_option} block {number}
        block {number} option {alexa_option}
    """

    print("\033[93m", number, alexa_option, "\033[0m")
    num = number
    SessChain = consumers.getSessChain()
    if type(num) is int:
        if num < SessChain.getBlockListLength():
            block = SessChain.getBlock(num)
            try:
                block.getOption(alexa_option)
                msg = "processed"
            except:
                print("\033[93mUnexpected error:", sys.exc_info(), "\033[0m")
                msg = "error processing block" + str(num)
        else:
            msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength() - 1)
    else:
        print("\033[94m Amazon provided None type \033[0m")
        msg = "Please provide a number"

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)

# save Results intent
@intent(slots=Num, app="AlexaHandler")
def saveResult(session, num=0):
    """
        saves whatever result the block has to save
        ---
        save {num}
        {num} save
        save block {num}
        {num} save block
        export {num}
        {num} export
        export block {num}
        {num} export block
    """
    SessChain = consumers.getSessChain()
    if type(num) is int:
        if num < SessChain.getBlockListLength():
            block = SessChain.getBlock(num)
            try:
                print("got Chain")
                block.save()
                msg = "saved"
            except:
                print("\033[93mUnexpected error:", sys.exc_info(), "\033[0m")
                msg = "error saving block" + str(num)
        else:
            msg = "block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength() - 1)
    else:
        print("\033[94m Amazon provided None type \033[0m")
        msg = "Please provide a number"

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)

# delete Block intent
@intent(slots=Num, app="AlexaHandler")
def delBlock(session, num=0):
    """
        deletes the block with number {num}
        ---
        delete {num}
        {num} delete
        delete block {num}
        {num} delete block
    """
    SessChain = consumers.getSessChain()
    if type(num) is int:
        if num < SessChain.getBlockListLength():
            try:
                print("deleting:", num)
                SessChain.delBlockByIndex(num)
                data = {"type": "cmd",
                        "cmd": "del_block",
                        "block_num": num,
                        }
                Group("alexa").send({
                    "text": json.dumps(data)
                })
                msg = "block deleted"
            except:
                print("\033[93mUnexpected error:", sys.exc_info(), "\033[0m")
                msg = "error deleting block" + str(num)
        else:
            msg = "block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength() - 1)
    else:
        print("\033[94m Amazon provided None type \033[0m")
        msg = "Please provide a number"

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)

# minimize intent
@intent(slots=None, app="AlexaHandler")
def minimize(session):
    """
    minimizes after show Block
    ---
    minimize
    make small
    hide
    back
    """
    data = {"type": "cmd",
            "cmd": "minimize",
            }
    Group("alexa").send({
        "text": json.dumps(data)
    })
    return ResponseBuilder.create_response(message="",
                                           reprompt="",
                                           end_session=False,
                                           launched=True)