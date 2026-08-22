import asyncio
import select
import sys

from . import eventio
from .events import InputEvent

# needed for compatibility
from .eventio import EvdevError

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing import Any as Self


class ReadIterator:
    def __init__(self, device: "EventIO"):
        self.current_batch = iter(())
        self.device = device

    # Standard iterator protocol.
    def __iter__(self) -> Self:
        return self

    def __next__(self) -> InputEvent:
        try:
            # Read from the previous batch of events.
            return next(self.current_batch)
        except StopIteration:
            r, w, x = select.select([self.device.fd], [], [])
            self.current_batch = self.device.read()
            return next(self.current_batch)

    def __aiter__(self) -> Self:
        return self

    def __anext__(self) -> "asyncio.Future[InputEvent]":
        future = asyncio.get_running_loop().create_future()
        try:
            # Read from the previous batch of events.
            future.set_result(next(self.current_batch))
        except StopIteration:

            def next_batch_ready(batch):
                try:
                    self.current_batch = batch.result()
                    future.set_result(next(self.current_batch))
                except Exception as e:
                    future.set_exception(e)

            self.device.async_read().add_done_callback(next_batch_ready)
        return future


class EventIO(eventio.EventIO):
    # The event loop a reader was last registered on, or None if no async read
    # has been awaited yet. Set in _do_when_readable, used by close().
    _loop: "asyncio.AbstractEventLoop | None" = None

    def _do_when_readable(self, callback) -> None:
        # Remember the loop the reader is registered on so that close() can
        # remove it later, even when called without a running event loop.
        loop = asyncio.get_running_loop()
        self._loop = loop

        def ready():
            loop.remove_reader(self.fileno())
            callback()

        loop.add_reader(self.fileno(), ready)

    def _set_result(self, future, cb) -> None:
        try:
            future.set_result(cb())
        except Exception as error:
            future.set_exception(error)

    def async_read_one(self) -> "asyncio.Future[InputEvent]":
        """
        Asyncio coroutine to read and return a single input event as
        an instance of :class:`InputEvent <evdev.events.InputEvent>`.
        """
        future = asyncio.get_running_loop().create_future()
        self._do_when_readable(lambda: self._set_result(future, self.read_one))
        return future

    def async_read(self) -> "asyncio.Future[InputEvent]":
        """
        Asyncio coroutine to read multiple input events from device. Return
        a generator object that yields :class:`InputEvent <evdev.events.InputEvent>`
        instances.
        """
        future = asyncio.get_running_loop().create_future()
        self._do_when_readable(lambda: self._set_result(future, self.read))
        return future

    def async_read_loop(self) -> ReadIterator:
        """
        Return an iterator that yields input events. This iterator is
        compatible with the ``async for`` syntax.

        """
        return ReadIterator(self)

    def close(self) -> None:
        # A reader is only registered once an async read has been awaited, in
        # which case _do_when_readable recorded the loop it was added to.
        loop = self._loop
        if loop is None or loop.is_closed():
            # No reader was ever registered, or its loop is already gone, so
            # there is nothing to remove the reader from.
            return
        loop.remove_reader(self.fileno())
