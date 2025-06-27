

from contextlib import asynccontextmanager
from typing import Coroutine, AsyncIterator

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
async def daemonise(coro: Coroutine) -> AsyncIterator:
    task = asyncio.create_task(coro)
    try:
        yield
    finally:
        task.cancel()


# By passing in an existing task object the use can decide whether to create
# an ordinary Task or one in a TaskGroup.
#
# Calling it "cancelling(...)" gives a nice symmetry with contextlib.closing(...)
# and contextlib.aclosing(...).
@asynccontextmanager
async def cancelling(task: asyncio.Task) -> AsyncIterator:
    try:
        yield task
    finally:
        task.cancel()


# Why not allow either Tasks or Coroutines to be passed in:
#
# You could even define a typing.Protocol to specify the right method.
#
@asynccontextmanager
async def cancelling2(cancellable: Coroutine | asyncio.Task) -> AsyncIterator:
    task = asyncio.ensure_future(cancellable)
    try:
        yield task
    finally:
        task.cancel()
