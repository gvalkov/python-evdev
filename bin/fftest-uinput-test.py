#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
evdev example - uinput force feedback event monitor
'''

from __future__ import print_function
import time, sys, select

from evdev import UInput, UInputError, ecodes


cap = {
    ecodes.EV_FF: [
        ecodes.FF_CONSTANT,
        ecodes.FF_PERIODIC,
        ecodes.FF_RAMP,
        ecodes.FF_SPRING,
        ecodes.FF_FRICTION,
        ecodes.FF_DAMPER,
        # ecodes.FF_RUMBLE,
        ecodes.FF_INERTIA,
    ]
}

def ffcb(event):
    import ipdb ; ipdb.set_trace()
    print(event)

ui = UInput(cap, ff_effects_max=10, ff_callback=ffcb)

try:
    print('uinput device created - run "fftest %s" to test' % ui.device.fn)
except AttributeError:
    print('error: could not find corresponding /dev/input/eventXX device - check permissions')
    sys.exit(1)

print('waiting for events:')
while True:
    r, w, x = select.select([ui.fd], [], [])
    if r:
        ui.read()
