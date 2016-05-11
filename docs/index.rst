.. raw:: html

    <div style="float:right;
         margin:1em;
         padding: 0.5em 1em 0em 1em;
         background-color: #efefef;
         border-width: thin;
         border-style: dotted;
         border-color: #0C3762;
         ">
    <strong>Links</strong><br/>
    <ul>
    <li><a href="#news"  title="Jump to News">News</a></li>
    <li><a href="search.html"   title="Jump to Search">Search</a></li>
    <li><a href="#quick-start"  title="Jump to quick start">Quick Start</a></li>
    <li><a href="tutorial.html" title="Jump to turorial page">Tutorial</a></li>
    <li><a href="apidoc.html"   title="Jump to API reference">API Reference</a></li>
    <li><a href="https://github.com/gvalkov/python-evdev"  title="Jump to Github">Github</a></li>
    </ul>
    <!--
    <hr/>
    <a href="https://github.com/gvalkov/python-evdev">
    <img style="
         display: block;
         margin-left: auto;
         margin-right: auto;
         opacity: 0.9;
         width: 50px;"
    src="_static/github-logo.png" title="Github Repo"/>
    </a>
    -->
    </div>

Synopsis
--------

This package provides bindings to the generic input event interface in
Linux. The *evdev* interface serves the purpose of passing events
generated in the kernel directly to userspace through character
devices that are typically located in ``/dev/input/``.

This package also comes with bindings to *uinput*, the userspace input
subsystem. *Uinput* allows userspace programs to create and handle
input devices that can inject events directly into the input
subsystem.

In other words, *python-evdev* allows you to read and write input
events on Linux. An event can be a key or button press, a mouse
movement or a tap on a touchscreen.

Quick Start
-----------

Installing:
^^^^^^^^^^^

The following GNU/Linux distributions have *python-evdev* in their package
repositories:

.. raw:: html

    <div style="margin:1em;">
    <a href="https://aur.archlinux.org/packages/python-evdev/"><img height="40px" src="_static/pacifica-icon-set/distributor-logo-archlinux.png"></a>
    <a href="http://packages.ubuntu.com/wily/python-evdev">   <img height="40px" src="_static/pacifica-icon-set/distributor-logo-ubuntu.png"></a>
    <!--
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-raspbian.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-fedora.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-debian.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-linux-mint.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-opensuse.png"></a>
    --!>
    </div>

The latest stable version of *python-evdev* can be installed from pypi_,
provided that you have gcc/clang, pip_ and the Python and Linux development
headers installed on your system. Installing them is distribution specific and
typically falls in one of the following categories:

On a Debian compatible OS:

.. code-block:: bash

    $ apt-get install python-dev python-pip gcc
    $ apt-get install linux-headers-$(uname -r)

On a Redhat compatible OS:

.. code-block:: bash

    $ yum install python-devel python-pip gcc
    $ yum install kernel-headers-$(uname -r)

On Arch Linux and derivatives:

.. code-block:: bash

    $ pacman -S core/linux-api-headers python-pip gcc

Installing *python-evdev* with pip_:

.. code-block:: bash

    $ sudo pip install evdev

For more advanced installation options, please read the :doc:`full installation
<installation>` page.

Listing accessible event devices:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> import evdev

    >>> devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    >>> for device in devices:
    ...    print(device.fn, device.name, device.phys)
    /dev/input/event1    Dell Dell USB Keyboard   usb-0000:00:12.1-2/input0
    /dev/input/event0    Dell USB Optical Mouse   usb-0000:00:12.0-2/input0


Reading events from a device:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> import evdev

    >>> device = evdev.InputDevice('/dev/input/event1')
    >>> print(device)
    device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"

    >>> for event in device.read_loop():
    ...     if event.type == evdev.ecodes.EV_KEY:
    ...         print(categorize(event))
    ... # pressing 'a' and holding 'space'
    key event at 1337016188.396030, 30 (KEY_A), down
    key event at 1337016188.492033, 30 (KEY_A), up
    key event at 1337016189.772129, 57 (KEY_SPACE), down
    key event at 1337016190.275396, 57 (KEY_SPACE), hold
    key event at 1337016190.284160, 57 (KEY_SPACE), up

