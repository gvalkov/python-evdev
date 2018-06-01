Introduction
------------

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


.. toctree::
   :caption: Installation
   :maxdepth: 2

   install

.. toctree::
   :caption: Usage

   usage
   tutorial
   apidoc

.. toctree::
   :caption: Project
   :maxdepth: 2

   scope
   changelog


License
-------

This package is released under the terms of the `Revised BSD License`_.

.. _`Revised BSD License`: https://raw.github.com/gvalkov/python-evdev/master/LICENSE
.. _evdev:             http://svn.navi.cx/misc/trunk/python/evdev/
