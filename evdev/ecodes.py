# encoding: utf-8

'''
This modules exposes most integer constants defined in `linux/input.h`.

Exposed constants::

    KEY, ABS, REL, SW, MSC, LED, BTN, REP, SND, ID, EV, BUS, SYN

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

prefixes = 'KEY ABS REL SW MSC LED BTN REP SND ID EV BUS SYN'
g = globals()

for k,v in getmembers(_ecodes):
    for i in prefixes.split():
        if k.startswith(i):
            g.setdefault(i, {})[v] = k
            ecodes[k] = v

#: keys are a combination of all BTN and KEY codes
keys = {}
keys.update(KEY)
keys.update(BTN)

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
    _ecodes.EV_SYN: SYN, }

from evdev._ecodes import *

# cheaper than whitelisting in an __all__
del k, v, i, getmembers, g, prefixes
