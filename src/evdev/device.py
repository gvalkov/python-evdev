from __future__ import annotations

import contextlib
import os
from typing import TYPE_CHECKING, Any, Generic, Literal, NamedTuple, TypeVar, overload

from . import _input, ecodes, util


if TYPE_CHECKING:
    from collections.abc import Generator

    from . import ff
    from .eventio_async import EvdevError as EvdevError, EventIO

    _T = TypeVar('_T')
    _KeyT = TypeVar('_KeyT')
    _ValueT = TypeVar('_ValueT')
    _AbsKeyT = TypeVar('_AbsKeyT')
    _AbsValueT = TypeVar('_AbsValueT')

    class _Capabilities(dict['_KeyT | _AbsKeyT', '_ValueT | _AbsValueT']):
        @overload
        def __getitem__(self, key: _AbsKeyT, /) -> _AbsValueT: ...  # pyright: ignore[reportNoOverloadImplementation]
        @overload
        def __getitem__(self, key: _KeyT, /) -> _ValueT: ...
        @overload
        def __getitem__(self, key: _KeyT | _AbsKeyT, /) -> _AbsValueT | _ValueT: ...
        def __getitem__(self, key: Any, /) -> Any: ...
        @overload  # type: ignore[override]
        def get(self, key: _AbsKeyT, default: None = None, /) -> _AbsValueT | None: ...  # pyright: ignore[reportNoOverloadImplementation]
        @overload
        def get(self, key: _KeyT, default: None = None, /) -> _ValueT | None: ...
        @overload
        def get(self, key: _KeyT | _AbsKeyT, default: None = None, /) -> _AbsValueT | _ValueT | None: ...
        @overload
        def get(self, key: _AbsKeyT, default: _AbsValueT | _T, /) -> _AbsValueT | _T: ...
        @overload
        def get(self, key: _KeyT, default: _ValueT | _T, /) -> _ValueT | _T: ...
        @overload
        def get(self, key: _KeyT | _AbsKeyT, default: _AbsValueT | _ValueT | _T, /) -> _AbsValueT | _ValueT | _T: ...
        def get(self, key: Any, default: Any = None, /) -> Any: ...  # pyright: ignore[reportIncompatibleMethodOverride]

    class _AbsInfoCapabilities(
        _Capabilities[
            ecodes._CapabilitiesKeys,
            ecodes._CapabilitiesAbsKeys,
            list[int],
            list[tuple[int, 'AbsInfo']]
        ]
    ): ...

    class _VerboseAbsInfoCapabilities(
        _Capabilities[
            ecodes._CapabilitiesVerboseKeys,
            ecodes._CapabilitiesVerboseAbsKeys,
            list[tuple[str, int]],
            list[tuple[tuple[str, int], 'AbsInfo']],
        ]
    ): ...
else:
    try:
        from .eventio_async import EvdevError as EvdevError, EventIO
    except ImportError:
        from .eventio import EvdevError as EvdevError, EventIO

    _Capabilities = dict
    _AbsInfoCapabilities = dict
    _VerboseAbsInfoCapabilities = dict

_AnyStr = TypeVar("_AnyStr", str, bytes)


class AbsInfo(NamedTuple):
    """Absolute axis information.

    A ``namedtuple`` with absolute axis information -
    corresponds to the ``input_absinfo`` struct:

    Attributes
    ---------
    value
      Latest reported value for the axis.

    min
      Specifies minimum value for the axis.

    max
      Specifies maximum value for the axis.

    fuzz
      Specifies fuzz value that is used to filter noise from the
      event stream.

    flat
      Values that are within this value will be discarded by joydev
      interface and reported as 0 instead.

    resolution
      Specifies resolution for the values reported for the axis.
      Resolution for main axes (``ABS_X, ABS_Y, ABS_Z``) is reported
      in units per millimeter (units/mm), resolution for rotational
      axes (``ABS_RX, ABS_RY, ABS_RZ``) is reported in units per
      radian.

    Note
    ----
    The input core does not clamp reported values to the ``[minimum,
    maximum]`` limits, such task is left to userspace.

    """

    value: int
    min: int
    max: int
    fuzz: int
    flat: int
    resolution: int

    def __str__(self):
        return "value {}, min {}, max {}, fuzz {}, flat {}, res {}".format(*self)  # pylint: disable=not-an-iterable


class KbdInfo(NamedTuple):
    """Keyboard repeat rate.

    Attributes
    ----------
    delay
      Amount of time that a key must be depressed before it will start
      to repeat (in milliseconds).

    repeat
      Keyboard repeat rate in characters per second.
    """

    delay: int
    repeat: int

    def __str__(self):
        return f"delay {self.delay}, repeat {self.repeat}"