Reading events using async/await:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Python-evdev* proudly supports the new `async/await`_ syntax in Python 3.5:

::

    import asyncio, evdev

    async def print_events(device):
        async for event in device.async_read_loop():
            print(device.fn, evdev.categorize(event), sep=': ')

    device = evdev.InputDevice('/dev/input/event4')
    asyncio.ensure_future(print_events(device))

    loop = asyncio.get_event_loop()
    loop.run_forever()

Accessing evdev constants:
^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Listing and monitoring input devices:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *python-evdev* package also comes with a small command-line program for
listing and monitoring input devices:

.. code-block:: bash

   $ python -m evdev.evtest

More information:
^^^^^^^^^^^^^^^^^

- Read the full :doc:`tutorial <tutorial>`.

- See the example_ programs.

- Refer to the API :doc:`documentation <apidoc>`:

  * :mod:`device <evdev.device>`

    - :class:`AbsInfo <evdev.device.AbsInfo>`

    - :class:`KbdInfo <evdev.device.KbdInfo>`

    - :class:`InputDevice <evdev.device.InputDevice>`

  * :mod:`events <evdev.events>`

    - :class:`InputEvent <evdev.events.InputEvent>`

    - :class:`KeyEvent <evdev.events.KeyEvent>`

    - :class:`RelEvent <evdev.events.RelEvent>`

    - :class:`AbsEvent <evdev.events.AbsEvent>`

    - :class:`SynEvent <evdev.events.SynEvent>`

  * :mod:`eventio <evdev.eventio>`

    - :class:`EventIO <evdev.eventio.EventIO>`

  * :mod:`eventio_async <evdev.eventio_async>`

    - :class:`EventIO <evdev.eventio_async.EventIO>`

  * :mod:`util <evdev.util>`

    - :class:`list_devices() <evdev.util.list_devices>`

    - :class:`is_device() <evdev.util.is_device>`

    - :class:`categorize() <evdev.util.categorize>`

    - :class:`categorize() <evdev.util.categorize>`

  * :mod:`uinput <evdev.uinput>`

    - :class:`UInput <evdev.uinput.UInput>`

  * :mod:`ecodes <evdev.ecodes>`


Scope and Status
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


News
----
.. include:: news.rst

Please refer to the :doc:`changelog <changelog>` for a full list of changes.


License
-------

The :mod:`evdev` package is released under the terms of the `Revised BSD License`_.

.. _`Revised BSD License`: https://raw.github.com/gvalkov/python-evdev/master/LICENSE
.. _python-uinput:     https://github.com/tuomasjjrasanen/python-uinput
.. _ruby-evdev:        http://technofetish.net/repos/buffaloplay/ruby_evdev/doc/
.. _evdev:             http://svn.navi.cx/misc/trunk/python/evdev/

.. _pypi:              http://pypi.python.org/pypi/evdev
.. _github:            https://github.com/gvalkov/python-evdev
.. _pip:               http://pip.readthedocs.org/en/latest/installing.html
.. _example:           https://github.com/gvalkov/python-evdev/tree/master/examples
.. _`async/await`:     https://docs.python.org/3/library/asyncio-task.html

.. _python-uinput:     https://github.com/tuomasjjrasanen/python-uinput
.. _uinput-mapper:     https://github.com/MerlijnWajer/uinput-mapper
.. _PyUserInput:       https://github.com/PyUserInput/PyUserInput
.. _pygame:            http://www.pygame.org/

.. _`#7`:  https://github.com/gvalkov/python-evdev/issues/7
.. _`#23`: https://github.com/gvalkov/python-evdev/pull/23
