import asyncio

from graia.application import GraiaMiraiApplication as GraiaApp, Session
from graia.broadcast import Broadcast
from graia.application.entry import Friend, FriendMessage, MessageChain, Group, GroupMessage, Plain
from graia.application.entry import ApplicationLaunched, MemberMuteEvent, At, MemberUnmuteEvent, Member

import yaml
import aiohttp
import time

time.sleep(15)

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

# 复读
# @bcc.receiver(FriendMessage)
async def echoer(app: GraiaApp, message: MessageChain, friend: Friend):
    if message.asDisplay().startswith("复读"):
        await app.sendFriendMessage(friend, message.asSendable())
echoer = bcc.receiver(FriendMessage)(echoer)  # 如果不用修饰器

TEST_GROUP_LIST = [943603660]


# 查电费
@bcc.receiver(GroupMessage)
async def electricity(app: GraiaApp, message: MessageChain, group: Group):
    if not (group.id in TEST_GROUP_LIST and message.asDisplay().startswith("电费")):
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


# 开机事件
@bcc.receiver(ApplicationLaunched)
async def hello(app: GraiaApp):
    for group in TEST_GROUP_LIST:
        await app.sendGroupMessage(group, MessageChain.fromSerializationString(
            "hello[mirai:image:{43E03605-6CE5-48D3-2CB5-0A52A9512896}.mirai]"
        ))


# 禁言（直接获取事件）
@bcc.receiver(MemberMuteEvent)
async def mute_notice(app: GraiaApp, event: MemberMuteEvent):
    await app.sendGroupMessage(event.member.group, MessageChain.create([
        At(event.member.id),
        Plain("被卷死了")
    ]))


# 解除禁言（利用注释）
@bcc.receiver(MemberUnmuteEvent)
async def unmute_notice(app: GraiaApp, group: Group, member: Member = "target"):
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),
        Plain("开始学了")
    ]))

app.launch_blocking()
