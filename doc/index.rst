*evdev* documentation
========================================

:mod:`evdev` provides bindings to the generic input event interface in
Linux.  The *evdev* interface serves the purpose of passing events
generated in the kernel directly to userspace through character
devices that are typically located in ``/dev/input/``.

:mod:`evdev` also comes with bindings to ``uinput``, the userspace
input subsystem. ``Uinput`` allows userspace programs to create and
handle input devices from which they can inject events directly into
the input subsystem.


Tutorial
--------

Listing accessible event devices::

    >>> from evdev import InputDevice, list_devices

    >>> devices = map(InputDevice, list_devices())

    >>> for dev in devices:
    ...    print( '%-20s %-32s %s' % (dev.fn, dev.name, dev.phys) )
    /dev/input/event1    Dell Dell USB Keyboard           usb-0000:00:12.1-2/input0
    /dev/input/event0    Dell Premium USB Optical Mouse   usb-0000:00:12.0-2/input0

Listing device capabilities::

    >>> dev = InputDevice('/dev/input/event0')

    >>> print(dev)
    device /dev/input/event0, name "Dell Premium USB Optical Mouse", phys "usb-0000:00:12.0-2/input0"

    >>> dev.capabilities()
    >>> { 0: [0, 1, 2], 1: [272, 273, 274, 275], 2: [0, 1, 6, 8], 4: [4] }

    >>> dev.capabilities(verbose=True)
    >>> { ('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('SYN_MT_REPORT', 2)],
    >>>   ('EV_KEY', 1): [('BTN_MOUSE', 272), ('BTN_RIGHT', 273), ('BTN_MIDDLE', 274), ('BTN_SIDE', 275)], ...

Accessing input subsystem constants::

    >>> from evdev import ecodes
    >>> ecodes.KEY_A, ecodes.ecodes['KEY_A']
    (30, 30)
    >>> ecodes.KEY[30]
    'KEY_A'
    >>> ecodes.bytype[ecodes.EV_KEY][30]
    'KEY_A'


Reading events::

    >>> from evdev import InputDevice, categorize, ecodes
    >>> from select import select
    >>> dev = InputDevice('/dev/input/event1')

    >>> print(dev)
    device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"

    >>> while True:
    ...    r,w,x = select([dev], [], [])
    ...    for event in dev.read():
    ...        if event.type == ecodes.EV_KEY:
    ...            print(categorize(e))
    ... # hitting a and holding space
    key event at 1337016188.396030, 30 (KEY_A), down
    key event at 1337016188.492033, 30 (KEY_A), up
    key event at 1337016189.772129, 57 (KEY_SPACE), down
    key event at 1337016190.275396, 57 (KEY_SPACE), hold
    key event at 1337016190.284160, 57 (KEY_SPACE), up


Reading events with asyncore::

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


Associating classes with event types (see :mod:`events <evdev.events>`)::

    >>> from evdev import categorize, event_factory, ecodes

    >>> class SynEvent(object):
    ...     def __init__(self, event):
    ...         ...

    >>> event_factory[ecodes.EV_SYN] = SynEvent


Injecting events::

    >>> from evdev import ecodes, UInput, events

    >>> ui = UInput('test-device', 0x0001, 0x0002, 0x0003)
    >>> ev = events.InputEvent(1334414993, 274296, ecodes.EV_KEY, ecodes.KEY_A, 1)

    >>> ui.write(ev)
    >>> ui.syn()
    >>> ui.close()


Requirements
------------

:mod:`evdev` contains C extension modules and requires the Python development
headers as well as the kernel headers.

On a Debian compatible OS:

.. code-block:: bash

    $ apt-get install python-dev
    $ apt-get install linux-headers-$(uname -r)

On a Redhat compatible OS:

.. code-block:: bash

    $ yum install python-devel
    $ yum install kernel-headers-$(uname -r)

:mod:`evdev` itself requires CPython **>= 2.7**


Installation
------------

Assuming all requirements have been met, the latest stable version of
:mod:`evdev` can be installed from PyPi_, while the development version can be
installed from github_:

.. code-block:: bash

    $ pip install evdev  # latest stable version
    $ pip install git+git://github.com/gvalkov/python-evdev.git # latest development version

Alternatively, :mod:`evdev` can be installed like any other
:mod:`distutils`/:mod:`setuptools`/:mod:`packaging` package:

.. code-block:: bash

    $ git clone github.com/gvalkov/python-evdev.git
    $ cd python-evdev
    $ git checkout $versiontag
    $ python setup.py install



Module Contents
---------------

.. toctree::
   :maxdepth: 2

   moduledoc


Similar Projects
----------------

* `python-uinput`_
* `ruby-evdev`_
* `evdev`_ (ctypes)


License
-------

:mod:`evdev` is released under the terms of the `New BSD License`_.


Todo
----

* Use libudev to find the uinput device node as well as the other input
  devices. Their locations are currently assumed to be ``/dev/uinput`` and
  ``/dev/input/*``.

* More tests.

* Better uinput support (setting device capabilities as in `python-uinput`_)

* Expose more input subsystem functionality (``EVIOCSKEYCODE``, ``EVIOCGREP`` etc)

* Figure out if using ``linux/input.h`` and other kernel headers in your
  userspace program binds it to the GPL2.


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _`New BSD License`: https://raw.github.com/gvalkov/python-evdev/master/LICENSE
.. _PyPi:              http://pypi.python.org/pypi/evdev
.. _github:            https://github.com/gvalkov/python-evdev
.. _python-uinput:     https://github.com/tuomasjjrasanen/python-uinput
.. _ruby-evdev:        http://technofetish.net/repos/buffaloplay/ruby_evdev/doc/
.. _evdev:             http://svn.navi.cx/misc/trunk/python/evdev/
