"""Validate the native input API without requiring an input device."""

import ctypes
import errno
import subprocess
import sys

import pytest

from evdev import _input, device, ff


@pytest.mark.parametrize("expression", ["None", "0", "'effect'", "[]", "bytearray(64)", "memoryview(bytes(64))"])
def test_upload_effect_rejects_non_bytes(expression):
    # A conversion failure used to dereference NULL. Keep a broken extension
    # from crashing the test runner, and do not leave core dumps behind.
    code = """
import resource
import sys
from evdev import _input
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
try:
    _input.upload_effect(-1, eval(sys.argv[1]))
except TypeError:
    pass
else:
    raise AssertionError('expected TypeError')
"""
    result = subprocess.run([sys.executable, "-c", code, expression], check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("size", [0, 1, ctypes.sizeof(ff.Effect) - 1])
def test_upload_effect_rejects_short_bytes(size):
    with pytest.raises(ValueError, match="effect data"):
        _input.upload_effect(-1, bytes(size))


class EffectBytes(bytes):
    pass


@pytest.mark.parametrize("data", [bytes(ff.Effect()), bytes(ff.Effect()) + b"extra", EffectBytes(bytes(ff.Effect()))])
def test_upload_effect_preserves_ioctl_errors(data):
    # A complete effect must reach ioctl, including bytes subclasses and the
    # previously accepted trailing bytes. Invalid descriptors remain EBADF.
    with pytest.raises(OSError) as error:
        _input.upload_effect(-1, data)
    assert error.value.errno == errno.EBADF


def test_device_upload_effect_uses_complete_structure():
    input_device = device.InputDevice.__new__(device.InputDevice)
    input_device.fd = -1
    effect = ff.Effect()
    effect.id = -1
    with pytest.raises(OSError) as error:
        input_device.upload_effect(effect)
    assert error.value.errno == errno.EBADF
    assert effect.id == -1
    # No descriptor is owned by this stand-in InputDevice.
    input_device.fd = None
