# discord-ext-ipc

## Example Client

```python
import discord
from discord.ext import ipc


client = discord.Client(intents=discord.Intents.all())
ipc_client = ipc.Client(client, "TopSecretKey")


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
