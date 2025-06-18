

from typing import Any, Callable

import logging
LOG = logging.getLogger(__name__)


# This demonstrates the basic desired behaviour: the supervise(...) function
# is called with the details needed to create a coroutine.  It creates one,
# and ensures that if that coroutine ever exits a replacement one is created.
#
# The main problem with this is that it has no error handling for if the
# coroutine "crashes".
#
async def supervise_0(fn: Callable, *args: Any) -> None:
    while True:
        await fn(*args)


"""
>>> import asyncio
>>> async def activity(kvstore):
...     await asyncio.sleep(3)
...     print(kvstore["key"])
>>> asyncio.run(supervise_0(activity, {"foo": "bar"}))
"""


# Using try/except can handle the restarting even with failures.
# And we can lean into the stdlib logging library to show the traceback.
#
# BUT... it's really not obvious how well it handles being cancelled from outside.
#
async def supervise_1(fn: Callable, *args: Any) -> None:
    while True:
        try:
            await fn(*args)
        except Exception as exc:
            LOG.exception(exc)
