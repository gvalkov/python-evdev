# encoding: utf-8

'''
This module provides the :class:`InputEvent` class, which closely resembles the
`input_event` C struct in `linux/input.h`:

.. code-block:: c

    struct input_event {
        struct timeval time;
        __u16 type;
        __u16 code;
        __s32 value;
    };

This module also defines several abstractions on top of :class:`InputEvent`
that know more about the different event types (key, abs, rel etc). The
:data:`event_factory` dictionary maps event types to these classes.

Assuming you use the provided :func:`evdev.util.categorize()` function to
categorize events according to type, adding or replacing a class for a specific
event type becomes a matter of modifying :data:`event_factory`.

All of the provided classes have reasonable str() and repr() methods::

    >>> print(event)
    event at 1337197425.477827, code 04, type 04, val 458792
    >>> print(repr(event))
    InputEvent(1337197425L, 477827L, 4, 4, 458792L)

    >>> print(key_event)
    key event at 1337197425.477835, 28 (KEY_ENTER), up
    >>> print(repr(key_event))
    KeyEvent(InputEvent(1337197425L, 477835L, 1, 28, 0L))
'''

# event type descriptions have been taken mot-a-mot from:
# http://www.kernel.org/doc/Documentation/input/event-codes.txt

from evdev.ecodes import keys, KEY, SYN, REL, ABS, EV_KEY, EV_REL, EV_ABS, EV_SYN


class InputEvent(object):
    '''
    A generic input event. This closely resembles the input_event C struct.
    '''

    __slots__ = 'sec', 'usec', 'type', 'code', 'value'

    def __init__(self, sec, usec, type, code, value):
        #: Time in seconds since epoch at which event occurred
        self.sec  = sec

        #: Microsecond portion of the timestamp
        self.usec = usec

        #: Event type - one of ecodes.EV_*
        self.type = type

        #: Event code - probably one of :data:`evdev.ecodes.bytype`
        self.code = code

        #: Event value
        self.value = value

    def timestamp(self):
        ''' Return event timestamp as a python float. '''
        return self.sec + (self.usec / 1000000.0)

    def __str__(s):
        msg = 'event at {:f}, code {:02d}, type {:02d}, val {:02d}'
        return msg.format(s.timestamp(), s.code, s.type, s.value)

    def __repr__(s):
        msg = '{}({!r}, {!r}, {!r}, {!r}, {!r})'
        return msg.format(s.__class__.__name__,
                          s.sec, s.usec, s.type, s.code, s.value)


class KeyEvent(object):
    '''
    Used to describe state changes of keyboards, buttons, or other
    key-like devices.
    '''

    key_up   = 0x0
    key_down = 0x1
    key_hold = 0x2

    __slots__ = 'scancode', 'keycode', 'keystate', 'event'

    def __init__(self, event):
        if event.value == 0:
            self.keystate = KeyEvent.key_up
        elif event.value == 2:
            self.keystate = KeyEvent.key_hold
        elif event.value == 1:
            self.keystate = KeyEvent.key_down

        self.keycode  = keys[event.code]  # :todo:
        self.scancode = event.code

        #: :class:`InputEvent` instance
        self.event = event

    def __str__(self):
        try:    ks = ('up', 'down', 'hold')[self.keystate]
        except: ks = 'unknown'

        msg = 'key event at {:f}, {} ({}), {}'
        return msg.format(self.event.timestamp(),
                          self.scancode, self.keycode, ks)

    def __repr__(s):
        return '{}({!r})'.format(s.__class__.__name__, s.event)


class RelEvent(object):
    '''
    Used to describe relative axis value changes, e.g. moving the
    mouse 5 units to the left.
    '''

    __slots__ = 'event'

    def __init__(self, event):
        #: :class:`InputEvent` instance
        self.event = event

    def __str__(self):
        msg = 'relative axis event at {:f}, {} '
        return msg.format(self.event.timestamp(), REL[self.event.code])

    def __repr__(s):
        return '{}({!r})'.format(s.__class__.__name__, s.event)


class AbsEvent(object):
    '''
    Used to describe absolute axis value changes, e.g. describing the
    coordinates of a touch on a touchscreen.
    '''

    __slots__ = 'event'

    def __init__(self, event):
        #: :class:`InputEvent` instance
        self.event = event

    def __str__(self):
        msg = 'absolute axis event at {:f}, {} '
        return msg.format(self.event.timestamp(), ABS[self.event.code])

    def __repr__(s):
        return '{}({!r})'.format(s.__class__.__name__, s.event)


class SynEvent(object):
    '''
    Used as markers to separate events. Events may be separated in time or
    in space, such as with the multitouch protocol.
    '''

    __slots__ = 'event'

    def __init__(self, event):
        #: :class:`InputEvent` instance
        self.event = event

    def __str__(self):
        msg = 'synchronization event at {:f}, {} '
        return msg.format(self.event.timestamp(), SYN[self.event.code])

    def __repr__(s):
        return '{}({!r})'.format(s.__class__.__name__, s.event)


#: Used by :func:`evdev.util.categorize()`
event_factory = {
    EV_KEY: KeyEvent,
    EV_REL: RelEvent,
    EV_ABS: AbsEvent,
    EV_SYN: SynEvent,
}


__all__ = InputEvent, KeyEvent, RelEvent, SynEvent, AbsEvent, event_factory
