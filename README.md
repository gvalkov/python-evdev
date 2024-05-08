# evdev

<p>
    <a href="https://pypi.python.org/pypi/evdev"><img alt="pypi version" src="https://img.shields.io/pypi/v/evdev.svg"></a>
    <a href="https://github.com/gvalkov/python-evdev/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/evdev"></a>
    <a href="https://repology.org/project/python:evdev/versions"><img alt="Packaging status" src="https://repology.org/badge/tiny-repos/python:evdev.svg"></a>
</p>

This package provides bindings to the generic input event interface in Linux.
The *evdev* interface serves the purpose of passing events generated in the
kernel directly to userspace through character devices that are typically
located in `/dev/input/`.

This package also comes with bindings to *uinput*, the userspace input
subsystem. *Uinput* allows userspace programs to create and handle input devices
that can inject events directly into the input subsystem.

***Documentation:***  
https://python-evdev.readthedocs.io/en/latest/

***Development:***  
https://github.com/gvalkov/python-evdev

***Package:***  
https://pypi.python.org/pypi/evdev

***Changelog:***  
https://python-evdev.readthedocs.io/en/latest/changelog.html