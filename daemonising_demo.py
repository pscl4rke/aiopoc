

import asyncio

import daemonising


async def keep_saying_hello():
    #while True:
    #    await asyncio.sleep(0.4)
    #    print("Hello!")
    try:
        while True:
            await asyncio.sleep(0.4)
            print("Hello!")
    except asyncio.CancelledError:
        print("I've been cancelled! Goodbye!")


async def main():
    async with daemonising.daemonise(keep_saying_hello()):
        await asyncio.sleep(1)
        print("Thing 1")
        await asyncio.sleep(1)
        print("Thing 2")
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
