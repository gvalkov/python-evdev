Changelog
---------

1.9.3 (Feb 05, 2025)
====================

- Fix several memory leaks in ``input.c``.

- Raise the minimum supported Python version to 3.9 and the setuptools version to 77.0.


1.9.2 (May 01, 2025)
====================

- Add the "--reproducible" build option which removes the build date and used headers from the
  generated ``ecodes.c``. Example usage::

    python -m build --config-setting=--build-option='build_ecodes --reproducible' -n 

- Use ``Generic`` to set precise type for ``InputDevice.path``.


1.9.1 (Feb 22, 2025)
====================

- Fix fox missing ``UI_FF`` constants in generated ``ecodes.py``.

- More type annotations.


1.9.0 (Feb 08, 2025)
====================

- Fix for ``CPATH/C_INCLUDE_PATH`` being ignored during build.

- Slightly faster reading of events in ``device.read()`` and ``device.read_one()``.

- Fix FreeBSD support.

- Drop deprecated ``InputDevice.fn`` (use ``InputDevice.path`` instead).

- Improve type hint coverage and add a ``py.typed`` file to the sdist.


1.8.0 (Jan 25, 2025)
====================

- Binary wheels are now provided by the `evdev-binary <http://pypi.python.org/pypi/evdev-binary>`_ package.
  The package is compiled on manylinux_2_28 against kernel 4.18.

- The ``evdev.ecodes`` module is now generated at install time and contains only constants. This allows type
  checking and introspection of the ``evdev.ecodes`` module, without having to execute it first. The old
  module is available as ``evdev.ecodes_runtime``. In case generation of the static ``ecodes.py`` fails, the
  install process falls back to using ``ecodes_runtime.py`` as ``ecodes.py``.

- Reverse mappings in ``evdev.ecodes`` that point to more than one value are now tuples instead of lists. For example::

    >>> ecodes.KEY[153]
    ('KEY_DIRECTION', 'KEY_ROTATE_DISPLAY')

- Raise the minimum supported Python version to 3.8.

