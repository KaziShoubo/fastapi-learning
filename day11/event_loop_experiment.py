import asyncio


# It is one coroutine
async def io_operation():
    print("Starting I/O operation")
    await asyncio.sleep(5)
    print("I/O operation finished")


# It is another coroutine
async def other_work():
    for i in range(1, 6):
        await asyncio.sleep(1)
        print(f"Event loop is doing other work.....{i}")


# When waiting for io_operation, the event loop(main()) can execute other coroutine i.e, other_work()
async def main():
    results = await asyncio.gather(
        io_operation(),
        other_work()
    )
    print(results)


asyncio.run(main())
