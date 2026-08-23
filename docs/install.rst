OS package
==========

Python-evdev has been packaged for the following distributions:

.. raw:: html

    <a href="https://repology.org/project/python:evdev/versions">
      <img src="https://repology.org/badge/vertical-allrepos/python:evdev.svg?exclude_sources=modules,site&exclude_unsupported=1" alt="Packaging status">
    </a>

Consult the documentation of your OS package manager for installation instructions.


From source
===========

The latest stable version of *python-evdev* can be installed from PyPi_,
provided that you have a compiler, pip and the Python and Linux development
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

Once all OS dependencies are installed, you may use your preferred Python
package manager to install *python-evdev*. For example:

.. code-block:: bash

    # Using pip (user install).
    $ python3 -m pip install --user evdev

    # Using pip in a virtual environment.
    $ python3 -m venv venv_path && venv_path/bin/python3 -m pip install evdev

    # Using uv.
    uv add evdev  # or uv pip install evdev


Specifying header locations
---------------------------

By default, the setup script will look for the ``input.h`` and
``input-event-codes.h`` header files in ``/usr/include/linux``.

The ``--evdev-headers`` option of the setuptools ``build_ext`` command
overrides the header search location. It accepts one or more colon-separated
paths. For example:

.. code-block:: bash

    $ python3 setup.py build_ext \
        --evdev-headers buildroot/input.h:buildroot/input-event-codes.h \
        --include-dirs  buildroot/ \
        install  # or any other command (e.g. develop, bdist, bdist_wheel)


Binary wheels
=============

The `evdev-binary`_ package on PyPi provides binary wheels that have been
compiled on `manylinux_2_34`_ (AlmaLinux 9, glibc 2.34, kernel 5.14.0). Wheels
for musl-based systems are built on the `musllinux_1_2`_ image (Alpine Linux
3.22).

.. code-block:: bash

    $ python3 -m pip install evdev-binary

While the evdev interface is stable, the precompiled version may not be fully
compatible or expose all the features of your running kernel. For best results,
it is recommended to use an OS package or to install from source.


.. _PyPi:              https://pypi.org/project/evdev
.. _evdev-binary:      https://pypi.org/project/evdev-binary
.. _manylinux_2_34:    https://github.com/pypa/manylinux
.. _musllinux_1_2:     https://peps.python.org/pep-0600/
