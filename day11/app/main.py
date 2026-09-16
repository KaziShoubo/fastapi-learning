from fastapi import FastAPI, HTTPException
import asyncio
import httpx

app = FastAPI()


# async def allows FastAPI to run the endpoint as a coroutine, so when it reaches an awaitable I/O operation,
# it can pause that request while waiting and let the event loop handle other work
# awaits-Pause this coroutine while the awaited async operation is in progress, so the event loop can work on other tasks.
@app.get("/")
async def home():
    return {"message": "Hello from Day 11"}


@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(3)
    return {"message": "Finished after 3 seconds"}


# await asyncio.sleep(3) is a non-blocking asynchronous operation. It pauses the current coroutine while waiting,
# giving the event loop an opportunity to handle other work. time.sleep(3) is a blocking operation;
# it blocks the event loop during those three seconds.
# Day11: Learn async FastAPI and concurrent operations


@app.get("/async-task")
async def async_task():
    await asyncio.sleep(3)

    return {"message": "asynchronous friendly"}


@app.get("/blocking-task")
async def blocking_task():
    import time
    time.sleep(3)

    return {"message": "Blocking task finished"}


@app.get("/external-data")
async def get_external_data():
    async with httpx.AsyncClient() as client:  # This creates an asynchronous HTTP client that we can use to communicate with external HTTP APIs.

        try:
            response = await client.get("https://httpbin.org/get")
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=503, detail="External service is unavailable")

        return response.json()


# ---------Practical Challenge-------------
async def api_a():
    await asyncio.sleep(2)
    return {"api_a": "API A finished"}


async def api_b():
    await asyncio.sleep(3)
    return {"api_b": "API B finished"}


@app.get("/combined-data")
async def combined_data():
    results = await asyncio.gather(
        api_a(),
        api_b()
    )
    # ** means: Take all the key-value pairs from this dictionary and put them here.
    return{
        **results[0],
        **results[1]
    }
