#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
evdev example - uinput force feedback event monitor
'''

from __future__ import print_function
import time, sys

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

ui = UInput(cap, ff_effects_max=10)

try:
    print('uinput device created - run "fftest %s" to test' % ui.device.fn)
except AttributeError:
    print('error: could not find corresponding /dev/input/eventXX device - check permissions')
    sys.exit(1)

print('waiting for events:')
ui.read_loop()
# while True:
#     status, event = ui.read()

#     if status is not None:
#         print(event)
#         # if status == ecodes.FF_STATUS_PLAYING:
#         #     print("rumble playing")
#         # elif status == ecodes.FF_STATUS_STOPPED:
#         #     print("rumble stopped")
#         # else:
#         #     print("received an unknown event!")

#     time.sleep(0.2)
