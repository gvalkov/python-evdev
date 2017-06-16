Changelog
---------


0.7.0 (Jun 16, 2017)
====================

- ``InputDevice`` now accepts objects that support the path protocol.
  For example::

    pth = pathlib.Path('/dev/input/event0')
    dev = evdev.InputDevice(pth)

- Support path protocol in ``InputDevice``. This means that ``InputDevice``
  instances can be passed to callers that expect a ``os.PathLike`` object.

- Exceptions raised during ``InputDevice.async_read()`` (and similar) are now
  handled properly (i.e. an exception is set on the returned future instead of
  leaking that exception into the event loop) (Fixes `#67`_).


0.6.4 (Oct 07, 2016)
====================

- Exclude ``ecodes.c`` from source distribution (Fixes `#63`_).


0.6.3 (Oct 06, 2016)
====================

- Add the ``UInput.from_device`` class method, which allows uinput device to be
  created with the capabiltiies of one or more existing input devices::

    ui = UInput.from_device('/dev/input1', '/dev/input2', **constructor_kwargs)

- Add the ``build_ecodes`` distutils command, which generates the ``ecodes.c``
  extension module. The new way of overwriting the evdev header locations is::

    python setup.py build \
      build_ecodes --evdev-headers path/input.h:path/input-event-codes.h \
      build_ext --include-dirs  path/ \
      install

  The ``build*`` and ``install`` commands no longer have to be part of the same
  command-line (i.e. running ``install`` will reuse the outputs of the last
  ``build``).


0.6.1 (Jun 04, 2016)
====================

- Dissable tty echoing while evtest is running.
- Allow evtest to listen to more than one devices.

- The setup.py script now allows the location of the input header files to be
  overwritten. For example::

    python setup.py build_ext \
      --evdev-headers path/input.h:path/input-event-codes.h \
      --include-dirs  path/ \
      install


0.6.0 (Feb 14, 2016)
====================

- Asyncio and async/await support (many thanks to `@paulo-raca`_).
- Add the ability to set the `phys` property of uinput devices (thanks `@paulo-raca`_).
- Add a generic :func:`InputDevice.set` method (thanks `@paulo-raca`_).
- Distribute the evtest script along with evdev.
- Fix issue with generating :mod:`ecodes.c` in recent kernels (``>= 4.4.0``).
- Fix absinfo item indexes in :func:`UInput.uinput_create()` (thanks `@forsenonlhaimaisentito`_).
- More robust comparison of :class:`InputDevice` objects (thanks `@isia`_).


0.5.0 (Jun 16, 2015)
====================

- Write access to the input device is no longer mandatory. Evdev will
  first try to open the device for reading and writing and fallback to
  read-only. Methods that require write access (e.g. :func:`set_led()`)
  will raise :class:`EvdevError` if the device is open only for reading.


0.4.7 (Oct 07, 2014)
====================

- Fallback to distutils if setuptools is not available.


0.4.6 (Oct 07, 2014)
====================

- Rework documentation and docstrings once more.

- Fix install on Python 3.4 (works around issue21121_).

- Fix :func:`ioctl()` requested buffer size (thanks Jakub Wojciech Klama).


0.4.5 (Jul 06, 2014)
====================

- Add method for returning a list of the currently active keys -
  :func:`InputDevice.active_keys()` (thanks `@spasche`_).

- Fix a potential buffer overflow in :func:`ioctl_capabilities()` (thanks `@spasche`_).


0.4.4 (Jun 04, 2014)
====================

- Calling :func:`InputDevice.read_one()` should always return ``None``,
  when there is nothing to be read, even in case of a ``EAGAIN`` errno
  (thanks JPP).


0.4.3 (Dec 19, 2013)
====================

- Silence :class:`OSError` in destructor (thanks `@polyphemus`_).

- Make :func:`InputDevice.close()` work in cases in which stdin (fd 0)
  has been closed (thanks `@polyphemus`_).


0.4.2 (Dec 13, 2013)
====================

- Rework documentation and docstrings.

- Call :func:`InputDevice.close()` from :func:`InputDevice.__del__()`.


0.4.1 (Jul 24, 2013)
====================

- Fix reference counting in :func:`InputDevice.device_read()`,
  :func:`InputDevice.device_read_many()` and :func:`ioctl_capabilities`.


0.4.0 (Jul 01, 2013)
====================

- Add ``FF_*`` and ``FF_STATUS`` codes to :func:`ecodes` (thanks `@bgilbert`_).

