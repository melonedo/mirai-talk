from graia.broadcast import Broadcast
from graia.application.entry import GraiaMiraiApplication
import asyncio
import yaml

with open('setting.yml') as f:
    setting = yaml.load(f, yaml.BaseLoader)
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=f"http://{setting['host']}:{setting['port']}",
        authKey=f"{setting['authKey']}",
        account=setting['qq'],
        websocket=setting['enableWebsocket']
    )
)