- Fix keyboard delay and repeat being swapped (#227).

- Move the ``syn()`` convenience method from ``InputDevice`` to ``EventIO`` (#224).


1.7.1 (May 8, 2024)
====================

- Provide fallback value for ``FF_MAX_EFFECTS``, which fixes the build on EL 7 (#219).

- Add ``#ifdef`` guards around ``UI_GET_SYSNAME`` to improve kernel compatibility (#218) .

- Wait up to two seconds for uinput devices to appear. (#215)


1.7.0 (Feb 18, 2024)
====================

- Respect the ``CPATH/C_INCLUDE_PATH`` environment variables during install.

- Add the uniq address to the string representation of ``InputDevice``.

- Improved method for finding the device node corresponding to a uinput device (`#206 <https://github.com/gvalkov/python-evdev/pull/206>`_).

- Repository TLC (reformatted with ruff, fixed linting warnings, moved packaging metadata to ``pyproject.toml`` etc.).


1.6.1 (Jan 20, 2023)
====================

- Fix generation of ``ecodes.c`` when the path to ``sys.executable`` contains spaces.


1.6.0 (Jul 17, 2022)
====================

- Fix Python 3.11 compatibility (`#174 <https://github.com/gvalkov/python-evdev/pull/174>`_).


1.5.0 (Mar 24, 2022)
====================

- Fix documentation (`#163 <https://github.com/gvalkov/python-evdev/pull/163>`_, `#160 <https://github.com/gvalkov/python-evdev/pull/160>`_).

- Re-enable TTY echo at evtest exit (`#155 <https://github.com/gvalkov/python-evdev/pull/155>`_).

- Fix ``ImportError: sys.meta_path is None, Python is likely shutting down`` (`#154 <https://github.com/gvalkov/python-evdev/pull/154>`_).

- Closing the input device file descriptor in ``InputDevice.close()`` now
  happens in the main thread, instead of in a new thread (reverts `#146
  <https://github.com/gvalkov/python-evdev/pull/146>`_).

- Fix ``util.find_ecodes_by_regex`` not working across all supported Python versions (`#152 <https://github.com/gvalkov/python-evdev/pull/152>`_).



1.4.0 (Jan 16, 2021)
====================

- Fix ``InputDevice.set_absinfo`` to allow setting parameters to zero.

- Fix off-by-one in ``ioctl_EVIOCG_bits``, which causes value at the end of the
  list to not be reported back (`#131 <https://github.com/gvalkov/python-evdev/pull/131>`_).

- Fix ``set_absinfo`` to allow setting parameters to zero (`#128 <https://github.com/gvalkov/python-evdev/pull/128>`_).

- Fix leak when returning ``BlockingIOError`` from a read (`#143 <https://github.com/gvalkov/python-evdev/pull/143>`_).

- Fix "There is no current event loop in thread" error for non asyncio code
  (`#146 <https://github.com/gvalkov/python-evdev/pull/146>`_).

- Prevent ``InputDevice`` destructor from blocking (`#145 <https://github.com/gvalkov/python-evdev/pull/145>`_).

- Add missing return codes to ``os.strerror()`` calls and fix force feedback
  example in docs (`#138 <https://github.com/gvalkov/python-evdev/pull/137>`_).

- Add the ``util.find_ecodes_by_regex()`` helper function.



1.3.0 (Jan 12, 2020)
====================

- Fix build on 32bit arches with 64bit time_t

- Add functionality to query device properties. See ``InputDevice.input_props``
  and the ``input_props`` argument to ``Uinput``.

- ``KeyEvent`` received an ``allow_unknown`` constructor argument, which
  determines what will happen when an event code cannot be mapped to a keycode.
  The default and behavior so far has been to raise ``KeyError``. If set to
  ``True``, the keycode will be set to the event code formatted as a hex number.

- Add ``InputDevice.set_absinfo()`` and ``InputDevice.absinfo()``.

- Instruct the asyncio event loop to stop monitoring the fd of the input device
  when the device is closed.


1.2.0 (Apr 7, 2019)
====================

- Add UInput support for the resolution parameter in AbsInfo. This brings
  support for the new method of uinput device setup, which was `introduced in
  Linux 4.5`_ (thanks to `@LinusCDE`_).

- Vendor and product identifiers can be greater or equal to `0x8000` (thanks
  `@ivaradi`_).


1.1.2 (Sep 1, 2018)
====================

- Fix installation on kernels <= 4.4.

- Fix uinput creation ignoring absinfo settings.


1.1.0 (Aug 27, 2018)
====================

- Add support for handling force-feedback effect uploads (many thanks to `@ndreys`_).

- Fix typo preventing ff effects that need left coefficients from working.


1.0.0 (Jun 02, 2018)
====================

- Prevent ``Uinput`` device creation raising ``Objects/longobject.c:415: bad
  argument to internal function`` when a non-complete ``AbsInfo`` structure is
  passed. All missing ``AbsInfo`` fields are set to 0.

- Fix ``Uinput`` device creation raising ``KeyError`` when a capability filtered
  by default is not present.

- The ``InputDevice.fn`` attribute was deprecated in favor of ``InputDevice.path``.
  Using the former will show a ``DeprecationWarning``, but would otherwise continue
  working as before.

- Fix ``InputDevice`` comparison raising ``AttributeError`` due to a non-existant
  ``path`` attribute.

- Fix asyncio support in Python 3.5+.

- Uploading FF effect now works both on Python 2.7 and Python 3+.

- Remove the ``asyncore`` example from the tutorial.


0.8.1 (Mar 24, 2018)
====================

- Fix Python 2 compatibility issue in with ``Uinput.from_device``.

- Fix minor `evdev.evtest` formatting issue.


0.8.0 (Mar 22, 2018)
====================

- Fix ``InputDevice`` comparison on Python 2.

- The device path is now considered when comparing two devices.

- Fix ``UInput.from_device`` not correctly merging the capabilities of
  selected devices.

- The list of excluded event types in ``UInput.from_device`` is now
  configurable. For example::

    UInput.from_device(dev, filtered_types=(EV_SYN, EV_FF))

  In addition, ``ecodes.EV_FF`` is now excluded by default.

- Add a context manager for grabbing access to a device -
  ``InputDevice.grab_context``. For example::

    with dev.grab_context():
        pass

- Add the ``InputDevice.uniq`` attribute, which contains the unique identifier
  of the device. As with ``phys``, this attribute may be empty (i.e. `''`).


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

- Disable tty echoing while evtest is running.
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
.. _`@ndreys`: https://github.com/ndreys
.. _`@LinusCDE`: https://github.com/gvalkov/python-evdev/pulls/LinusCDE
.. _`@ivaradi`: https://github.com/gvalkov/python-evdev/pull/104

.. _`introduced in Linux 4.5`: https://github.com/torvalds/linux/commit/052876f8e5aec887d22c4d06e54aa5531ffcec75
.. _issue21121: http://bugs.python.org/issue21121
.. _`#63`:      https://github.com/gvalkov/python-evdev/issues/63
.. _`#67`:      https://github.com/gvalkov/python-evdev/issues/67