- Reverse event code mappings (``ecodes.{KEY,FF,REL,ABS}`` and etc.)
  will now map to a list of codes, whenever a value corresponds to
  multiple codes::

    >>> ecodes.KEY[152]
    ... ['KEY_COFFEE', 'KEY_SCREENLOCK']
    >>> ecodes.KEY[30]
    ... 'KEY_A'

- Set the state of a LED through :func:`InputDevice.set_led()` (thanks
  `@accek`_).

- Open :attr:`InputDevice.fd` in ``O_RDWR`` mode from now on.

- Fix segfault in :func:`InputDevice.device_read_many()` (thanks `@bgilbert`_).


0.3.3 (May 29, 2013)
====================

- Raise :class:`IOError` from :func:`InputDevice.device_read()` and
  :func:`InputDevice.device_read_many()` when :func:`InputDevice.read()`
  fails.

- Several stability and style changes (thank you debian code reviewers).


0.3.2 (Apr 05, 2013)
====================

- Fix vendor id and product id order in :func:`DeviceInfo` (thanks `@kived`_).


0.3.1 (Nov 23, 2012)
====================

- :func:`InputDevice.read()` will return an empty tuple if the device
  has nothing to offer (instead of segfaulting).

- Exclude unnecessary package data in sdist and bdist.


0.3.0 (Nov 06, 2012)
====================

- Add ability to set/get auto-repeat settings with ``EVIOC{SG}REP``.

- Add :func:`InputDevice.version` - the value of ``EVIOCGVERSION``.

- Add :func:`InputDevice.read_loop()`.

- Add :func:`InputDevice.grab()` and :func:`InputDevice.ungrab()` -
  exposes ``EVIOCGRAB``.

- Add :func:`InputDevice.leds` - exposes ``EVIOCGLED``.

- Replace :class:`DeviceInfo` class with a namedtuple.

- Prevent :func:`InputDevice.read_one()` from skipping events.

- Rename :class:`AbsData` to :class:`AbsInfo` (as in ``struct input_absinfo``).


0.2.0 (Aug 22, 2012)
====================

- Add the ability to set arbitrary device capabilities on uinput
  devices (defaults to all ``EV_KEY`` ecodes).

- Add :attr:`UInput.device` which is an open :class:`InputDevice` to
  the input device that uinput 'spawns'.

- Add :func:`UInput.capabilities()` which is just a shortcut to
  :func:`UInput.device.capabilities()`.

- Rename :func:`UInput.write()` to :func:`UInput.write_event()`.

- Add a simpler :func:`UInput.write(type, code, value)` method.

- Make all :func:`UInput` constructor arguments optional (default
  device name is now ``py-evdev-uinput``).

- Add the ability to set ``absmin``, ``absmax``, ``absfuzz`` and
  ``absflat`` when specifying the uinput device's capabilities.

- Remove the ``nophys`` argument - if a device fails the
  ``EVIOCGPHYS`` ioctl, phys will equal the empty string.

- Make :func:`InputDevice.capabilities()` perform a ``EVIOCGABS``
  ioctl for devices that support ``EV_ABS`` and return that info
  wrapped in an ``AbsData`` namedtuple.

- Split ``ioctl_devinfo`` into ``ioctl_devinfo`` and
  ``ioctl_capabilities``.

- Split :func:`UInput.uinput_open()` to :func:`UInput.uinput_open()`
  and :func:`UInput.uinput_create()`

- Add more uinput usage examples and documentation.

- Rewrite uinput tests.

- Remove ``mouserel`` and ``mouseabs`` from :class:`UInput`.

- Tie the sphinx version and release to the distutils version.

- Set 'methods-before-attributes' sorting in the docs.

- Remove ``KEY_CNT`` and ``KEY_MAX`` from :func:`ecodes.keys`.


0.1.1 (May 18, 2012)
====================

- Add ``events.keys``, which is a combination of all ``BTN_`` and
  ``KEY_`` event codes.

- ``ecodes.c`` was not generated when installing through ``pip``.


0.1.0 (May 17, 2012)
====================

*Initial Release*

.. _`@polyphemus`: https://github.com/polyphemus
.. _`@bgilbert`: https://github.com/bgilbert
.. _`@accek`: https://github.com/accek
.. _`@kived`: https://github.com/kived
.. _`@spasche`: https://github.com/spasche
.. _`@isia`:    https://github.com/isia
.. _`@forsenonlhaimaisentito`: https://github.com/forsenonlhaimaisentito
.. _`@paulo-raca`: https://github.com/paulo-raca

.. _issue21121: http://bugs.python.org/issue21121
.. _`#63`:      https://github.com/gvalkov/python-evdev/issues/63
.. _`#63`:      https://github.com/gvalkov/python-evdev/issues/67
