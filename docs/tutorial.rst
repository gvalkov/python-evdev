Tutorial
--------


Listing accessible event devices
================================

::

    >>> import evdev

    >>> devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    >>> for device in devices:
    >>>     print(device.path, device.name, device.phys)
    /dev/input/event1    Dell Dell USB Keyboard   usb-0000:00:12.1-2/input0
    /dev/input/event0    Dell USB Optical Mouse   usb-0000:00:12.0-2/input0


Listing device capabilities
===========================

::

    >>> import evdev

    >>> device = evdev.InputDevice('/dev/input/event0')
    >>> print(device)
    device /dev/input/event0, name "Dell USB Optical Mouse", phys "usb-0000:00:12.0-2/input0"

    >>> device.capabilities()
    ... { 0: [0, 1, 2], 1: [272, 273, 274, 275], 2: [0, 1, 6, 8], 4: [4] }

    >>> device.capabilities(verbose=True)
    ... { ('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('SYN_MT_REPORT', 2)],
    ...   ('EV_KEY', 1): [('BTN_MOUSE', 272), ('BTN_RIGHT', 273), ('BTN_MIDDLE', 274), ('BTN_SIDE', 275)], ...


Listing device capabilities (devices with absolute axes)
========================================================

::

    >>> import evdev

    >>> device = evdev.InputDevice('/dev/input/event7')
    >>> print(device)
    device /dev/input/event7, name "Wacom Bamboo 2FG 4x5 Finger", phys ""

    >>> device.capabilities()
    ... { 1: [272, 273, 277, 278, 325, 330, 333] ,
    ...   3: [(0, AbsInfo(min=0, max=15360, fuzz=128, flat=0)),
    ...       (1, AbsInfo(min=0, max=10240, fuzz=128, flat=0))] }

    >>> device.capabilities(verbose=True)
    ... { ('EV_KEY', 1): [('BTN_MOUSE', 272), ('BTN_RIGHT', 273), ...],
    ...   ('EV_ABS', 3): [(('ABS_X', 0), AbsInfo(min=0, max=15360, fuzz=128, flat=0)),
    ...                   (('ABS_Y', 1), AbsInfo(min=0, max=10240, fuzz=128, flat=0)),] }

    >>> device.capabilities(absinfo=False)
    ... { 1: [272, 273, 277, 278, 325, 330, 333],
    ...   3: [0, 1, 47, 53, 54, 57] }


Getting and setting LED states
==============================

::

    >>> dev.leds(verbose=True)
    ... [('LED_NUML', 0), ('LED_CAPSL', 1)]

    >>> dev.leds()
    ... [0, 1]

    >>> dev.set_led(ecodes.LED_NUML, 1)  # enable numlock
    >>> dev.set_led(ecodes.LED_NUML, 0)  # disable numlock


Getting currently active keys
=============================

::

    >>> dev.active_keys(verbose=True)
    ... [('KEY_3', 4), ('KEY_LEFTSHIFT', 42)]

    >>> dev.active_keys()
    ... [4, 42]


Reading events
==============

Reading events from a single device in an endless loop.

::

    >>> from evdev import InputDevice, categorize, ecodes
    >>> dev = InputDevice('/dev/input/event1')

    >>> print(dev)
    device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"

    >>> for event in dev.read_loop():
    ...     if event.type == ecodes.EV_KEY:
    ...         print(categorize(event))
    ... # pressing 'a' and holding 'space'
    key event at 1337016188.396030, 30 (KEY_A), down
    key event at 1337016188.492033, 30 (KEY_A), up
    key event at 1337016189.772129, 57 (KEY_SPACE), down
    key event at 1337016190.275396, 57 (KEY_SPACE), hold
    key event at 1337016190.284160, 57 (KEY_SPACE), up


Reading events (using :mod:`asyncio`)
======================================

.. note::

   This requires Python 3.5+ for the async/await keywords.


::

    >>> import asyncio
    >>> from evdev import InputDevice

    >>> dev = InputDevice('/dev/input/event1')

    >>> async def main(dev):
    ...     async for ev in dev.async_read_loop():
    ...         print(repr(ev))

    >>> asyncio.run(main(dev))
    InputEvent(1527363738, 348740, 4, 4, 458792)
    InputEvent(1527363738, 348740, 1, 28, 0)
    InputEvent(1527363738, 348740, 0, 0, 0)


Reading events from multiple devices (using :mod:`select`)
==========================================================

::

    >>> from evdev import InputDevice
    >>> from select import select

    # A mapping of file descriptors (integers) to InputDevice instances.
    >>> devices = map(InputDevice, ('/dev/input/event1', '/dev/input/event2'))
    >>> devices = {dev.fd: dev for dev in devices}

    >>> for dev in devices.values(): print(dev)
    device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"
    device /dev/input/event2, name "Logitech USB Laser Mouse", phys "usb-0000:00:12.0-2/input0"

    >>> while True:
    ...    r, w, x = select(devices, [], [])
    ...    for fd in r:
    ...        for event in devices[fd].read():
    ...            print(event)
    event at 1351116708.002230, code 01, type 02, val 01
    event at 1351116708.002234, code 00, type 00, val 00
    event at 1351116708.782231, code 04, type 04, val 458782
    event at 1351116708.782237, code 02, type 01, val 01


Reading events from multiple devices (using :mod:`selectors`)
=============================================================

This can also be achieved using the :mod:`selectors` module in Python 3.4:

::

   from evdev import InputDevice
   from selectors import DefaultSelector, EVENT_READ

   selector = DefaultSelector()

   mouse = InputDevice('/dev/input/event1')
   keybd = InputDevice('/dev/input/event2')

   # This works because InputDevice has a `fileno()` method.
   selector.register(mouse, EVENT_READ)
   selector.register(keybd, EVENT_READ)

   while True:
       for key, mask in selector.select():
           device = key.fileobj
           for event in device.read():
               print(event)


Reading events from multiple devices (using :mod:`asyncio`)
===========================================================

Yet another possibility is the :mod:`asyncio` module from Python 3.4:

::

    import asyncio, evdev

    @asyncio.coroutine
    def print_events(device):
        while True:
            events = yield from device.async_read()
            for event in events:
                print(device.path, evdev.categorize(event), sep=': ')

    mouse = evdev.InputDevice('/dev/input/eventX')
    keybd = evdev.InputDevice('/dev/input/eventY')

    for device in mouse, keybd:
        asyncio.async(print_events(device))

    loop = asyncio.get_event_loop()
    loop.run_forever()

Since Python 3.5, the `async/await`_ syntax makes this even simpler:

::

    import asyncio, evdev

    mouse = evdev.InputDevice('/dev/input/event4')
    keybd = evdev.InputDevice('/dev/input/event5')

    async def print_events(device):
        async for event in device.async_read_loop():
            print(device.path, evdev.categorize(event), sep=': ')

    for device in mouse, keybd:
        asyncio.ensure_future(print_events(device))

    loop = asyncio.get_event_loop()
    loop.run_forever()


Accessing evdev constants
=========================

::

    >>> from evdev import ecodes

    >>> ecodes.KEY_A, ecodes.ecodes['KEY_A']
    ... (30, 30)
    >>> ecodes.KEY[30]
    ... 'KEY_A'
    >>> ecodes.bytype[ecodes.EV_KEY][30]
    ... 'KEY_A'
    >>> ecodes.KEY[152]  # a single value may correspond to multiple codes
    ... ['KEY_COFFEE', 'KEY_SCREENLOCK']


Searching event codes by regex
==============================

::

    >>> from evdev import util

    >>> res = util.find_ecodes_by_regex(r'(ABS|KEY)_BR(AKE|EAK)')
    >>> res
    ... {1: [411], 3: [10]}
    >>> util.resolve_ecodes_dict(res)
    ... {('EV_KEY', 1): [('KEY_BREAK', 411)], ('EV_ABS', 3): [('ABS_BRAKE', 10)]}


Getting exclusive access to a device
====================================

::

    >>> dev.grab()  # become the sole recipient of all incoming input events
    >>> dev.ungrab()

This functionality is also available as a context manager.

::

    >>> with dev.grab_context():
    ...     pass


Associating classes with event types
====================================

::

    >>> from evdev import categorize, event_factory, ecodes

    >>> class SynEvent:
    ...     def __init__(self, event):
    ...         ...

    >>> event_factory[ecodes.EV_SYN] = SynEvent

See :mod:`events <evdev.events.event_factory>` for more information.

Injecting input
===============

::

    >>> from evdev import UInput, ecodes as e

    >>> ui = UInput()

    >>> # accepts only KEY_* events by default
    >>> ui.write(e.EV_KEY, e.KEY_A, 1)  # KEY_A down
    >>> ui.write(e.EV_KEY, e.KEY_A, 0)  # KEY_A up
    >>> ui.syn()

    >>> ui.close()


Injecting events (using a context manager)
==========================================

::

    >>> ev = InputEvent(1334414993, 274296, ecodes.EV_KEY, ecodes.KEY_A, 1)
    >>> with UInput() as ui:
    ...    ui.write_event(ev)
    ...    ui.syn()


Specifying ``uinput`` device options
====================================

.. note::

   ``ecodes.EV_SYN`` cannot be in the ``cap`` dictionary or the device will not be created.

::

    >>> from evdev import UInput, AbsInfo, ecodes as e

    >>> cap = {
    ...     e.EV_KEY : [e.KEY_A, e.KEY_B],
    ...     e.EV_ABS : [
    ...         (e.ABS_X, AbsInfo(value=0, min=0, max=255,
    ...                           fuzz=0, flat=0, resolution=0)),
    ...         (e.ABS_Y, AbsInfo(0, 0, 255, 0, 0, 0)),
    ...         (e.ABS_MT_POSITION_X, (0, 128, 255, 0)) ]
    ... }

    >>> ui = UInput(cap, name='example-device', version=0x3)
    >>> print(ui)
    name "example-device", bus "BUS_USB", vendor "0001", product "0001", version "0003"
    event types: EV_KEY EV_ABS EV_SYN

    >>> print(ui.capabilities())
    {0: [0, 1, 3],
     1: [30, 48],
     3: [(0,  AbsInfo(value=0, min=0, max=0,   fuzz=255, flat=0, resolution=0)),
         (1,  AbsInfo(value=0, min=0, max=0,   fuzz=255, flat=0, resolution=0)),
         (53, AbsInfo(value=0, min=0, max=255, fuzz=128, flat=0, resolution=0))]}

    >>> # move mouse cursor
    >>> ui.write(e.EV_ABS, e.ABS_X, 20)
    >>> ui.write(e.EV_ABS, e.ABS_Y, 20)
    >>> ui.syn()


Create ``uinput`` device with capabilities of another device
================================================================

::

    >>> from evdev import UInput, InputDevice

    >>> mouse = InputDevice('/dev/input/event1')
    >>> keybd = '/dev/input/event2'

    >>> ui = UInput.from_device(mouse, keybd, name='keyboard-mouse-device')
    >>> ui.capabilities(verbose=True).keys()
    dict_keys([('EV_LED', 17), ('EV_KEY', 1), ('EV_SYN', 0), ('EV_REL', 2), ('EV_MSC', 4)])


.. _`async/await`:  https://docs.python.org/3/library/asyncio-task.html

Create ``uinput`` device capable of receiving FF-effects
========================================================

::

    import asyncio
    from evdev import UInput, categorize, ecodes

    cap = {
       ecodes.EV_FF:  [ecodes.FF_RUMBLE ],
       ecodes.EV_KEY: [ecodes.KEY_A, ecodes.KEY_B]
    }

    ui = UInput(cap, name='test-controller', version=0x3)

    async def print_events(device):
        async for event in device.async_read_loop():
            print(categorize(event))

            # Wait for an EV_UINPUT event that will signal us that an
            # effect upload/erase operation is in progress.
            if event.type != ecodes.EV_UINPUT:
                continue

            if event.code == ecodes.UI_FF_UPLOAD:
                upload = device.begin_upload(event.value)
                upload.retval = 0

                print(f'[upload] effect_id: {upload.effect.id}, type: {upload.effect.type}')
                device.end_upload(upload)

            elif event.code == ecodes.UI_FF_ERASE:
                erase = device.begin_erase(event.value)
                print(f'[erase] effect_id {erase.effect_id}')

                erase.retval = 0
                device.end_erase(erase)

    asyncio.ensure_future(print_events(ui))
    loop = asyncio.get_event_loop()
    loop.run_forever()


Injecting an FF-event into first FF-capable device found
========================================================

::

    from evdev import ecodes, InputDevice, ff, list_devices
    import time

    # Find first EV_FF capable event device (that we have permissions to use).
    for name in list_devices():
        dev = InputDevice(name)
        if ecodes.EV_FF in dev.capabilities():
            break

    rumble = ff.Rumble(strong_magnitude=0x0000, weak_magnitude=0xffff)
    effect_type = ff.EffectType(ff_rumble_effect=rumble)
    duration_ms = 1000

    effect = ff.Effect(
        ecodes.FF_RUMBLE, -1, 0,
        ff.Trigger(0, 0),
        ff.Replay(duration_ms, 0),
        effect_type
    )

    repeat_count = 1
    effect_id = dev.upload_effect(effect)
    dev.write(ecodes.EV_FF, effect_id, repeat_count)
    time.sleep(duration_ms)
    dev.erase_effect(effect_id)

Forwarding force-feedback from uinput to a real device
======================================================

::

    import evdev
    from evdev import ecodes as e

    # Find first EV_FF capable event device (that we have permissions to use).
    for name in evdev.list_devices():
        dev = evdev.InputDevice(name)
        if e.EV_FF in dev.capabilities():
            break
    # To ensure forwarding works correctly it is important that `max_effects` 
    # of the uinput device is <= `dev.ff_effects_count`.
    # `from_device()` will do this automatically, but in some situations you may 
    # want to set the `max_effects` parameter manually, such as when using `Uinput()`.
    # `filtered_types` is specified as by default EV_FF events are filtered
    uinput = evdev.UInput.from_device(dev, filtered_types=[e.EV_SYN])

    # Keeps track of which effects have been uploaded to the device
    effects = set()

    for event in uinput.read_loop():
        
        # Handle the special uinput events
        if event.type == e.EV_UINPUT:

            if event.code == e.UI_FF_UPLOAD:
                upload = uinput.begin_upload(event.value)

                # Checks if this is a new effect
                if upload.effect.id not in effects:
                    effects.add(upload.effect.id)
                    # Setting id to 1 indicates that a new effect must be allocated
                    upload.effect.id = -1

                dev.upload_effect(upload.effect)
                upload.retval = 0
                uinput.end_upload(upload)
                
            elif event.code == e.UI_FF_ERASE:
                erase = uinput.begin_erase(event.value)
                erase.retval = 0
                dev.erase_effect(erase.effect_id)
                effects.remove(erase.effect_id)
                uinput.end_erase(erase)
        
        # Forward writes to actual rumble device.
        elif event.type == e.EV_FF:
            dev.write(event.type, event.code, event.value)
