"""Python bindings to certain linux input subsystem functions"""

def ioctl_devinfo(fd: int, /) -> tuple[int, int, int, int, str, str, str]:
    """fetch input device info"""

def ioctl_capabilities(
    fd: int, /
) -> dict[int, list[int | tuple[int, tuple[int, int, int, int, int, int]]]]:
    """fetch input device capabilities"""

def ioctl_EVIOCGABS(fd: int, ev_code: int, /) -> tuple[int, int, int, int, int, int]:
    """get input device absinfo"""

def ioctl_EVIOCSABS(
    fd: int,
    ev_code: int,
    absinfo: tuple[int, int, int, int, int, int],
    /,
) -> None:
    """set input device absinfo"""

def ioctl_EVIOCGREP(fd: int, /) -> tuple[int, int]: ...
def ioctl_EVIOCSREP(fd: int, delay: int, period: int, /) -> int: ...
def ioctl_EVIOCGVERSION(fd: int, /) -> int: ...
def ioctl_EVIOCGRAB(fd: int, flag: int, /) -> None: ...
def ioctl_EVIOCGEFFECTS(fd: int, /) -> int:
    """fetch the number of effects the device can keep in its memory."""

def ioctl_EVIOCG_bits(fd: int, evtype: int, /) -> list[int]:
    """get state of KEY|LED|SND|SW"""

def ioctl_EVIOCGPROP(fd: int, /) -> list[int]:
    """get device properties"""

def device_read(fd: int, /) -> tuple[int, int, int, int, int] | None:
    """read an input event from a device"""

def device_read_many(fd: int, /) -> tuple[tuple[int, int, int, int, int], ...]:
    """read all available input events from a device"""

def upload_effect(fd: int, effect_data: bytes, /) -> int: ...
def erase_effect(fd: int, ff_id: int, /) -> None: ...
