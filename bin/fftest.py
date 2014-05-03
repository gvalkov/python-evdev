#!/usr/bin/env python
# encoding: utf-8

'''
evdev example - tests the force feedback driver
'''

from sys import argv, exit
from select import select
from getopt import gnu_getopt

from evdev import ecodes, ff, InputDevice


usage = 'usage: fftest [options] <device>'

device = InputDevice(argv[1])

print('Axes query:')
