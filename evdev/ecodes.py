# encoding: utf-8

'''
This modules exposes most integer constants defined in ``linux/input.h``.

Exposed constants::

    KEY, ABS, REL, SW, MSC, LED, BTN, REP, SND, ID, EV, BUS, SYN, FF,
    FF_STATUS

This module also provides numerous reverse and forward mappings that are best
illustrated by a few examples::

    >>> evdev.ecodes.KEY_A
    30

    >>> evdev.ecodes.ecodes['KEY_A']
    30

    >>> evdev.ecodes.KEY[30]
    'KEY_A'

    >>> evdev.ecodes.REL[0]
    'REL_X'

    >>> evdev.ecodes.EV[evdev.EV_KEY]
    'EV_KEY'

    >>> evdev.ecodes.bytype[EV_REL][0]
    'REL_X'
'''

from inspect import getmembers
from evdev import _ecodes


#: mapping of names to values
ecodes = {}

# the order of FF_STATUS and FF is significant
prefixes = 'KEY ABS REL SW MSC LED BTN REP SND ID EV BUS SYN FF_STATUS FF'
g = globals()

for k,v in getmembers(_ecodes):
    for i in prefixes.split():
        if k.startswith(i):
            ecodes[k] = v
            d = g.setdefault(i, {})
            # keep FF_RUMBLE from being named FF_EFFECT_MIN, etc.
            if v not in d or d[v].endswith('_MIN') or d[v].endswith('_MAX'):
                d[v] = k
            break


#: keys are a combination of all BTN and KEY codes
keys = {}
keys.update(BTN)
keys.update(KEY)

# make keys safe to use for the default list of uinput device
# capabilities
del keys[_ecodes.KEY_MAX]
del keys[_ecodes.KEY_CNT]

#: mapping of event types to other value/name mappings
bytype = {
    _ecodes.EV_KEY: keys,
    _ecodes.EV_ABS: ABS,
    _ecodes.EV_REL: REL,
    _ecodes.EV_SW:  SW,
    _ecodes.EV_MSC: MSC,
    _ecodes.EV_LED: LED,
    _ecodes.EV_REP: REP,
    _ecodes.EV_SND: SND,
    _ecodes.EV_SYN: SYN,
    _ecodes.EV_FF:  FF,
    _ecodes.EV_FF_STATUS: FF_STATUS, }

from evdev._ecodes import *

# cheaper than whitelisting in an __all__
del k, v, i, getmembers, g, prefixes
