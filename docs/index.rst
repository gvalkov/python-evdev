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
    <li><a href="search.html"  title="Jump to Search">Search</a></li>
    <li><a href="#quick-start" title="Jump to quick start">Quick Start</a></li>
    <li><a href="apidoc.html"  title="Jump to API reference">API Reference</a></li>
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

**Installing:**

The following GNU/Linux distributions have *python-evdev* in their repositories:

.. raw:: html

    <div style="margin:1em;">
    <a href="https://aur.archlinux.org/packages/python-evdev/"><img height="40px" src="_static/pacifica-icon-set/distributor-logo-archlinux.png"></a>
    <a href="http://packages.ubuntu.com/saucy/python-evdev">   <img height="40px" src="_static/pacifica-icon-set/distributor-logo-ubuntu.png"></a>
    <!--
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-raspbian.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-fedora.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-debian.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-linux-mint.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-opensuse.png"></a>
    --!>
    </div>

The latest stable version of *python-evdev* can be installed from
pypi_, provided that you have gcc/clang, pip_ and the Python and Linux
development headers installed on your system. Installing them is
distribution specific and usually falls in one of these categories:

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

**Listing accessible event devices:**

::

    >>> from evdev import InputDevice, list_devices

    >>> devices = [InputDevice(fn) for fn in list_devices()]
    >>> for dev in devices:
    ...    print(dev.fn, dev.name, dev.phys)
    /dev/input/event1    Dell Dell USB Keyboard   usb-0000:00:12.1-2/input0
    /dev/input/event0    Dell USB Optical Mouse   usb-0000:00:12.0-2/input0


**Reading events from a device:**

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

**Accessing evdev constants:**

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

**Further information:**

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

  * :mod:`util <evdev.util>`

    - :class:`list_devices() <evdev.util.list_devices>`

    - :class:`is_device() <evdev.util.is_device>`

    - :class:`categorize() <evdev.util.categorize>`

    - :class:`categorize() <evdev.util.categorize>`

  * :mod:`uinput <evdev.uinput>`

    - :class:`UInput <evdev.uinput.UInput>`

  * :mod:`ecodes <evdev.ecodes>`


News
----
.. include:: news.rst

See :doc:`changelog <changelog>` for a full list of changes.


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
.. _example:           https://github.com/gvalkov/python-evdev/tree/master/bin
