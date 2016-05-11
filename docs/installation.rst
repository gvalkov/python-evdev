Extended Installation
---------------------

Specifying header location
==========================

You may use the ``--evdev-headers`` option to the ``build_ext`` setuptools
command to specify the location of ``input.h`` and ``input-event-codes.h``
(optionally). It accepts one or more colon-separated paths. For example:

.. code-block:: bash

    $ python setup.py build_ext \
        --evdev-headers buildroot/input.h:buildroot/input-event-codes.h \
        --include-dirs  buildroot/ \
        install  # or any other command (e.g. develop, bdist, bdist_wheel)

If nothing is specified, ``build_ext`` will search in ``/usr/include/linux`` by
default.
