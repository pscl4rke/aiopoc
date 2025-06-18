

import asyncio

import supervising


async def hello(name: str) -> None:
    await asyncio.sleep(1)
    print(f"Hello {name}")
    raise Exception("Went wrong")


async def main():
    task = asyncio.create_task(supervising.supervise_1(hello, "Ebenezer"))
    await asyncio.sleep(4.5)
    print("Done")
    task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
