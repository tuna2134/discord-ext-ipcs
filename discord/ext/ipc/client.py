# discord.ext.ipc - client
from websockets.client import WebSocketClientProtocol
from .errors import ConnectionError
from websockets import connect
from discord import Client
import asyncio

try:
    from orjson import dumps, loads
except ImportError:
    from json import dumps, load


class Client:
    def __init__(self, client: Client, secret_key: str, *, loop=None):
        self.client = client
        self.secret_key = secret_key
        self.loop = loop
        self.ws: WebSocketClientProtocol = None
        self.events: list = []
        
    async def __aenter__(self):
        if self.loop is None:
            self.loop = asyncio.get_running_loop()
        
    async def __aexit__(self, *args):
        await self.close()
        self.loop.close()
        
    async def connect(self, host: str, port: int=80, *, scheme: str="ws"):
        self.host, self.port, self.scheme = host, port, scheme
        if self.ws is not None:
            raise ConnectionError("Already connected")
        self.ws = await connect("{0}://{1}:{2}".format(scheme, host, port))
        self.client.dispatch("ipc_connect")
        await self.login()
        while self.ws.open:
            await self.recv()
    
    async def close(self):
        if self.ws is not None:
            if not self.ws.closed:
                await self.ws.close()
                self.client.dispatch("ipc_close")
            self.ws = None
        else:
            raise ConnectionError("Already closed")
            
    async def reconnect(self):
        await self.close()
        await asyncio.sleep(0.5)
        await self.connect(self.host, self.port, scheme=self.scheme)
            
    def login(self):
        return self.request("login")
            
    async def request(self, eventtype: str, data: dict={}):
        payload = {
            "type": eventtype,
            "data": data
        }
        await self.ws.send(dumps(payload))
        
    def listen(self, eventtype: str):
        def decorator(func):
            if eventtype in self.events:
                self.events[eventtype].append(func)
            else:
                self.events[eventtype] = [func]
            return func
        return decorator
    
    async def recv(self):
        data = loads(await self.ws.recv())
        
        if data["type"] == "close":
            self.client.dispatch("ipc_close")

        if data["type"] in self.events:
            self.loop.create_task(
                self.events[data["type"]](
                    ResponseItem(
                        data["data"]
                    )
                )
            )

class ResponseItem:
    def __init__(self, data: dict):
        for name, value in data.items():
            setattr(self, name, value)