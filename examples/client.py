import discord
import asyncio
from discord.ext import ipc


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ipc = ipc.Client(client, "Test")
        
    async def setup_hook(self):
        async with self.ipc:
            await self.ipc.connect("ws://localhost:8080")
    
    async def on_ipc_connect(self, r):
        print("Connected")
    
client = MyClient(intents=discord.Intents.all())


client.run("TOKEN")
