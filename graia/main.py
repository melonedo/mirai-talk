import asyncio

from graia.application import GraiaMiraiApplication as GraiaApp, Session
from graia.broadcast import Broadcast
from graia.broadcast.exceptions import ExecutionStop
from graia.broadcast.builtin.decoraters import Depend
from graia.application.entry import Friend, FriendMessage, MessageChain, Group, GroupMessage, Plain, ApplicationShutdowned

import yaml
import aiohttp

# 包含mirai-api-http的配置文件中的对应部分以及qq号
with open('setting.yml') as f:
    setting = yaml.load(f, yaml.BaseLoader)
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaApp(
    broadcast=bcc,
    connect_info=Session(
        host=f"http://{setting['host']}:{setting['port']}",
        authKey=f"{setting['authKey']}",
        account=setting['qq'],
        websocket=setting['enableWebsocket']
    )
)


@bcc.receiver(FriendMessage)
async def echoer(app: GraiaApp, message: MessageChain, friend: Friend):
    if message.asDisplay().startswith("复读"):
        await app.sendFriendMessage(friend, message.asSendable())


WHITELIST = [943603660]


@bcc.receiver(GroupMessage)
async def electricity(app: GraiaApp, message: MessageChain, group: Group):
    if not (group.id in WHITELIST and message.asDisplay().startswith("电费")):
        return

    async with aiohttp.ClientSession() as s:
        resp = await s.get(
            "http://172.81.215.215/pi/electricity",
            params={'room': message.asDisplay()[2:]})
        json = await resp.json()
    if json['success']:
        text = f"{json['name']} {json['type']}: {json['number']}{json['unit']}"
    else:
        text = f"查询失败，原因：{json['error']}"
    await app.sendGroupMessage(group, MessageChain.create([Plain(text)]))

app.launch_blocking()
