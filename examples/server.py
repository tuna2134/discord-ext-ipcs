from websockets import serve
import asyncio


async def echo(ws):
    print(await ws.recv())
    
async def main():
    async with serve():
        await asyncio.Future()
        
asyncio.run(main())
