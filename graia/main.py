import asyncio

from graia.application import GraiaMiraiApplication as GMA, Session
from graia.broadcast import Broadcast
from graia.application.entry import Friend, FriendMessage, MessageChain

import yaml

with open('setting.yml') as f:
    setting = yaml.load(f, yaml.BaseLoader)
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GMA(
    broadcast=bcc,
    connect_info=Session(
        host=f"http://{setting['host']}:{setting['port']}",
        authKey=f"{setting['authKey']}",
        account=setting['qq'],
        websocket=setting['enableWebsocket']
    )
)



@bcc.receiver(FriendMessage)
async def group_message_handler(app: GMA, message: MessageChain, friend: Friend):
    if message.asDisplay().startswith("复读"):
        await app.sendFriendMessage(friend, message.asSendable())

app.launch_blocking()
