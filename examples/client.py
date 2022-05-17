import discord
import asyncio
from discord.ext import ipc


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ipc_client = ipc.Client(client, "Test")
        
    async def setup_hook(self):
        async with ipc_client:
            await ipc_client.connect("ws://localhost:8080")
    
    async def on_ipc_connect(self, r):
        print("Connected")
    
client = MyClient(intents=discord.Intents.all())


client.run("TOKEN")
