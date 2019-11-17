from chepy.extras.combinatons import *


def test_all_combinations():
    combo = generate_combo(["a", 1, "\x10"])
    assert type(next(combo)) == tuple
    assert len([x for x in combo]) == 15
    assert len(list(generate_combo(['a', 'b', 'c'], 2, 3))) == 12
    assert len(list(generate_combo(['a', 'b', 'c'], max_length=2))) == 6

def test_all_hex():
    assert len(hex_chars()) == 256
