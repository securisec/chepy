from chepy.extras.combinatons import *


def test_all_combinations():
    combo = all_combinations_from_list(["a", 1, "\x10"])
    assert type(next(combo)) == tuple
    assert len([x for x in combo]) == 15

def test_all_hex():
    assert len(all_hex_chars()) == 256
