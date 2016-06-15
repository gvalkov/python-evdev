Scope and status
----------------

Python-evdev exposes most of the more common interfaces defined in the evdev
subsystem. Reading and injecting events is well supported and has been tested
with nearly all event types.

The basic functionality for reading and uploading force-feedback events is
there, but it has not been exercised sufficiently. A major shortcoming of the
uinput wrapper is that it does not support force-feedback devices at all (see
issue `#23`_).

Some characters, such as ``:`` (colon), cannot be easily injected (see issue
`#7`_), Translating them into UInput events would require knowing the kernel
keyboard translation table, which is beyond the scope of python-evdev. Please
look into the following projects if you need more complete or convenient input
injection support.

- python-uinput_
- uinput-mapper_
- PyUserInput_ (cross-platform, works on the display server level)
- pygame_ (cross-platform)


.. _python-uinput:     https://github.com/tuomasjjrasanen/python-uinput
.. _uinput-mapper:     https://github.com/MerlijnWajer/uinput-mapper
.. _PyUserInput:       https://github.com/PyUserInput/PyUserInput
.. _pygame:            http://www.pygame.org/

.. _`#7`:  https://github.com/gvalkov/python-evdev/issues/7
.. _`#23`: https://github.com/gvalkov/python-evdev/pull/23
