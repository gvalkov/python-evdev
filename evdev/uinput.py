# encoding: utf-8

import os
import stat
import time
from collections import defaultdict

from evdev import _uinput
from evdev import ecodes, util, device
from evdev.events import InputEvent
import evdev.ff as ff
import ctypes

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

        filtered_types : Tuple[event type codes]
          Event types to exclude from the capabilities of the uinput device.

        **kwargs
          Keyword arguments to UInput constructor (i.e. name, vendor etc.).
        '''

        # TODO: Move back to the argument list once Python 2 support is dropped.
        filtered_types = kwargs.pop('filtered_types', (ecodes.EV_SYN, ecodes.EV_FF))

        device_instances = []
        for dev in devices:
            if not isinstance(dev, device.InputDevice):
                dev = device.InputDevice(str(dev))
            device_instances.append(dev)

        all_capabilities = defaultdict(set)

        # Merge the capabilities of all devices into one dictionary.
        for dev in device_instances:
            for ev_type, ev_codes in dev.capabilities().items():
                all_capabilities[ev_type].update(ev_codes)

        for evtype in filtered_types:
            if evtype in all_capabilities:
                del all_capabilities[evtype]

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

        self._verify()

        #: Write-only, non-blocking file descriptor to the uinput device node.
        self.fd = _uinput.open(devnode)

        # Prepare the list of events for passing to _uinput.enable and _uinput.setup.
        absinfo, prepared_events = self._prepare_events(events)

        # Set phys name
        _uinput.set_phys(self.fd, phys)

        for etype, code in prepared_events:
            _uinput.enable(self.fd, etype, code)

        _uinput.setup(self.fd, name, vendor, product, version, bustype, absinfo)

        # Create the uinput device.
        _uinput.create(self.fd)

        self.dll = ctypes.CDLL(_uinput.__file__)
        self.dll._uinput_begin_upload.restype = ctypes.c_int
        self.dll._uinput_end_upload.restype = ctypes.c_int

        #: An :class:`InputDevice <evdev.device.InputDevice>` instance
        #: for the fake input device. ``None`` if the device cannot be
        #: opened for reading and writing.
        self.device = self._find_device()

    def _prepare_events(self, events):
        '''Prepare events for passing to _uinput.enable and _uinput.setup'''
        absinfo, prepared_events = [], []
        for etype, codes in events.items():
            for code in codes:
                # Handle max, min, fuzz, flat.
                if isinstance(code, (tuple, list, device.AbsInfo)):
                    # Flatten (ABS_Y, (0, 255, 0, 0, 0, 0)) to (ABS_Y, 0, 255, 0, 0, 0, 0).
                    f = [code[0]]
                    f.extend(code[1])
                    # Ensure the tuple is always 6 ints long, since uinput.c:uinput_create
                    # does little in the way of checking the length.
                    f.extend([0] * (6 - len(code[1])))
                    absinfo.append(f)
                    code = code[0]
                prepared_events.append((etype, code))
        return absinfo, prepared_events

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
            raise UInputError('input device not opened - cannot read capabilities')

        return self.device.capabilities(verbose, absinfo)

    def begin_upload(self, effect_id):
        upload = ff.UInputUpload()
        upload.effect_id = effect_id

        if self.dll._uinput_begin_upload(self.fd, ctypes.byref(upload)):
            raise UInputError('Failed to begin uinput upload: ' + os.strerror())

        return upload

    def end_upload(self, upload):
        if self.dll._uinput_end_upload(self.fd, ctypes.byref(upload)):
            raise UInputError('Failed to end uinput upload: ' + os.strerror())

    def begin_erase(self, effect_id):
        erase = ff.UInputErase()
        erase.effect_id = effect_id

        if self.dll._uinput_begin_erase(self.fd, ctypes.byref(erase)):
            raise UInputError('Failed to begin uinput erase: ' + os.strerror())
        return erase

    def end_erase(self, erase):
        if self.dll._uinput_end_erase(self.fd, ctypes.byref(erase)):
            raise UInputError('Failed to end uinput erase: ' + os.strerror())

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

        for path in util.list_devices('/dev/input/'):
            d = device.InputDevice(path)
            if d.name == self.name:
                return d
