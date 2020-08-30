from evdev import util


def test_filter_ecodes():
    assert list(util.filter_ecodes(r"KEY_[F-H]$")) == [33, 34, 35]
