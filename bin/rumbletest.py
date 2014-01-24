#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Example of a device listening to rumble events.

Test using any program that sends rumble events to the uinput device (e.g. fftest)
'''

import time

from evdev import UInput, UInputError, ecodes

joystick = UInput()

had_event = True

while True:
    event = joystick.read()

    if event == None:
        if had_event:
            had_event = False
            print('Waiting for events', end='', flush=True)
        else:
            print('.', end='', flush=True)
    else:
        had_event = True
        print()
        print()

        if event == ecodes.FF_STATUS_PLAYING:
            print("Rumble playing!")
        elif event == ecodes.FF_STATUS_STOPPED:
            print("Rumble stopped!")
        else:
            print("Received an unknown event!")

    time.sleep(0.2)
