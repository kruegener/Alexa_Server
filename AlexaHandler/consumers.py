''' making the consumers '''

from channels.handler import AsgiHandler
from channels import Group

def ws_message(message):
    #print(message.content['text'])
    Group("alexa").send({
        "text": "[user] %s" % message.content['text'],
    })

def ws_add(message):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})
    # Add them to the chat group
    Group("alexa").add(message.reply_channel)

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("alexa").discard(message.reply_channel)