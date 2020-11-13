from startup import bcc, app
from graia.application.entry import GraiaMiraiApplication as GraiaApp, Friend, FriendMessage, MessageChain, Plain

@bcc.receiver(FriendMessage)
async def hello_world(app: GraiaApp, friend: Friend):
    await app.sendFriendMessage(MessageChain.create([
        Plain("Hello world!")
    ]))

app.launch_blocking()