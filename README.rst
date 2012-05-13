*evdev* 
----------------------------------------

*evdev* provides bindings to the generic input event interface in Linux.
The *evdev* interface serves the purpose of passing events generated in the
kernel directly to userspace through character devices that are typically
located in `/dev/input/`. 

*evdev* also comes with bindings to *uinput*, the userspace input
subsystem. *Uinput* allows userspace programs to create and handle input
devices from which they can inject events directly into the input subsystem.


Documentation:
    +---------+-----------------------------------------+ 
    | devel   | http://gvalkov.github.com/python-evdev  |
    +---------+-----------------------------------------+ 
    | stable  | http://packages.python.org/evdev        |
    +---------+-----------------------------------------+ 

Development:
    https://github.com/gvalkov/python-evdev

PyPi:
    http://pypi.python.org/pypi/evdev
