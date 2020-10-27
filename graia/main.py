import asyncio

from graia.application import GraiaMiraiApplication as GraiaApp, Session
from graia.broadcast import Broadcast
from graia.broadcast.exceptions import ExecutionStop
from graia.broadcast.builtin.decoraters import Depend
from graia.application.entry import Friend, FriendMessage, MessageChain, Group, GroupMessage, Plain, ApplicationShutdowned

import yaml
import aiohttp

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

def judge_group(group: Group):
    whitelist = [943603660]
    if group.id not in whitelist:
        raise ExecutionStop

def judge_command(cmd: str) -> callable:
    def _judge_command(msg: MessageChain):
        if not msg.asDisplay().startswith(cmd):
            raise ExecutionStop
    return _judge_command


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(judge_group), Depend(judge_command("电费"))])
async def electricity(app:GraiaApp, message: MessageChain, group: Group):
    async with aiohttp.ClientSession() as s:
        resp = await s.get("http://172.81.215.215/pi/electricity", params={'room': message.asDisplay()[2:]})
        json = await resp.json()
    if json['success']:
        text = f"{json['name']} {json['type']}: {json['number']}{json['unit']}"
    else:
        text = f"查询失败，原因：{json['error']}"
    await app.sendGroupMessage(group, MessageChain.create([Plain(text)]))

app.launch_blocking()
