# encoding: utf-8

import os
import stat
import glob

from evdev.events import event_factory


def list_devices(input_device_dir='/dev/input'):
    '''List readable character devices.'''

    fns = glob.glob('{}/event*'.format(input_device_dir))
    fns = list(filter(is_device, fns))

    return fns


def is_device(fn):
    '''Determine if a file exists, is readable and is a character device.'''

    if not os.path.exists(fn):
        return False

    m = os.stat(fn)[stat.ST_MODE]
    if not stat.S_ISCHR(m):
        return False

    if not os.access(fn, os.R_OK):
        return False

    return True


def categorize(event):
    '''
    Categorize an event according to its type.

    The :data:`event_factory <evdev.events.event_factory>` dictionary maps
    event types to their classes. If there is no corresponding key, the event
    is returned as it was.
    '''

    if event.type in event_factory:
        return event_factory[event.type](event)
    else:
        return event


__all__ = list_devices, is_device, categorize
