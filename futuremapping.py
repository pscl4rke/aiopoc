

# I'm not sure how much this is an async pattern, and really not sure
# how much it is specific to futures.  But that's where I've found it
# helpful.


# This is for when you've got a block of code that triggers a thing
# and blocks waiting for another task to get a result.  But the other
# task is handling results from many triggers, so it needs to look up
# which future to write to.

# But we use a context manager because we want to ensure we always
# tidy up the futures we're not using any more...

# >>> async def do_work(action):
# ...     identifier = generate_id()
# ...     with FUTUREMAP.new(identifier) as future:
# ...         await CONTROLLER.send(f"START {action} {identifier}\n")
# ...         async with asyncio.timeout(10):
# ...             await future
# ...         return future.result()

# >>> async def handle_responses():
# ...     async for response in CONTROLLER.responses():
# ...         key, reaction, result = response.split()
# ...         if reaction == "SUCCESS":
# ...             FUTUREMAP.set_result_for(key, result, ignore=True)
# ...         elif reaction == "FAILURE":
# ...             FUTUREMAP.set_exception_for(key, Exception(result), ignore=True)

# Note that we cannot trigger a start until the future is in place because
# there is a race condition if the response comes back before _pending is
# updated.

# Hmm, should FutureMap itself be cancellable, propagating to all
# the futures it contains.  Maybe it is itself a context?


#from contextlib import asynccontextmanager
from contextlib import contextmanager
import asyncio


class FutureMap:

    def __init__(self):
        self._pending = {}

    def set_result_for(self, key, result, ignore=False):
        if key not in self._pending:
            if ignore:
                return
            else:
                raise KeyError(key)
        self._pending[key].set_result(result)

    def set_exception_for(self, key, exception, ignore=False):
        if key not in self._pending:
            if ignore:
                return
            else:
                raise KeyError(key)
        self._pending[key].set_exception(exception)

    @contextmanager
    def new_for(self, key):
        if key in self._pending:
            raise Exception("Duplicate key: %r" % key)
        future = asyncio.Future()
        self._pending[key] = future
        try:
            yield future
        finally:
            del self._pending[key]
