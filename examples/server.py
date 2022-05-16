from websockets import serve
import asyncio


async def echo(ws):
    while True:
        print(await ws.recv())


async def main():
    async with serve(echo, "localhost", 8080):
        await asyncio.Future()

asyncio.run(main())
