API Reference
-------------

``events``
============

.. automodule:: evdev.events
   :members: InputEvent, KeyEvent, AbsEvent, RelEvent, SynEvent, event_factory
   :undoc-members:
   :exclude-members: __dict__, __str__, __module__, __del__, __slots__, __repr__
   :member-order: bysource


``eventio``
============

.. automodule:: evdev.eventio
   :members: EventIO
   :undoc-members:
   :special-members:
   :exclude-members: __dict__, __str__, __module__, __del__, __slots__, __repr__
   :member-order: bysource

``eventio_async``
=================

.. automodule:: evdev.eventio_async
   :members: EventIO
   :undoc-members:
   :special-members:
   :exclude-members: __dict__, __str__, __module__, __del__, __slots__, __repr__
   :member-order: bysource

``device``
============

.. automodule:: evdev.device
   :members: InputDevice, DeviceInfo, AbsInfo, KbdInfo
   :undoc-members:
   :special-members:
   :exclude-members: __dict__, __str__, __module__, __del__, __slots__, __repr__
   :member-order: bysource

``uinput``
============

.. automodule:: evdev.uinput
   :members: UInput
   :special-members:
   :exclude-members: __dict__, __str__, __module__, __del__, __slots__, __repr__
   :member-order: bysource

``util``
==========

.. automodule:: evdev.util
   :members: list_devices, is_device, categorize, resolve_ecodes, resolve_ecodes_dict
   :member-order: bysource

``ecodes``
============

.. automodule:: evdev.ecodes
   :members:
   :exclude-members: __module__, keys, ecodes, bytype
   :member-order: bysource

.. autodata:: evdev.ecodes.keys
   :annotation: {0: 'KEY_RESERVED', 1: 'KEY_ESC', 2: 'KEY_1', ...}

.. autodata:: evdev.ecodes.ecodes
   :annotation: {'KEY_END': 107, 'FF_RUMBLE': 80, 'KEY_KPDOT': 83, 'KEY_CNT': 768, ...}'

.. autodata:: evdev.ecodes.bytype
   :annotation: {0: {0: 'SYN_REPORT', 1: 'SYN_CONFIG', 2: 'SYN_MT_REPORT', 3: 'SYN_DROPPED'}, ...}
