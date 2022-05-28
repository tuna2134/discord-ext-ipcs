# discord-ext-ipc

[![Documentation Status](https://readthedocs.org/projects/discord-ext-ipcs/badge/?version=latest)](https://discord-ext-ipcs.readthedocs.io/en/latest/?badge=latest)

## Example Client

```python
import discord
from discord.ext import ipcs


client = discord.Client(intents=discord.Intents.all())
ipc_client = ipcs.Client(client, "TopSecretKey")


@client.event
async def on_ready():
    async with ipc_client:
        await ipc_client.connect("ws://localhost/ipc")

@client.event
async def on_ipc_connect():
    print("ipc connected")
    
@client.event
async def on_ipc_close():
    print("Ipc closed")
        
@ipc_client.listen("ready")
async def ipc_ready():
    print("ready")
```
