# django-alexa imports
from django_alexa.api import fields, intent, ResponseBuilder
# BlockChain import for SessChain Handling
from .BlockChain import BlockChain

from .. import consumers


# ALEXA PART

# define slots
class Num(fields.AmazonSlots):
    num = fields.AmazonNumber()

# define intent
@intent(slots=Num, app="AlexaHandler")
def executeBlock(session, num=0):
    """
        executing the block with number X
        ---
        execute block {num}
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