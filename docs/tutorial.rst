Tutorial
--------

Listing accessible event devices
================================

::

    >>> from evdev import InputDevice, list_devices

    >>> devices = [InputDevice(fn) for fn in list_devices()]
    >>> for dev in devices:
    ...    print(dev.fn, dev.name, dev.phys)
    /dev/input/event1    Dell Dell USB Keyboard   usb-0000:00:12.1-2/input0
    /dev/input/event0    Dell USB Optical Mouse   usb-0000:00:12.0-2/input0


Listing device capabilities
===========================

::

    >>> from evdev import InputDevice

    >>> dev = InputDevice('/dev/input/event0')
    >>> print(dev)
    device /dev/input/event0, name "Dell USB Optical Mouse", phys "usb-0000:00:12.0-2/input0"

    >>> dev.capabilities()
    ... { 0: [0, 1, 2], 1: [272, 273, 274, 275], 2: [0, 1, 6, 8], 4: [4] }

    >>> dev.capabilities(verbose=True)
    ... { ('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('SYN_MT_REPORT', 2)],
    ...   ('EV_KEY', 1): [('BTN_MOUSE', 272), ('BTN_RIGHT', 273), ('BTN_MIDDLE', 274), ('BTN_SIDE', 275)], ...


Listing device capabilities for devices with absolute axes
==========================================================

::

    >>> from evdev import InputDevice

    >>> dev = InputDevice('/dev/input/event7')
    >>> print(dev)
    device /dev/input/event7, name "Wacom Bamboo 2FG 4x5 Finger", phys ""

    >>> dev.capabilities()
    ... { 1: [272, 273, 277, 278, 325, 330, 333] ,
    ...   3: [(0, AbsInfo(min=0, max=15360, fuzz=128, flat=0)),
    ...       (1, AbsInfo(min=0, max=10240, fuzz=128, flat=0))] }

    >>> dev.capabilities(verbose=True)
    ... { ('EV_KEY', 1): [('BTN_MOUSE', 272), ('BTN_RIGHT', 273), ...],
    ...   ('EV_ABS', 3): [(('ABS_X', 0), AbsInfo(min=0, max=15360, fuzz=128, flat=0)),
    ...                   (('ABS_Y', 1), AbsInfo(min=0, max=10240, fuzz=128, flat=0)),] }

    >>> dev.capabilities(absinfo=False)
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


Reading events from multiple devices
====================================

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


This can also be achieved using the selectors_ module in Python 3.4:

::

   from evdev import InputDevice
   from selectors import DefaultSelector, EVENT_READ

   selector = selectors.DefaultSelector()

   mouse = evdev.InputDevice('/dev/input/event1')
   keybd = evdev.InputDevice('/dev/input/event2')

   # This works because InputDevice has a `fileno()` method.
   selector.register(mouse, selectors.EVENT_READ)
   selector.register(keybd, selectors.EVENT_READ)

   while True:
       for key, mask in selector.select():
           device = key.fileobj
           for event in device.read():
               print(event)

               
Yet another possibility is asyncio in Python 3.4:

::

    import asyncio
    from evdev import list_devices, InputDevice, categorize

    # Python 3.5 syntax, using "async for"
    async def dump_events(device):    
        async for ev in device.read_loop():
            print(device.name, categorize(ev))

    ## Python 3.4 syntax, using "yield from" in an infinite loop
    #@asyncio.coroutine
    #def dump_events(device):    
    #    while True:
    #        evs = yield from device.async_read()
    #        for ev in evs:
    #            print(device.name, categorize(ev))

    for file in list_devices():
        device = InputDevice(file)
        asyncio.ensure_future( dump_events( device ) )

    asyncio.get_event_loop().run_forever()



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


Reading events with asyncore
============================

::

    >>> from asyncore import file_dispatcher, loop
    >>> from evdev import InputDevice, categorize, ecodes
    >>> dev = InputDevice('/dev/input/event1')

    >>> class InputDeviceDispatcher(file_dispatcher):
    ...     def __init__(self, device):
    ...         self.device = device
    ...         file_dispatcher.__init__(self, device)
    ...
    ...     def recv(self, ign=None):
    ...         return self.device.read()
    ...
    ...     def handle_read(self):
    ...         for event in self.recv():
    ...             print(repr(event))

    >>> InputDeviceDispatcher(dev)
    >>> loop()
    InputEvent(1337255905L, 358854L, 1, 30, 0L)
    InputEvent(1337255905L, 358857L, 0, 0, 0L)


Reading events with asyncio
===========================

To read a single event, you can use device.async_read_one()

::

    event = await dev.async_read_one()    

To read a batch of events, you can use device.async_read():

::

    ev_batch = await dev.async_read()
    for ev in ev_batch:
        print(categorize(ev))

To read all events in an infinite loop, use dev.read_loop() and `async for`:

::
    async for ev in dev.read_loop():
        print(categorize(ev))
        
See "Reading events from multiple devices" for a complete example using asyncio.


Getting exclusive access to a device
====================================

::

    >>> dev.grab()  # become the sole recipient of all incoming input events
    >>> dev.ungrab()


Associating classes with event types
====================================

::

    >>> from evdev import categorize, event_factory, ecodes

    >>> class SynEvent(object):
    ...     def __init__(self, event):
    ...         ...

    >>> event_factory[ecodes.EV_SYN] = SynEvent

See :mod:`events <evdev.events.event_factory>` for more information.

Injecting input events
======================

::

    >>> from evdev import UInput, ecodes as e

    >>> ui = UInput()

    >>> # accepts only KEY_* events by default
    >>> ui.write(e.EV_KEY, e.KEY_A, 1)  # KEY_A down
    >>> ui.write(e.EV_KEY, e.KEY_A, 0)  # KEY_A up
    >>> ui.syn()

    >>> ui.close()


Injecting events (2)
====================

::

    >>> ev = InputEvent(1334414993, 274296, ecodes.EV_KEY, ecodes.KEY_A, 1)
    >>> with UInput() as ui:
    ...    ui.write_event(ev)
    ...    ui.syn()


Specifying ``uinput`` device options
====================================
::

    >>> from evdev import UInput, AbsInfo, ecodes as e

    >>> cap = {
    ...     e.EV_KEY : [e.KEY_A, e.KEY_B],
    ...     e.EV_ABS : [
    ...         (e.ABS_X, AbsInfo(value=0, min=0, max=255,
    ...                           fuzz=0, flat=0, resolution=0)),
    ...         (e.ABS_Y, AbsInfo(0, 0, 255, 0, 0, 0)),
    ...         (e.ABS_MT_POSITION_X, (0, 255, 128, 0)) ]
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


.. _selectors:   https://docs.python.org/3/library/selectors.html
