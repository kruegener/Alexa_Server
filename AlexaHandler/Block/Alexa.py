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
    """
    print("woop", num)
    SessChain = consumers.getSessChain()

    print("inside BLOCK: ")
    print(SessChain)

    if num < SessChain.getBlockListLength():
        msg = "Executed block " + str(num);
        SessChain.getBlock(num).executeBlock(num)
    else:
        msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength())

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)


@intent(slots=Num, app="AlexaHandler")
def showImg(session, num=0):
    """
        showing the block with number X in new tab
        ---
        show block {num}
        show {num}
        {num} show
    """
    print("woop", num)
    SessChain = consumers.getSessChain()

    print("inside BLOCK: ")
    print(SessChain)

    if num < SessChain.getBlockListLength():
        msg = "showing block " + str(num);
        try:
            SessChain.getBlock(num).showBlock(num)
        except:
            msg = "function not available for block " + str(num);
    else:
        msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength())

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)

@intent(slots=Num, app="AlexaHandler")
def readMsg(session, num=0):
    """
        reading the block with number X
        ---
        read block {num}
        read {num}
        {num} read
    """
    print("woop", num)
    SessChain = consumers.getSessChain()

    print("inside BLOCK: ")
    print(SessChain)

    if num < SessChain.getBlockListLength():
        try:
            msg = SessChain.getBlock(num).readBlock()
        except:
            msg = "function not available for block " + str(num);
    else:
        msg = "Block with number " + str(num) + " does not exist. Maximum block number is " + str(SessChain.getBlockListLength())

    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)