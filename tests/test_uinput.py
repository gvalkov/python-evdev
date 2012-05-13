# encoding: utf-8

from select import select
from pytest import raises

from evdev import uinput, ecodes, events, device, util


uinput_options = {
    'name'      : 'test-uinput-device',
    'vendor'    : 0x1100,
    'product'   : 0x2200,
    'version'   : 0x3300,
    'mouserel'  : True,
    'mouseabs'  : False,
    'keys'      : True,
    'fn'        : '/dev/uinput',
}


def test_open():
    ui = uinput.UInput(**uinput_options)
    device_exists()
    ui.close()

def test_with_open():
    with uinput.UInput(**uinput_options):
        pass

def test_maxnamelen():
    o = uinput_options.copy()
    with raises(uinput.UInputError):
        o['name'] = 'a' * 150
        uinput.UInput(**o)

def test_write():
    ui = uinput.UInput(**uinput_options)

    dev = find_device_byname(uinput_options['name'])
    assert dev, 'could not find uinput device "%s"' % uinput_options['name']

    ev1 = events.InputEvent(1334414993, 274296, ecodes.EV_KEY, ecodes.KEY_P, 1) # KEY_P down
    ev2 = events.InputEvent(1334414993, 274396, ecodes.EV_KEY, ecodes.KEY_P, 1) # KEY_P down
    ev3 = events.InputEvent(1334414993, 274296, ecodes.EV_KEY, ecodes.KEY_P, 0) # KEY_P up

    while True:
        r, w, x = select([dev], [dev], [])

        if w:
            ui.write(ev1)
            ui.write(ev2)
            ui.write(ev3)
            ui.syn()

        if r:
            assert dev.read_one().code == ev1.code
            assert dev.read_one().code == ev3.code
            break

    dev.close()
    ui.close()


def device_exists():
    o = uinput_options
    match = 'I: Bus=0003 Vendor=%04hx Product=%04hx Version=%04hx' % \
            (o['vendor'], o['product'], o['version'])

    for line in open('/proc/bus/input/devices'):
        if line.strip() == match: break
    else:
        assert False, '%s missing from /proc/bus/input/devices' % match

def find_device_byname(name):
    for fn in util.list_devices('/dev/input/'):
        d = device.InputDevice(fn, nophys=True)
        if d.name == name:
            return d
