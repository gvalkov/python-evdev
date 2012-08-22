# encoding: utf-8

import os
from collections import namedtuple

from evdev import _input, ecodes, util
from evdev.events import InputEvent


class DeviceInfo(object):
    __slots__ = 'bustype', 'product', 'vendor', 'version'

    def __init__(self, bustype, vendor, product, version):
        self.bustype = bustype
        self.vendor  = vendor
        self.product = product
        self.version = version

    def __str__(self):
        msg = 'bus: {:04x}, product {:04x}, vendor {:04x}, version {:04x}'
        return msg.format(self.bustype, self.product, self.vendor, self.version)

    def __repr__(s):
        msg = (s.__class__.__name__, s.bustype, s.vendor, s.product, s.version)
        return '{}({:04x}, {:04x}, {:04x}, {:04x})'.format(*msg)

    def __eq__(self, o):
        return self.bustype == o.bustype \
           and self.vendor  == o.vendor  \
           and self.product == o.product \
           and self.version == o.version



_AbsInfo = namedtuple('AbsInfo',
                     ['min', 'max', 'fuzz', 'flat'])

class AbsInfo(_AbsInfo):
    pass


class InputDevice(object):
    '''
    A linux input device from which input events can be read.
    '''

    __slots__ = 'fn', 'nophys', 'fd', 'info', 'name', 'phys', '_rawcapabilities'

    def __init__(self, dev, nophys=False):
        '''
        :param dev: path to input device
        :param nophys: do not do a ``EVIOCGPHYS`` ioctl (needed by uinput)
        '''

        #: Path to input device
        self.fn = dev
        self.nophys = nophys

        #: A non-blocking file descriptor to the device file
        self.fd = os.open(dev, os.O_RDONLY | os.O_NONBLOCK)

        # Returns (bustype, vendor, product, version, name, phys, capabilities)
        info_res  = _input.ioctl_devinfo(self.fd, nophys)

        #: A :class:`DeviceInfo <evdev.device.DeviceInfo>` instance
        self.info = DeviceInfo(*info_res[:4])

        #: The name of the event device
        self.name = info_res[4]

        #: The physical topology of the device
        self.phys = info_res[5] if not nophys else ''
        self._rawcapabilities = info_res[6]

    def _capabilities(self, absinfo=True):
        res = {}
        for etype, ecodes in self._rawcapabilities.items():
            for code in ecodes:
                l = res.setdefault(etype, [])
                if isinstance(code, tuple):
                    if absinfo:
                        a = code[1]  # (0, 0, 255, 0)
                        i = AbsInfo(min=a[1], max=a[2], fuzz=a[3], flat=a[4])
                        l.append((code[0], i))
                    else:
                        l.append(code[0])
                else:
                    l.append(code)

        return res

    def capabilities(self, verbose=False, absinfo=True):
        '''
        Returns the event types that this device supports as a a mapping of
        supported event types to lists of handled event codes. Example::

          { 1: [272, 273, 274],
            2: [0, 1, 6, 8] }

        If ``verbose`` is ``True``, event codes and types will be resolved
        to their names. Example::

          { ('EV_KEY', 1) : [('BTN_MOUSE', 272), ('BTN_RIGHT', 273), ('BTN_MIDDLE', 273)],
            ('EV_REL', 2) : [('REL_X', 0), ('REL_Y', 0), ('REL_HWHEEL', 6), ('REL_WHEEL', 8)] }

        Unknown codes or types will be resolved to '?'.

        If ``absinfo`` is ``True``, the list of capabilities will also
        include absolute axis information (``absmin``, ``absmax``,
        ``absfuzz``, ``absflat``) in the following form::

          { 3 : [ (0, AbsInfo(min=0, max=255, fuzz=0, flat=0)),
                  (1, AbsInfo(min=0, max=255, fuzz=0, flat=0)) ]}

        Combined with ``verbose`` the above becomes::

          { ('EV_ABS', 3) : [ (('ABS_X', 0), AbsInfo(min=0, max=255, fuzz=0, flat=0)),
                              (('ABS_Y', 1), AbsInfo(min=0, max=255, fuzz=0, flat=0)) ]}

        '''

        if verbose:
            return dict(util.resolve_ecodes(self._capabilities(absinfo)))
        else:
            return self._capabilities(absinfo)

    def __eq__(self, o):
        ''' Two devices are considered equal if their :data:`info` attributes are equal. '''
        return self.info == o.info

    def __str__(self):
        msg = 'device {}, name "{}", phys "{}"'
        return msg.format(self.fn, self.name, self.phys)

    def __repr__(self):
        msg = (self.__class__.__name__, self.fn, self.nophys)
        return '{}({!r}, {})'.format(*msg)

    def close(self):
        os.close(self.fd)
        self.fd = -1

    def fileno(self):
        '''
        Returns the file descriptor to the event device. This makes
        passing ``InputDevice`` instances directly to
        :func:`select.select()` and :class:`asyncore.file_dispatcher`
        possible. '''

        return self.fd

    def read_one(self):
        '''
        Read and return a single input event as a
        :class:`InputEvent <evdev.events.InputEvent>` instance.

        Return `None` if there are no pending input events.
        '''

        # event -> (sec, usec, type, code, val)
        event = _input.device_read(self.fd)

        if event:
            return InputEvent(*event)

    def read(self):
        '''
        Read multiple input events from device. This function returns a
        generator object that yields :class:`InputEvent
        <evdev.events.InputEvent>` instances.  '''

        # events -> [(sec, usec, type, code, val), ...]
        events = _input.device_read_many(self.fd)

        for i in events:
            yield InputEvent(*i)
