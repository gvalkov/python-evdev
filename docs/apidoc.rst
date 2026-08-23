API
---

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
   :members: DeviceInfo, AbsInfo, KbdInfo
   :special-members:
   :exclude-members: __dict__, __str__, __module__, __del__, __slots__, __repr__,
   :member-order: bysource

.. autoclass:: evdev.device.InputDevice
   :members:

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

.. automodule:: evdev.ecodes_generated
   :members:
   :exclude-members: __module__, keys, ecodes, bytype
   :member-order: bysource

.. py:data:: evdev.ecodes.keys
   :type:  dict[int, str | tuple[str]]
   :value: {0: "KEY_RESERVED", 1: "KEY_ESC", 2: "KEY_1", ...}

   Keys are a combination of all ``BTN`` and ``KEY`` codes.

.. py:data:: evdev.ecodes.bytype
   :type:  dict[int, dict[int, str | tuple[str]]]
   :value: {0: {0: "SYN_REPORT", 1: "SYN_CONFIG", 2: "SYN_MT_REPORT", 3: "SYN_DROPPED"}, ...}

   Mapping of event types to other value/name mappings.

.. py:data:: evdev.ecodes.ecodes
   :type:  dict[str, int]
   :value: {"KEY_END": 107, "FF_RUMBLE": 80, "KEY_KPDOT": 83, "KEY_CNT": 768, ...}

   Mapping of names to values

.. py:data:: evdev.ecodes.KEY
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.ABS
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.SW
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.MSC
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.LED
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.BTN
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.REP
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.SND
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.ID
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.EV
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.BUS
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.SYN
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.FF
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.UI_FF
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.FF_STATUS
   :type: dict[int, str | tuple[str]]

.. py:data:: evdev.ecodes.INPUT_PROP
   :type: dict[int, str | tuple[str]]
