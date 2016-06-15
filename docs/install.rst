From a binary package
=====================

Python-evdev has been packaged for the following GNU/Linux distributions:


.. raw:: html

    <div style="margin:1em;">
    <a href="https://aur.archlinux.org/packages/python-evdev/">
      <img height="30px" src="_static/pacifica-icon-set/distributor-logo-archlinux.png">
    </a>
    <a href="http://packages.ubuntu.com/wily/python-evdev">
      <img height="30px" src="_static/pacifica-icon-set/distributor-logo-ubuntu.png">
    </a>
    <a href="https://copr.fedorainfracloud.org/coprs/gvalkov/python-evdev/">
      <img height="30px" src="_static/pacifica-icon-set/distributor-logo-fedora.png">
    </a>
    <!--
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-raspbian.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-debian.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-linux-mint.png"></a>
    <a href=""><img height="40px" src="_static/pacifica-icon-set/distributor-logo-opensuse.png"></a>
    --!>
    </div>

Consult the relevant documentation of your OS package manager for installation instructions.


From source
===========

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

Once all dependencies are available, you may install *python-evdev* using pip_:

.. code-block:: bash

    $ sudo pip install evdev


Specifying header locations
===========================

By default, the setup script will look for the ``input.h`` and
``input-event-codes.h`` [#f1]_ header files ``/usr/include/linux``.

You may use the ``--evdev-headers`` option to the ``build_ext`` setuptools
command to specify the location of these header files. It accepts one or more
colon-separated paths. For example:

.. code-block:: bash

    $ python setup.py build_ext \
        --evdev-headers buildroot/input.h:buildroot/input-event-codes.h \
        --include-dirs  buildroot/ \
        install  # or any other command (e.g. develop, bdist, bdist_wheel)

.. [#f1] ``input-event-codes.h`` is found only in more recent kernel versions.


.. _pypi:              http://pypi.python.org/pypi/evdev
.. _github:            https://github.com/gvalkov/python-evdev
.. _pip:               http://pip.readthedocs.org/en/latest/installing.html
.. _example:           https://github.com/gvalkov/python-evdev/tree/master/examples
.. _`async/await`:     https://docs.python.org/3/library/asyncio-task.html
