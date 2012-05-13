# encoding: utf-8

import os
import stat

from evdev import _uinput
from evdev import ecodes


class UInputError(Exception):
    pass


class UInput(object):
    '''
    I represent a linux userland input (uinput) device and am capapble of
    injecting input events into the input subsystem.
    '''

    __slots__ = (
        'name', 'vendor', 'product', 'version',
        'mouserel', 'mouseabs', 'keys', 'fn', 'fd',
    )

    def __init__(self, name, vendor, product, version,
                 mouserel=True, mouseabs=False,
                 keys=True, fn='/dev/uinput'):
        '''
        :param name:    the name of the input device
        :param vendor:  todo
        :param product: todo
        :param version: todo
        '''

        self.name = name
        self.vendor = vendor
        self.product = product
        self.version = version

        self.mouserel = mouserel
        self.mouseabs = mouseabs

        self.keys = keys
        self.fn = fn

        self.verify()

        self.fd = self.open()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def __repr__(self):
        v = (repr(getattr(self, i)) for i in self.__slots__)
        return '{}({})'.format(self.__class__.__name__, ', '.join(v))

    def open(self):
        args = (self.name, self.vendor, self.product, self.version, self.fn)
        uidev_fd = _uinput.open(*args)
        return uidev_fd

    def close(self):
        if self.fd and self.fd > 0:
            _uinput.close(self.fd)

    def write(self, event):
        '''
        Inject an input event into the input subsystem. Events are queued by
        until a synchronization event is received.

        :param event: InputEvent instance or an object with an `event`
                      attribute (KeyEvent, RelEvent etc)
        '''

        if hasattr(event, 'event'):
            event = event.event

        _uinput.write(self.fd, event.type, event.code, event.value)

    def syn(self):
        '''
        Inject a SYN_REPORT event into the input subsystem. Events queued by
        :func:`write()` will be fired. If applicable, events will be merged
        into an 'atomic' event.
        '''

        _uinput.write(self.fd, ecodes.EV_SYN, ecodes.SYN_REPORT, 0)

    def verify(self):
        '''
        Verify that a uinput device exists and is readable and writable
        by our process .
        '''

        try:
            m = os.stat(self.fn)[stat.ST_MODE]
            if not stat.S_ISCHR(m):
                raise
        except:
            msg = '"{}" does not exist or is not a character device file '\
                  '- verify that the uinput module is loaded'
            raise UInputError(msg.format(self.fn))

        if not os.access(self.fn, os.W_OK):
            msg = '"{}" cannot be opened for writing'
            raise UInputError(msg.format(self.fn))

        if len(self.name) > _uinput.maxnamelen:
            msg = 'uinput device name must not be longer than {} characters'
            raise UInputError(msg.format(_uinput.maxnamelen))
