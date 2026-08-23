Getting started
---------------


Listing accessible event devices
================================

::

    >>> import evdev

    >>> devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    >>> for device in devices:
    ...    print(device.path, device.name, device.phys)
    /dev/input/event1    USB Keyboard        usb-0000:00:12.1-2/input0
    /dev/input/event0    USB Optical Mouse   usb-0000:00:12.0-2/input0

.. note::

   If no devices are shown, ensure your user belongs to the correct group
   (usually ``input``) to obtain read and write access.


Reading events from a device
============================

::

    >>> import evdev

    >>> device = evdev.InputDevice("/dev/input/event1")
    >>> print(device)
    device /dev/input/event1, name "USB Keyboard", phys "usb-0000:00:12.1-2/input0"

    >>> for event in device.read_loop():
    ...     if event.type == evdev.ecodes.EV_KEY:
    ...         print(evdev.categorize(event))
    ... # pressing "a" and holding "space"
    key event at 1337016188.396030, 30 (KEY_A), down
    key event at 1337016188.492033, 30 (KEY_A), up
    key event at 1337016189.772129, 57 (KEY_SPACE), down
    key event at 1337016190.275396, 57 (KEY_SPACE), hold
    key event at 1337016190.284160, 57 (KEY_SPACE), up


Accessing event codes
=====================

The ``evdev.ecodes`` module provides reverse and forward mappings between the
names and values of the event subsystem constants.

::

    >>> from evdev import ecodes

    >>> ecodes.KEY_A
    ... 30
    >>> ecodes.ecodes["KEY_A"]
    ... 30
    >>> ecodes.KEY[30]
    ... "KEY_A"
    >>> ecodes.bytype[ecodes.EV_KEY][30]
    ... "KEY_A"

    # A single value may correspond to multiple event codes.
    >>> ecodes.KEY[152]
    ... ["KEY_COFFEE", "KEY_SCREENLOCK"]


Listing and monitoring input devices
====================================

The *python-evdev* package also comes with a small command-line program for
listing and monitoring input devices:

.. code-block:: bash

   $ python3 -m evdev.evtest

   ID  Device              Name                  Phys                             Uniq
   -------------------------------------------------------------------------------------------
   01  /dev/input/event11  Logitech MX Keys      usb-0000:00:14.0-5.4.4/input2:2  9a-b0-2c-b4
   02  /dev/input/event12  Logitech MX Master 3  usb-0000:00:14.0-5.4.4/input2:1  f8-b5-f2-aa

   Select devices [0-02]: 01
   Listening for events (press ctrl-c to exit) ...
   time 1787478743.772676 type 4 (EV_MSC), code 4    (MSC_SCAN), value 458976
   time 1787478743.772676 type 1 (EV_KEY), code 29   (KEY_LEFTCTRL), value 1
   time 1787478743.772676 ------------- SYN_REPORT -------------
   time 1787478743.872566 type 4 (EV_MSC), code 4    (MSC_SCAN), value 458758
   time 1787478743.872566 type 1 (EV_KEY), code 46   (KEY_C), value 1
   time 1787478743.872566 ------------- SYN_REPORT -------------
