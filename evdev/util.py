# encoding: utf-8

import os
import stat
import glob

from evdev import ecodes
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


def resolve_ecodes(typecodemap, unknown='?'):
    '''
    Resolve event codes and types to their verbose names:
    {            1  : [272, 273, 274] } =>
    { ('EV_KEY', 1) : [('BTN_MOUSE', 272),
                       ('BTN_RIGHT', 273),
                       ('BTN_MIDDLE', 273)] }
    '''

    for type, codes in typecodemap.items():
        type_name = ecodes.EV[type]

        # ecodes.keys are a combination of KEY_ and BTN_ codes
        if type == ecodes.EV_KEY:
            code_names = ecodes.keys
        else:
            code_names = getattr(ecodes, type_name.split('_')[-1])

        codes_res = []
        for i in codes:
            l = [(code_names[i], i) if i in code_names else (unknown, i)]
            codes_res.append(l)

        yield (type_name, type), codes_res


__all__ = list_devices, is_device, categorize, resolve_ecodes
