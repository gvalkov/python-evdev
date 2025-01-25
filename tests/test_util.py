from evdev import util


def test_match_ecodes_a():
    res = util.find_ecodes_by_regex("KEY_ZOOM.*")
    assert res == {1: [372, 418, 419, 420]}
    assert dict(util.resolve_ecodes_dict(res)) == {
        ("EV_KEY", 1): [
            (("KEY_FULL_SCREEN", "KEY_ZOOM"), 372),
            ("KEY_ZOOMIN", 418),
            ("KEY_ZOOMOUT", 419),
            ("KEY_ZOOMRESET", 420),
        ]
    }

    res = util.find_ecodes_by_regex(r"(ABS|KEY)_BR(AKE|EAK)")
    assert res == {1: [411], 3: [10]}
    assert dict(util.resolve_ecodes_dict(res)) == {
        ("EV_KEY", 1): [("KEY_BREAK", 411)],
        ("EV_ABS", 3): [("ABS_BRAKE", 10)],
    }
