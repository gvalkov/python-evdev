# encoding: utf-8

import os
import stat
import time

from evdev import _uinput
from evdev import ecodes, util, device
from evdev.events import InputEvent

try:
    from evdev.eventio_async import EventIO
except ImportError:
    from evdev.eventio import EventIO



class UInputError(Exception):
    pass


class UInput(EventIO):
    '''
    A userland input device and that can inject input events into the
    linux input subsystem.
    '''

    __slots__ = (
        'name', 'vendor', 'product', 'version', 'bustype',
        'events', 'devnode', 'fd', 'device',
    )

    @classmethod
    def from_device(cls, *devices, **kwargs):
        '''
        Create an UInput device with the capabilities of one or more input
        devices.

        Arguments
        ---------
        devices : InputDevice|str
          Varargs of InputDevice instances or paths to input devices.

        **kwargs
          Keyword arguments to UInput constructor (i.e. name, vendor etc.).
        '''

        device_instances = []
        for dev in devices:
            if not isinstance(dev, device.InputDevice):
                dev = device.InputDevice(str(dev))
            device_instances.append(dev)

        all_capabilities = {}
        for dev in device_instances:
            all_capabilities.update(dev.capabilities())

        del all_capabilities[ecodes.EV_SYN]

        return cls(events=all_capabilities, **kwargs)

    def __init__(self,
                 events=None,
                 name='py-evdev-uinput',
                 vendor=0x1, product=0x1, version=0x1, bustype=0x3,
                 devnode='/dev/uinput', phys='py-evdev-uinput'):
        '''
        Arguments
        ---------
        events : dict
          Dictionary of event types mapping to lists of event codes. The
          event types and codes that the uinput device will be able to
          inject - defaults to all key codes.

        name
          The name of the input device.

        vendor
          Vendor identifier.

        product
          Product identifier.

        version
          version identifier.

        bustype
          bustype identifier.

        phys
          physical path.

        Note
        ----
        If you do not specify any events, the uinput device will be able
        to inject only ``KEY_*`` and ``BTN_*`` event codes.
        '''

        self.name = name         #: Uinput device name.
        self.vendor = vendor     #: Device vendor identifier.
        self.product = product   #: Device product identifier.
        self.version = version   #: Device version identifier.
        self.bustype = bustype   #: Device bustype - e.g. ``BUS_USB``.
        self.phys    = phys      #: Uinput device physical path.
        self.devnode = devnode   #: Uinput device node - e.g. ``/dev/uinput/``.

        if not events:
            events = {ecodes.EV_KEY: ecodes.keys.keys()}

        # The min, max, fuzz and flat values for the absolute axis for
        # a given code.
        absinfo = []

        self._verify()

        #: Write-only, non-blocking file descriptor to the uinput device node.
        self.fd = _uinput.open(devnode)

        # Set phys name
        _uinput.set_phys(self.fd, phys)

        # Set device capabilities.
        for etype, codes in events.items():
            for code in codes:
                # Handle max, min, fuzz, flat.
                if isinstance(code, (tuple, list, device.AbsInfo)):
                    # Flatten (ABS_Y, (0, 255, 0, 0, 0, 0)) to (ABS_Y, 0, 255, 0, 0, 0, 0).
                    f = [code[0]]; f += code[1]
                    absinfo.append(f)
                    code = code[0]

                # TODO: a lot of unnecessary packing/unpacking
                _uinput.enable(self.fd, etype, code)

        # Create the uinput device.
        _uinput.create(self.fd, name, vendor, product, version, bustype, absinfo)

        #: An :class:`InputDevice <evdev.device.InputDevice>` instance
        #: for the fake input device. ``None`` if the device cannot be
        #: opened for reading and writing.
        self.device = self._find_device()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if hasattr(self, 'fd'):
            self.close()

    def __repr__(self):
        # TODO:
        v = (repr(getattr(self, i)) for i in
             ('name', 'bustype', 'vendor', 'product', 'version', 'phys'))
        return '{}({})'.format(self.__class__.__name__, ', '.join(v))

    def __str__(self):
        msg = ('name "{}", bus "{}", vendor "{:04x}", product "{:04x}", version "{:04x}", phys "{}"\n'
               'event types: {}')

        evtypes = [i[0] for i in self.capabilities(True).keys()]
        msg = msg.format(self.name, ecodes.BUS[self.bustype],
                         self.vendor, self.product,
                         self.version, self.phys, ' '.join(evtypes))

        return msg

    def close(self):
        # Close the associated InputDevice, if it was previously opened.
        if self.device is not None:
            self.device.close()

        # Destroy the uinput device.
        if self.fd > -1:
            _uinput.close(self.fd)
            self.fd = -1

    def syn(self):
        '''
        Inject a ``SYN_REPORT`` event into the input subsystem. Events
        queued by :func:`write()` will be fired. If possible, events
        will be merged into an 'atomic' event.
        '''

        _uinput.write(self.fd, ecodes.EV_SYN, ecodes.SYN_REPORT, 0)

    def capabilities(self, verbose=False, absinfo=True):
        '''See :func:`capabilities <evdev.device.InputDevice.capabilities>`.'''
        if self.device is None:
            raise UInputError('input device not opened - cannot read capabilites')

        return self.device.capabilities(verbose, absinfo)

    def _verify(self):
        '''
        Verify that an uinput device exists and is readable and writable
        by the current process.
        '''

        try:
            m = os.stat(self.devnode)[stat.ST_MODE]
            if not stat.S_ISCHR(m):
                raise
        except (IndexError, OSError):
            msg = '"{}" does not exist or is not a character device file '\
                  '- verify that the uinput module is loaded'
            raise UInputError(msg.format(self.devnode))

        if not os.access(self.devnode, os.W_OK):
            msg = '"{}" cannot be opened for writing'
            raise UInputError(msg.format(self.devnode))

        if len(self.name) > _uinput.maxnamelen:
            msg = 'uinput device name must not be longer than {} characters'
            raise UInputError(msg.format(_uinput.maxnamelen))

    def _find_device(self):
        #:bug: the device node might not be immediately available
        time.sleep(0.1)

        for fn in util.list_devices('/dev/input/'):
            d = device.InputDevice(fn)
            if d.name == self.name:
                return d
