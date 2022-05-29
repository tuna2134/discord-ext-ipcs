from websockets import serve
import orjson
import asyncio


async def echo(ws):
    while True:
        payload = orjson.loads(await ws.recv())
        type_, data = payload["type"], payload["data"]
        if type_ == "login":
            if data["password"] == "":
                await ws.send(orjson.dumps({"type": "ready", "data": {}}))
            else:
                await ws.close()


async def main():
    async with serve(echo, "localhost", 8080):
        await asyncio.Future()

asyncio.run(main())
