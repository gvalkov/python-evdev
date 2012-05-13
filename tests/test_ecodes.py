# encoding: utf-8

from evdev import ecodes

def test_equality():
    keys = []
    for i in 'KEY','ABS','REL','SW','MSC','LED','BTN','REP','SND','ID','EV','BUS','SYN':
        keys.extend(getattr(ecodes, i, {}).keys())

    assert set(keys) == set(ecodes.ecodes.values())

def test_access():
    assert ecodes.KEY_A == ecodes.ecodes['KEY_A'] == ecodes.KEY_A
    assert ecodes.KEY[ecodes.ecodes['KEY_A']] == 'KEY_A'
    assert ecodes.REL[0] == 'REL_X'

