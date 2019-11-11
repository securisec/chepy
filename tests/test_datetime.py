from chepy import Chepy


def test_from_unix_ts():
    assert Chepy("1573426649").from_unix_ts().o == "Sun Nov 10 17:57:29 2019"


def test_to_unix_ts():
    assert Chepy("Sun Nov 10 17:57:29 2019").to_unix_ts().o == 1573426649
