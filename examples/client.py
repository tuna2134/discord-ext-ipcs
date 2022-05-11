import discord
import asyncio
from discord.ext import ipc


client = discord.Client(intents=discord.Intents.all())
ipc_client = ipc.Client(client, "Test")

async def main():
    async with ipc_client:
        await ipc_client.connect("ws://localhost:8080")
        
asyncio.run(main())
