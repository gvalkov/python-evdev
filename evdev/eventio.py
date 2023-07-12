# encoding: utf-8

import os
import fcntl
import select
import functools

from evdev import _input, _uinput, ecodes, util
from evdev.events import InputEvent

#--------------------------------------------------------------------------
class EvdevError(Exception):
    pass


class EventIO:
    '''
    Base class for reading and writing input events.

    This class is used by :class:`InputDevice` and :class:`UInput`.

    - On, :class:`InputDevice` it used for reading user-generated events (e.g.
      key presses, mouse movements) and writing feedback events (e.g. leds,
      beeps).

    - On, :class:`UInput` it used for writing user-generated events (e.g.
      key presses, mouse movements) and reading feedback events (e.g. leds,
      beeps).
    '''

    def fileno(self):
        '''
        Return the file descriptor to the open event device. This makes
        it possible to pass instances directly to :func:`select.select()` and
        :class:`asyncore.file_dispatcher`.
        '''
        return self.fd

    def read_loop(self):
        '''
        Enter an endless :func:`select.select()` loop that yields input events.
        '''

        while True:
            r, w, x = select.select([self.fd], [], [])
            for event in self.read():
                yield event

    def read_loop_blockless(self, timeout=0.001):
        '''
        Enter a blockless :func:`select.select()` loop that yields input events endlessly.

        It is different from its blocking counterpart because it does not stop the execution when the device is
        idle, instead it replicates the previous event until another one happens. This is made possible by
        making use of a custom :func: 'read_one_blockless()' function that doesn't raise 'BlockingIOError' if there
        are no available events at the moment.
        '''
        
        # previous_event -> InputEvent.sec, InputEvent.usec, InputEvent.type, InputEvent.code, InputEvent.val
        previous_event = InputEvent(sec=0, usec=0, type=0, code=0, value=0)
        
        # flag for 0 / SynEvent type value
        syn_event = 0
                
        def read_one_blockless(previous_event):
            '''
            Read and yield a single input event as an instance of :class:`InputEvent <evdev.events.InputEvent>`.

            Return previous event as an instance of :class:`InputEvent <evdev.events.InputEvent>` if there are
            no pending input events.
            '''
        
            # current_event -> (sec, usec, type, code, val)
            current_event = _input.device_read(self.fd)

            if current_event == None:
                return previous_event

            # transforming result of device_read into an InputEvent        
            current_event = InputEvent(*current_event)

            if current_event.type == syn_event:
                current_event = InputEvent(current_event.sec, current_event.usec, previous_event.type, previous_event.code, previous_event.value)
                return current_event

            # returns current_event as InputEvent containing new data if none of the above applies    
            return current_event

        while True:
            # selecting device and setting timeout value, thus allowing non-blocking feature and replication rate control
            select.select([self.fd], [], [], timeout)
        
            # event -> InputEvent.sec, InputEvent.usec, InputEvent.type, InputEvent.code, InputEvent.value
            current_event = read_one_blockless(previous_event)
            
            # updating previous event with current event data
            previous_event = current_event
            yield current_event
                
    def read_one(self):
        '''
        Read and return a single input event as an instance of
        :class:`InputEvent <evdev.events.InputEvent>`.

        Return ``None`` if there are no pending input events.
        '''

        # event -> (sec, usec, type, code, val)
        event = _input.device_read(self.fd)

        if event:
            return InputEvent(*event)

    def read(self):
        '''
        Read multiple input events from device. Return a generator object that
        yields :class:`InputEvent <evdev.events.InputEvent>` instances. Raises
        `BlockingIOError` if there are no available events at the moment.
        '''

        # events -> [(sec, usec, type, code, val), ...]
        events = _input.device_read_many(self.fd)

        for event in events:
            yield InputEvent(*event)

    def need_write(func):
        '''
        Decorator that raises :class:`EvdevError` if there is no write access to the
        input device.
        '''
        @functools.wraps(func)
        def wrapper(*args):
            fd = args[0].fd
            if fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_RDWR:
                return func(*args)
            msg = 'no write access to device "%s"' % args[0].path
            raise EvdevError(msg)
        return wrapper

    def write_event(self, event):
        '''
        Inject an input event into the input subsystem. Events are
        queued until a synchronization event is received.

        Arguments
        ---------
        event: InputEvent
          InputEvent instance or an object with an ``event`` attribute
          (:class:`KeyEvent <evdev.events.KeyEvent>`, :class:`RelEvent
          <evdev.events.RelEvent>` etc).

        Example
        -------
        >>> ev = InputEvent(1334414993, 274296, ecodes.EV_KEY, ecodes.KEY_A, 1)
        >>> ui.write_event(ev)
        '''

        if hasattr(event, 'event'):
            event = event.event

        self.write(event.type, event.code, event.value)

    @need_write
    def write(self, etype, code, value):
        '''
        Inject an input event into the input subsystem. Events are
        queued until a synchronization event is received.

        Arguments
        ---------
        etype
          event type (e.g. ``EV_KEY``).

        code
          event code (e.g. ``KEY_A``).

        value
          event value (e.g. 0 1 2 - depends on event type).

        Example
        ---------
        >>> ui.write(e.EV_KEY, e.KEY_A, 1) # key A - down
        >>> ui.write(e.EV_KEY, e.KEY_A, 0) # key A - up
        '''

        _uinput.write(self.fd, etype, code, value)

    def close(self):
        pass
