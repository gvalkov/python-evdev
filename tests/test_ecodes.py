from evdev import ecodes
from evdev import ecodes_runtime


prefixes = "KEY ABS REL SW MSC LED BTN REP SND ID EV BUS SYN FF_STATUS FF UI_FF"


def to_tuples(val):
    t = lambda x: tuple(x) if isinstance(x, list) else x
    return map(t, val)


def test_equality():
    keys = []
    for i in prefixes.split():
        keys.extend(getattr(ecodes, i, {}).keys())

    assert set(keys) == set(ecodes.ecodes.values())


def test_access():
    assert ecodes.KEY_A == ecodes.ecodes["KEY_A"] == ecodes.KEY_A
    assert ecodes.KEY[ecodes.ecodes["KEY_A"]] == "KEY_A"
    assert ecodes.REL[0] == "REL_X"


def test_overlap():
    vals_ff = set(to_tuples(ecodes.FF.values()))
    vals_ff_status = set(to_tuples(ecodes.FF_STATUS.values()))
    assert bool(vals_ff & vals_ff_status) is False


def test_generated():
    e_run = vars(ecodes_runtime)
    e_gen = vars(ecodes)

    def keys(v):
        res = {k for k in v.keys() if not k.startswith("_") and not k[1].islower()}
        return res

    assert keys(e_run) == keys(e_gen)