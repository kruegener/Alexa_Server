# django-alexa imports
from django_alexa.api import fields, intent, ResponseBuilder
# BlockChain import for SessChain Handling
from .BlockChain import BlockChain

from .. import consumers


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
            msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength())

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
            msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength())
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
            msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength())
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