import asyncio
import time
import httpx


async def request_one():
    await asyncio.sleep(3)
    return "Request one finished"


async def request_two():
    await asyncio.sleep(3)
    return "Request two finished"


async def main():
    results = await asyncio.gather(
        request_one(),
        request_two()
    )

    print(results)


asyncio.run(main())




