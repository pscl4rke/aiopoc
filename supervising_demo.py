

import asyncio

import supervising


async def hello(queue) -> None:
    name = await queue.get()
    print(f"Hello {name}")
    raise Exception("Went wrong")


async def main_queue():
    queue = asyncio.Queue()
    task = asyncio.create_task(supervising.supervise_1(hello, queue))
    for name in ["Matthew", "Mark", "Luke", "John"]:
        await asyncio.sleep(1)
        await queue.put(name)
    await asyncio.sleep(1)
    print("Done")
    task.cancel()


async def main_timeout():
    queue = asyncio.Queue()
    await asyncio.wait_for(supervising.supervise_1(hello, queue), 3)


if __name__ == "__main__":
    asyncio.run(main_queue())
    #asyncio.run(main_timeout())
