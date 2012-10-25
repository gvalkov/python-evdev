*evdev*
----------------------------------------

*evdev* provides bindings to the generic input event interface in Linux.
The *evdev* interface serves the purpose of passing events generated in the
kernel directly to userspace through character devices that are typically
located in `/dev/input/`.

*evdev* also comes with bindings to *uinput*, the userspace input
subsystem. *Uinput* allows userspace programs to create and handle
input devices from which input events can be directly injected into
the input subsystem.


Documentation:
    +---------+-----------------------------------------+
    | devel   | http://gvalkov.github.com/python-evdev  |
    +---------+-----------------------------------------+
    | stable  | http://packages.python.org/evdev        |
    +---------+-----------------------------------------+

Development:
    https://github.com/gvalkov/python-evdev

PyPi:
    http://pypi.python.org/pypi/evdev


Changelog
=========

Development
^^^^^^^^^^^

Enhancements:
    - Add ability to set/get auto-repeat settings ``EVIOC{SG}REP``.

    - Add ``InputDevice.version`` - the value of ``EVIOCGVERSION``.

    - Add ``device.read_loop()``

    - Add ``device.grab() and device.ungrab()`` - ``EVIOCGRAB``

    - Replace the ``DeviceInfo`` class with a namedtuple.

Fixes:
    - ``device.read_one()`` was dropping events.

    - Rename ``AbsData`` to ``AbsInfo`` (due to ``struct input_absinfo``).


0.2.0 (Aug 22, 2012)
^^^^^^^^^^^^^^^^^^^^

Enhancements:
    - Add the ability to set arbitrary device capabilities on uinput
      devices (defaults to all ``EV_KEY`` ecodes).

    - Add ``UInput.device`` which is an open ``InputDevice`` to the
      input device that uinput 'spawns'.

    - Add ``UInput.capabilities()`` which is just a shortcut to
      ``UInput.device.capabilities()``.

    - Rename ``UInput.write()`` to ``UInput.write_event()``.

    - Add a simpler ``UInput.write(type, code, value)`` method.

    - Make all ``UInput`` constructor arguments optional (default
      device name is now ``py-evdev-uinput``).

    - Add the ability to set ``absmin``, ``absmax``, ``absfuzz`` and
      ``absflat`` when specifying the uinput device's capabilities.

    - Remove the ``nophys`` argument - if a device fails the
      ``EVIOCGPHYS`` ioctl, phys will equal the empty string.

    - Make ``InputDevice.capabilities()`` perform a ``EVIOCGABS`` ioctl
      for devices that support ``EV_ABS`` and return that info wrapped in
      an ``AbsData`` namedtuple.

    - Split ``ioctl_devinfo`` into ``ioctl_devinfo`` and
      ``ioctl_capabilities``.

    - Split ``uinput_open()`` to ``uinput_open()`` and ``uinput_create()``

    - Add more uinput usage examples and documentation.

    - Rewrite uinput tests.

    - Remove ``mouserel`` and ``mouseabs`` from ``UInput``.

    - Tie the sphinx version and release to the distutils version.

    - Set 'methods-before-attributes' sorting in the docs.


Fixes:
    - Remove ``KEY_CNT`` and ``KEY_MAX`` from ``ecodes.keys``.


0.1.1 (May 18, 2012)
^^^^^^^^^^^^^^^^^^^^

Enhancements:
    - Add ``events.keys``, which is a combination of all ``BTN_`` and
      ``KEY_`` event codes.

Fixes:
    - ``ecodes.c`` was not generated when installing through ``pip``.


0.1.0 (May 17, 2012)
^^^^^^^^^^^^^^^^^^^^

*Initial Release*
