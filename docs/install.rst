From an OS package
==================

Python-evdev has been packaged for the following distributions:

.. raw:: html

    <a href="https://repology.org/project/python:evdev/versions">
      <img src="https://repology.org/badge/vertical-allrepos/python:evdev.svg?exclude_sources=modules,site&exclude_unsupported=1" alt="Packaging status">
    </a>

Consult the documentation of your OS package manager for installation instructions.


From source
===========

The latest stable version of *python-evdev* can be installed from pypi_,
provided that you have a compiler, pip_ and the Python and Linux development
headers installed on your system. The exact packages are distribution specific
and typically falls into one of the following:

On a Debian compatible OS:

.. code-block:: bash

    $ apt install python-dev python-pip gcc
    $ apt install linux-headers-$(uname -r)

On a RedHat compatible OS:

.. code-block:: bash

    $ dnf install python-devel python-pip gcc
    $ dnf install kernel-headers-$(uname -r)

On Arch Linux and derivatives:

.. code-block:: bash

    $ pacman -S core/linux-api-headers python-pip gcc

Once all OS dependencies are available, you may install *python-evdev* using
pip_, preferably in a virtual environment:

.. code-block:: bash

    # Install globally (not recommended).
    $ sudo python3 -m pip install evdev

    # Install for the current user.
    $ python3 -m pip install --user evdev

    # Install in a virtual environment.
    $ python3 -m venv path
    $ source path/bin/activate
    $ python3 -m pip install evdev


Specifying header locations
---------------------------

By default, the setup script will look for the ``input.h`` and
``input-event-codes.h`` [#f1]_ header files in ``/usr/include/linux``.

The ``--evdev-headers`` option of the setuptools ``build_ext`` command
overrides the header search location. It accepts one or more colon-separated
paths. For example:

.. code-block:: bash

    $ python3 setup.py build_ext \
        --evdev-headers buildroot/input.h:buildroot/input-event-codes.h \
        --include-dirs  buildroot/ \
        install  # or any other command (e.g. develop, bdist, bdist_wheel)


From a binary package
=====================

You may choose to install a precompiled version of *python-evdev* from pypi. The
`evdev-binary`_ package provides binary wheels that have been compiled on EL8
against the 4.18.0 kernel headers.

.. code-block:: bash

    $ python3 -m pip install evdev-binary

While the evdev interface is stable, the precompiled version may not be fully
compatible or expose all the features of your running kernel. For best results,
it is recommended to use an OS package or to install from source.


.. [#f1] ``input-event-codes.h`` is found only in recent kernel versions.
.. _pypi:              https://pypi.org/project/evdev
.. _evdev-binary:      https://pypi.org/project/evdev-binary
.. _pip:               http://pip.readthedocs.org/en/latest/installing.html