class DeviceInfo(NamedTuple):
    """
    Attributes
    ----------
    bustype
    vendor
    product
    version
    """

    bustype: int
    vendor: int
    product: int
    version: int

    def __str__(self) -> str:
        msg = "bus: {:04x}, vendor {:04x}, product {:04x}, version {:04x}"
        return msg.format(*self)  # pylint: disable=not-an-iterable


class InputDevice(EventIO, Generic[_AnyStr]):
    """
    A linux input device from which input events can be read.
    """

    __slots__ = ("path", "fd", "info", "name", "phys", "uniq", "_rawcapabilities", "version", "ff_effects_count")

    def __init__(self, dev: _AnyStr | os.PathLike[_AnyStr]) -> None:
        """
        Arguments
        ---------
        dev : str|bytes|PathLike
          Path to input device
        """

        #: Path to input device.
        self.path: _AnyStr = dev if isinstance(dev, (str, bytes)) else dev.__fspath__()

        # Certain operations are possible only when the device is opened in read-write mode.
        try:
            fd = os.open(dev, os.O_RDWR | os.O_NONBLOCK)
        except OSError:
            fd = os.open(dev, os.O_RDONLY | os.O_NONBLOCK)

        #: A non-blocking file descriptor to the device file.
        self.fd: int = fd

        # Returns (bustype, vendor, product, version, name, phys, capabilities).
        info_res = _input.ioctl_devinfo(self.fd)

        #: A :class:`DeviceInfo <evdev.device.DeviceInfo>` instance.
        self.info = DeviceInfo(*info_res[:4])

        #: The name of the event device.
        self.name: str = info_res[4]

        #: The physical topology of the device.
        self.phys: str = info_res[5]

        #: The unique identifier of the device.
        self.uniq: str = info_res[6]

        #: The evdev protocol version.
        self.version: int = _input.ioctl_EVIOCGVERSION(self.fd)

        #: The raw dictionary of device capabilities - see `:func:capabilities()`.
        self._rawcapabilities = _input.ioctl_capabilities(self.fd)

        #: The number of force feedback effects the device can keep in its memory.
        self.ff_effects_count = _input.ioctl_EVIOCGEFFECTS(self.fd)

    def __del__(self) -> None:
        if hasattr(self, "fd") and self.fd is not None:
            try:
                self.close()
            except (OSError, ImportError, AttributeError):
                pass

    @overload
    def _capabilities(self, absinfo: Literal[True] = ...) -> _AbsInfoCapabilities: ...
    @overload
    def _capabilities(self, absinfo: Literal[False]) -> dict[int, list[int]]: ...
    @overload
    def _capabilities(self, absinfo: bool) -> _AbsInfoCapabilities | dict[int, list[int]]: ...
    def _capabilities(self, absinfo: bool = True) -> _AbsInfoCapabilities | dict[int, list[int]]:
        res: dict[Any, Any] = {}

        for etype, _ecodes in self._rawcapabilities.items():
            for code in _ecodes:
                l = res.setdefault(etype, [])
                if isinstance(code, tuple):
                    if absinfo:
                        a = code[1]  # (0, 0, 0, 255, 0, 0)
                        i = AbsInfo(*a)
                        l.append((code[0], i))
                    else:
                        l.append(code[0])
                else:
                    l.append(code)

        return res

    @overload
    def capabilities(
        self, verbose: Literal[False] = ..., absinfo: Literal[True] = ...
    ) -> _AbsInfoCapabilities: ...
    @overload
    def capabilities(
        self, verbose: Literal[False], absinfo: Literal[False]
    ) -> dict[int, list[int]]: ...
    @overload
    def capabilities(
        self, verbose: Literal[True], absinfo: Literal[True] = ...
    ) -> _VerboseAbsInfoCapabilities: ...
    @overload
    def capabilities(
        self, verbose: Literal[True], absinfo: Literal[False]
    ) -> dict[tuple[str, int], list[tuple[str, int]]]: ...
    @overload
    def capabilities(self, verbose: bool = False, absinfo: bool = True) -> (
        _AbsInfoCapabilities
        | dict[int, list[int]]
        | _VerboseAbsInfoCapabilities
        | dict[tuple[str, int], list[tuple[str, int]]]
    ): ...
    def capabilities(
        self, verbose: bool = False, absinfo: bool = True
    ) -> (
        _AbsInfoCapabilities
        | dict[int, list[int]]
        | _VerboseAbsInfoCapabilities
        | dict[tuple[str, int], list[tuple[str, int]]]
    ):
        """
        Return the event types that this device supports as a mapping of
        supported event types to lists of handled event codes.

        Example
        --------
        >>> device.capabilities()
        { 1: [272, 273, 274],
          2: [0, 1, 6, 8] }

        If ``verbose`` is ``True``, event codes and types will be resolved
        to their names.

        ::

          { ('EV_KEY', 1): [('BTN_MOUSE', 272),
                            ('BTN_RIGHT', 273),
                            ('BTN_MIDDLE', 273)],
            ('EV_REL', 2): [('REL_X', 0),
                            ('REL_Y', 1),
                            ('REL_HWHEEL', 6),
                            ('REL_WHEEL', 8)] }

        Unknown codes or types will be resolved to ``'?'``.

        If ``absinfo`` is ``True``, the list of capabilities will also
        include absolute axis information in the form of
        :class:`AbsInfo` instances::

          { 3: [ (0, AbsInfo(min=0, max=255, fuzz=0, flat=0)),
                 (1, AbsInfo(min=0, max=255, fuzz=0, flat=0)) ]}

        Combined with ``verbose`` the above becomes::

          { ('EV_ABS', 3): [ (('ABS_X', 0), AbsInfo(min=0, max=255, fuzz=0, flat=0)),
                             (('ABS_Y', 1), AbsInfo(min=0, max=255, fuzz=0, flat=0)) ]}

        """

        if verbose:
            return dict(util.resolve_ecodes_dict(self._capabilities(absinfo)))
        else:
            return self._capabilities(absinfo)

    @overload
    def input_props(
        self, verbose: Literal[False] = ...
    ) -> list[int]: ...
    @overload
    def input_props(
        self, verbose: Literal[True]
    ) -> list[tuple[str | tuple[str, ...], int]]: ...
    @overload
    def input_props(
        self, verbose: bool
    ) -> list[int] | list[tuple[str | tuple[str, ...], int]]: ...
    def input_props(
        self, verbose: bool = False
    ) -> list[int] | list[tuple[str | tuple[str, ...], int]]:
        """
        Get device properties and quirks.

        Example
        -------
        >>> device.input_props()
        [0, 5]

        If ``verbose`` is ``True``, input properties are resolved to their
        names. Unknown codes are resolved to ``'?'``::

        [('INPUT_PROP_POINTER', 0), ('INPUT_PROP_POINTING_STICK', 5)]

        """
        props = _input.ioctl_EVIOCGPROP(self.fd)
        if verbose:
            return util.resolve_ecodes(ecodes.INPUT_PROP, props)

        return props

    @overload
    def leds(self, verbose: Literal[False] = ...) -> list[int]: ...
    @overload
    def leds(self, verbose: Literal[True]) -> list[tuple[str | tuple[str, ...], int]]: ...
    @overload
    def leds(self, verbose: bool) -> list[int] | list[tuple[str | tuple[str, ...], int]]: ...
    def leds(self, verbose: bool = False) -> list[int] | list[tuple[str | tuple[str, ...], int]]:
        """
        Return currently set LED keys.

        Example
        -------
        >>> device.leds()
        [0, 1, 8, 9]

        If ``verbose`` is ``True``, event codes are resolved to their
        names. Unknown codes are resolved to ``'?'``::

        [('LED_NUML', 0), ('LED_CAPSL', 1), ('LED_MISC', 8), ('LED_MAIL', 9)]

        """
        leds = _input.ioctl_EVIOCG_bits(self.fd, ecodes.EV_LED)
        if verbose:
            return util.resolve_ecodes(ecodes.LED, leds)

        return leds

    def set_led(self, led_num: int, value: int) -> None:
        """
        Set the state of the selected LED.

        Example
        -------
        >>> device.set_led(ecodes.LED_NUML, 1)
        """
        self.write(ecodes.EV_LED, led_num, value)

    def __eq__(self, other: object) -> bool:
        """
        Two devices are equal if their :data:`info` attributes are equal.
        """
        return isinstance(other, self.__class__) and self.info == other.info and self.path == other.path

    def __str__(self) -> str:
        msg = 'device {}, name "{}", phys "{}", uniq "{}"'
        return msg.format(self.path, self.name, self.phys, self.uniq or "")

    def __repr__(self) -> str:
        msg = (self.__class__.__name__, self.path)
        return "{}({!r})".format(*msg)

    def __fspath__(self) -> _AnyStr:
        return self.path

    def close(self) -> None:
        if self.fd > -1:
            try:
                super().close()
                os.close(self.fd)
            finally:
                self.fd = -1

    def grab(self) -> None:
        """
        Grab input device using ``EVIOCGRAB`` - other applications will
        be unable to receive events until the device is released. Only
        one process can hold a ``EVIOCGRAB`` on a device.

        Warning
        -------
        Grabbing an already grabbed device will raise an ``OSError``.
        """

        _input.ioctl_EVIOCGRAB(self.fd, 1)

    def ungrab(self) -> None:
        """
        Release device if it has been already grabbed (uses `EVIOCGRAB`).

        Warning
        -------
        Releasing an already released device will raise an
        ``OSError('Invalid argument')``.
        """

        _input.ioctl_EVIOCGRAB(self.fd, 0)

    @contextlib.contextmanager
    def grab_context(self) -> Generator[None]:
        """
        A context manager for the duration of which only the current
        process will be able to receive events from the device.
        """
        self.grab()
        yield
        self.ungrab()

    def upload_effect(self, effect: ff.Effect) -> int:
        """
        Upload a force feedback effect to a force feedback device.
        """

        data = memoryview(effect).tobytes()
        ff_id = _input.upload_effect(self.fd, data)
        return ff_id

    def erase_effect(self, ff_id: int) -> None:
        """
        Erase a force effect from a force feedback device. This also
        stops the effect.
        """

        _input.erase_effect(self.fd, ff_id)

    @property
    def repeat(self) -> KbdInfo:
        """
        Get or set the keyboard repeat rate (in characters per
        minute) and delay (in milliseconds).
        """

        return KbdInfo(*_input.ioctl_EVIOCGREP(self.fd))  # pylint: disable=not-an-iterable

    @repeat.setter
    def repeat(self, value: tuple[int, int]) -> None:
        _input.ioctl_EVIOCSREP(self.fd, *value)

    @overload
    def active_keys(
        self, verbose: Literal[False] = ...
    ) -> list[int]: ...
    @overload
    def active_keys(
        self, verbose: Literal[True]
    ) -> list[tuple[str | tuple[str, ...], int]]: ...
    @overload
    def active_keys(
        self, verbose: bool
    ) -> list[int] | list[tuple[str | tuple[str, ...], int]]: ...
    def active_keys(
        self, verbose: bool = False
    ) -> list[int] | list[tuple[str | tuple[str, ...], int]]:
        """
        Return currently active keys.

        Example
        -------

        >>> device.active_keys()
        [1, 42]

        If ``verbose`` is ``True``, key codes are resolved to their
        verbose names. Unknown codes are resolved to ``'?'``. For
        example::

          [('KEY_ESC', 1), ('KEY_LEFTSHIFT', 42)]

        """
        active_keys = _input.ioctl_EVIOCG_bits(self.fd, ecodes.EV_KEY)
        if verbose:
            return util.resolve_ecodes(ecodes.KEY, active_keys)

        return active_keys

    def absinfo(self, axis_num: int) -> AbsInfo:
        """
        Return current :class:`AbsInfo` for input device axis

        Arguments
        ---------
        axis_num : int
          EV_ABS keycode (example :attr:`ecodes.ABS_X`)

        Example
        -------
        >>> device.absinfo(ecodes.ABS_X)
        AbsInfo(value=1501, min=-32768, max=32767, fuzz=0, flat=128, resolution=0)
        """
        return AbsInfo(*_input.ioctl_EVIOCGABS(self.fd, axis_num))

    def set_absinfo(
        self,
        axis_num: int,
        value: int | None = None,
        min: int | None = None,
        max: int | None = None,
        fuzz: int | None = None,
        flat: int | None = None,
        resolution: int | None = None
    ) -> None:
        """
        Update :class:`AbsInfo` values. Only specified values will be overwritten.

        Arguments
        ---------
        axis_num : int
          EV_ABS keycode (example :attr:`ecodes.ABS_X`)

        Example
        -------
        >>> device.set_absinfo(ecodes.ABS_X, min=-2000, max=2000)

        You can also unpack AbsInfo tuple that will overwrite all values

        >>> device.set_absinfo(ecodes.ABS_Y, *AbsInfo(0, -2000, 2000, 0, 15, 0))
        """

        cur_absinfo = self.absinfo(axis_num)
        new_absinfo = AbsInfo(
            value if value is not None else cur_absinfo.value,
            min if min is not None else cur_absinfo.min,
            max if max is not None else cur_absinfo.max,
            fuzz if fuzz is not None else cur_absinfo.fuzz,
            flat if flat is not None else cur_absinfo.flat,
            resolution if resolution is not None else cur_absinfo.resolution,
        )
        _input.ioctl_EVIOCSABS(self.fd, axis_num, new_absinfo)
