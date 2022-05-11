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
        self.uri: str = None
        
    async def __aenter__(self):
        if self.loop is None:
            self.loop = asyncio.get_running_loop()
        
    async def __aexit__(self, *args):
        await self.close()
        self.loop.close()
        
    async def connect(self, uri: str) -> None:
        """Connect to ipc server
        
        Args:
            uri (str): URI
            
        Examples:
            await ipc_client.connect("ws://localhost/ipc")
        
        Raises:
            ConnectionError: If you already connect, it will be raise.
        """
        self.uri = uri
        if self.ws is not None:
            raise ConnectionError("Already connected")
        self.ws = await connect(uri)
        self.client.dispatch("ipc_connect")
        await self.login()
        while self.ws.open:
            await self.recv()
    
    async def close(self) -> None:
        """Close from ipc server
        
        Raises:
            ConnectionError: If you already close, it will be raise.
            
        Examples:
            await ipc_client.close()
        """
        if self.ws is not None:
            if not self.ws.closed:
                await self.ws.close()
                self.client.dispatch("ipc_close")
            self.ws = None
        else:
            raise ConnectionError("Already closed")
            
    async def reconnect(self) -> None:
        """Reconnect from ipc server
        
        Examples:
            await ipc_client.reconnect()
        """
        await self.close()
        await asyncio.sleep(0.5)
        await self.connect(self.uri)
            
    def login(self):
        """Login to ipc server
        
        Examples:
            await ipc_client.login()
        """
        return self.request("login")
            
    async def request(self, eventtype: str, data: dict={}) -> None:
        """Send something to ipc server
        
        Args:
            eventtype (str): event type
            data (dict): The data you want to send.
            
        Examples:
            await ipc_client.request("hello", {"message": "What your name"})
        """
        payload = {
            "type": eventtype,
            "data": data
        }
        await self.ws.send(dumps(payload))
        
    def listen(self, eventtype: str):
        """Catch data from ipc server
        
        Args:
            eventtype (str): Event type.
            
        Examples:
            @ipc_client.listen("hello")
            async def hello(response):
                await self.request("hello", {"message": "My name is Satoshi"})
        """
        def decorator(func):
            if eventtype in self.events:
                self.events[eventtype].append(func)
            else:
                self.events[eventtype] = [func]
            return func
        return decorator
    
    async def dispatch(self, eventtype: str, response: ResponseItem):
        if eventtype in self.events:
            await asyncio.gather(*[coro(response) for coro in self.events[eventtype]])
        self.client.dispatch("ipc_{}".format(eventtype))
    
    async def recv(self) -> None:
        data = loads(await self.ws.recv())
        
        if data["type"] == "close":
            self.client.dispatch("ipc_close")

        if data["type"] in self.events:
            await self.dispatch(data["type"], data["data"])

class ResponseItem:
    """Response data
    
    Args:
        data (dict): Some kind of data.
        
    Examples:
        response = ResponseItem({"hello": "world", "message": "What your name?"})
        print(response.hello)
    """
    def __init__(self, data: dict):
        for name, value in data.items():
            setattr(self, name, value)
