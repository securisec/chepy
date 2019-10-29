from chepy.helpers import *


def test_all_combinations():
    combo = all_combinations_from_list(["a", 1, "\x10"])
    assert type(next(combo)) == tuple
    assert len([x for x in combo]) == 15

