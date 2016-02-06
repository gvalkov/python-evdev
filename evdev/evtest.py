#!/usr/bin/env python
# encoding: utf-8

'''
Usage: evtest [options] [<device>, ...]

Input device enumerator and event monitor.

Running evtest without any arguments will let you select
from a list of all readable input devices.

Options:
  -h, --help          Show this help message and exit.
  -c, --capabilities  List device capabilities and exit.
  -g, --grab          Other applications will not receive events from
                      the selected devices while evtest is running.

Examples:
  evtest /dev/input/event0 /dev/input/event1
'''


from __future__ import print_function

import sys
import select
import optparse

from evdev import ecodes, list_devices, AbsInfo, InputDevice


def parseopt():
    parser = optparse.OptionParser(add_help_option=False)
    parser.add_option('-h', '--help', action='store_true')
    parser.add_option('-g', '--grab', action='store_true')
    parser.add_option('-c', '--capabilities', action='store_true')
    return parser.parse_args()


def main():
    opts, devices = parseopt()
    if opts.help:
        print(__doc__.strip())
        return 0

    if not devices:
        devices = select_devices()
    else:
        devices = [InputDevice(path) for path in devices]

    if opts.capabilities:
        for device in devices:
            print_capabilities(device)
        return 0

    if opts.grab:
        for device in devices:
            device.grab()

    print('Listening for events ...\n')
    fd_to_device = {dev.fd: dev for dev in devices}
    while True:
        r, w, e = select.select(fd_to_device, [], [])

        for fd in r:
            for event in fd_to_device[fd].read():
                print_event(event)


def select_devices(device_dir='/dev/input'):
    '''
    Select one or more devices from a list of accessible input devices.
    '''

    devices = reversed(list_devices(device_dir))
    devices = [InputDevice(path) for path in devices]
    if not devices:
        msg = 'error: no input devices found (do you have rw permission on %s/*?)'
        print(msg % device_dir, file=sys.stderr)
        sys.exit(1)

    dev_format = '{0:<3} {1.fn:<20} {1.name:<35} {1.phys}'
    dev_lines  = [dev_format.format(n, d) for n, d in enumerate(devices)]

    print('ID  {:<20} {:<35} {}'.format('Device', 'Name', 'Phys'))
    print('-' * len(max(dev_lines, key=len)))
    print('\n'.join(dev_lines))
    print()

    choice = input('Select devices [0-%s]: ' % (len(dev_lines)-1))
    choice = choice.split()

    print()
    return [devices[int(num)] for num in choice]


def print_capabilities(device):
    capabilities = device.capabilities(verbose=True)

    print('Device name: {.name}'.format(device))
    print('Device info: {.info}'.format(device))
    print('Repeat settings: {}\n'.format(device.repeat))

    if ('EV_LED', ecodes.EV_LED) in capabilities:
        leds = ','.join(i[0] for i in device.leds(True))
        print('Active LEDs: %s' % leds)

    active_keys = ','.join(k[0] for k in device.active_keys(True))
    print('Active keys: %s\n' % active_keys)

    print('Device capabilities:')
    for type, codes in capabilities.items():
        print('  Type {} {}:'.format(*type))
        for code in codes:
            # code <- ('BTN_RIGHT', 273) or (['BTN_LEFT', 'BTN_MOUSE'], 272)
            if isinstance(code[1], AbsInfo):
                print('    Code {:<4} {}:'.format(*code[0]))
                print('      {}'.format(code[1]))
            else:
                # Multiple names may resolve to one value.
                s = ', '.join(code[0]) if isinstance(code[0], list) else code[0]
                print('    Code {:<4} {}'.format(s, code[1]))
        print('')


def print_event(e):
    if e.type == ecodes.EV_SYN:
        if e.code == ecodes.SYN_MT_REPORT:
            msg = 'time {:<16} +++++++++ {} ++++++++'
        else:
            msg = 'time {:<16} --------- {} --------'
        print(msg.format(e.timestamp(), ecodes.SYN[e.code]))
    else:
        if e.type in ecodes.bytype:
            codename = ecodes.bytype[e.type][e.code]
        else:
            codename = '?'

        evfmt = 'time {:<16} type {} ({}), code {:<4} ({}), value {}'
        print(evfmt.format(e.timestamp(), e.type, ecodes.EV[e.type], e.code, codename, e.value))


if __name__ == '__main__':
    sys.exit(main())
