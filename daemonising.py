

from contextlib import asynccontextmanager
from typing import Coroutine, Generator

import asyncio


# The idea of this is to run a task in the background.  But the task
# is "providing a service" and so will run forever.  Therefore we need
# to cancel it when the rest of the code is done (successfully or with
# an error).
#
# A context manager is the obvious way of structuring this, but existing
# context managers in the stdlib (such as TaskGroup) will wait until
# everything finishes.
#
# Q. Do we want TaskGroup support as well (or instead!)
#
# Q. What should be yielded? the task? the coro? something else?
#
@asynccontextmanager
async def daemonise(coro: Coroutine) -> Generator:
    task = asyncio.create_task(coro)
    try:
        yield
    finally:
        task.cancel()
