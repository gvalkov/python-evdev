import asyncio
import os

import pytest

from evdev import _uinput, ecodes
from evdev.eventio_async import EventIO


class PipeEventIO(EventIO):
    """Drive the native input-event reader with a pipe instead of hardware."""

    def __init__(self):
        self.fd, self.writer = os.pipe2(os.O_NONBLOCK)
        self.readable = asyncio.Event()

    def _do_when_readable(self, callback):
        def observed():
            try:
                callback()
            finally:
                self.readable.set()

        super()._do_when_readable(observed)

    def write_key(self):
        _uinput.write(self.writer, ecodes.EV_KEY, ecodes.KEY_A, 1)

    def close(self):
        super().close()
        os.close(self.fd)
        os.close(self.writer)


def start_read(device, mode):
    if mode == "loop":
        return device.async_read_loop().__anext__()
    return getattr(device, "async_" + mode)()


@pytest.mark.parametrize("mode", ["read_one", "read", "loop"])
@pytest.mark.parametrize("read_error", [False, True])
def test_cancelled_read_preserves_next_event(mode, read_error):
    async def check():
        errors = []
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(lambda loop, context: errors.append(context))
        device = PipeEventIO()
        try:
            pending = start_read(device, mode)
            if read_error:
                def fail():
                    raise OSError("device disconnected")

                device.read = device.read_one = fail
            pending.cancel()
            device.write_key()
            await asyncio.wait_for(device.readable.wait(), 1)
            assert pending.cancelled()
            assert errors == []
            if read_error:
                del device.read, device.read_one
            event = await asyncio.wait_for(device.async_read_one(), 1)
            assert (event.type, event.code, event.value) == (ecodes.EV_KEY, ecodes.KEY_A, 1)
        finally:
            device.close()

    asyncio.run(check())


@pytest.mark.parametrize("mode", ["read_one", "read", "loop"])
def test_active_read_preserves_error(mode):
    async def check():
        device = PipeEventIO()
        error = OSError("device disconnected")

        def fail():
            raise error

        device.read = device.read_one = fail
        try:
            pending = start_read(device, mode)
            device.write_key()
            with pytest.raises(OSError) as caught:
                await asyncio.wait_for(pending, 1)
            assert caught.value is error
        finally:
            device.close()

    asyncio.run(check())


@pytest.mark.parametrize("mode", ["read_one", "read", "loop"])
def test_active_read_still_delivers_event(mode):
    async def check():
        device = PipeEventIO()
        try:
            pending = start_read(device, mode)
            device.write_key()
            event = await asyncio.wait_for(pending, 1)
            if mode == "read":
                event = next(event)
            assert (event.type, event.code, event.value) == (ecodes.EV_KEY, ecodes.KEY_A, 1)
        finally:
            device.close()

    asyncio.run(check())
