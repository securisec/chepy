from chepy import Chepy


def test_from_unix_timestamp():
    assert Chepy("1573426649").from_unix_timestamp().o[-4:] == "2019"
    assert Chepy("1546573919").from_unix_timestamp(utc=True).o[-4:] == "2019"


# def test_to_unix_timestamp():
#     assert Chepy("Sun Nov 10 17:57:29 2019").to_unix_timestamp().o == 1573426649
