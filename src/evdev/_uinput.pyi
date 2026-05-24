"""Python bindings for parts of linux/uinput.c."""

from typing import Final

maxnamelen: Final[int]

def open(devnode: str, /) -> int:
    """Open uinput device node."""

def setup(
    fd: int,
    name: str,
    vendor: int,
    product: int,
    version: int,
    bustype: int,
    absinfo: list[list[int]],
    max_effects: int,
    /,
) -> None:
    """Set an uinput device up."""

def create(fd: int, /) -> None:
    """Create an uinput device."""

def close(fd: int, /) -> None:
    """Destroy uinput device."""

def write(fd: int, type: int, code: int, value: int, /) -> None:
    """Write event to uinput device."""

def enable(fd: int, type: int, code: int, /) -> None:
    """Enable a type of event."""

def set_phys(fd: int, phys: str, /) -> None:
    """Set physical path"""

def get_sysname(fd: int, /) -> str:
    """Obtain the sysname of the uinput device."""

def set_prop(fd: int, prop: int, /) -> None:
    """Set device input property"""
