# encoding: utf-8

import os
import stat
import glob
import re

from evdev import ecodes
from evdev.events import event_factory


def list_devices(input_device_dir='/dev/input'):
    '''List readable character devices in ``input_device_dir``.'''

    fns = glob.glob('{}/event*'.format(input_device_dir))
    fns = list(filter(is_device, fns))

    return fns


def is_device(fn):
    '''Check if ``fn`` is a readable and writable character device.'''

    if not os.path.exists(fn):
        return False

    m = os.stat(fn)[stat.ST_MODE]
    if not stat.S_ISCHR(m):
        return False

    if not os.access(fn, os.R_OK | os.W_OK):
        return False

    return True


def categorize(event):
    '''
    Categorize an event according to its type.

    The :data:`event_factory <evdev.events.event_factory>` dictionary
    maps event types to sub-classes of :class:`InputEvent
    <evdev.events.InputEvent>`. If the event cannot be categorized, it
    is returned unmodified.'''

    if event.type in event_factory:
        return event_factory[event.type](event)
    else:
        return event


def resolve_ecodes_dict(typecodemap, unknown='?'):
    '''
    Resolve event codes and types to their verbose names.

    :param typecodemap: mapping of event types to lists of event codes.
    :param unknown: symbol to which unknown types or codes will be resolved.

    Example
    -------
    >>> resolve_ecodes_dict({ 1: [272, 273, 274] })
    { ('EV_KEY', 1): [('BTN_MOUSE',  272),
                      ('BTN_RIGHT',  273),
                      ('BTN_MIDDLE', 274)] }

    If ``typecodemap`` contains absolute axis info (instances of
    :class:`AbsInfo <evdev.device.AbsInfo>` ) the result would look
    like:

    >>> resolve_ecodes_dict({ 3: [(0, AbsInfo(...))] })
    { ('EV_ABS', 3L): [(('ABS_X', 0L), AbsInfo(...))] }
    '''

    for etype, codes in typecodemap.items():
        type_name = ecodes.EV[etype]

        # ecodes.keys are a combination of KEY_ and BTN_ codes
        if etype == ecodes.EV_KEY:
            ecode_dict = ecodes.keys
        else:
            ecode_dict = getattr(ecodes, type_name.split('_')[-1])

        resolved = resolve_ecodes(ecode_dict, codes, unknown)
        yield (type_name, etype), resolved


def resolve_ecodes(ecode_dict, ecode_list, unknown='?'):
    '''
    Resolve event codes and types to their verbose names.

    Example
    -------
    >>> resolve_ecodes([272, 273, 274])
    [('BTN_MOUSE',  272), ('BTN_RIGHT',  273), ('BTN_MIDDLE', 274)]
    '''
    res = []
    for ecode in ecode_list:
        # elements with AbsInfo(), eg { 3 : [(0, AbsInfo(...)), (1, AbsInfo(...))] }
        if isinstance(ecode, tuple):
            if ecode[0] in ecode_dict:
                l = ((ecode_dict[ecode[0]], ecode[0]), ecode[1])
            else:
                l = ((unknown, ecode[0]), ecode[1])

        # just ecodes, e.g: { 0 : [0, 1, 3], 1 : [30, 48] }
        else:
            if ecode in ecode_dict:
                l = (ecode_dict[ecode], ecode)
            else:
                l = (unknown, ecode)
        res.append(l)

    return res


def filter_ecodes(r):
    '''
    Filter event key codes by regular expression.

    Example
    -------
    >>> list(filter_ecodes(r'KEY_([A-C]|ENTER|SPACE)$'))
    [30, 48, 46, 28, 57]
    '''
    c = re.compile(r)
    for key, value in ecodes.keys.items():
        if isinstance(value, str):
            codes = (value,)
        elif isinstance(value, list):
            codes = value

        for code in codes:
            if c.match(code):
                yield key


__all__ = (
    'list_devices',
    'is_device',
    'categorize',
    'resolve_ecodes',
    'resolve_ecodes_dict',
    'filter_ecodes',
)
