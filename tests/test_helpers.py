from chepy.helpers import *


def test_all_combinations():
    combo = all_combinations_from_list(["a", 1, "\x10"])
    assert type(next(combo)) == tuple
    assert len([x for x in combo]) == 15


def test_factordb():
    assert (
        factordb(
            833810193564967701912362955539789451139872863794534923259743419423089229206473091408403560311191545764221310666338878019
        )["id"]
        == "1100000000886507194"
    )

