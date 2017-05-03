# django-alexa imports
from django_alexa.api import fields, intent, ResponseBuilder
# BlockChain import for SessChain Handling
from .BlockChain import BlockChain
from .IO_Block import IO_Block
from .PCA_Block import PCA_Block
from channels import Group
from .. import consumers
import sys

# ALEXA PART

# define slots
class Num(fields.AmazonSlots):
    num = fields.AmazonNumber()

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


# read message intent
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
                SessChain.Chain_pickle()
                print(SessChain)
                Group("alexa").send({
                    "text": IO.GetNode()
                })
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

# read message intent
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
                print("got Chain")
                PCA = PCA_Block(var_name=block.data_name, data=block.getData(), session="alexa")
                print("NEW PCA BLOCK")
                SessChain.addBlock(PCA)
                print("added to Chain:")
                SessChain.Chain_pickle()
                print(SessChain)
                Group("alexa").send({
                    "text": PCA.GetNode()
                })
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

# read message intent
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