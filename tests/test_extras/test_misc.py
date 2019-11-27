from chepy.extras.misc import *


def test_shannon_entropy():
    assert shannon_entropy("some text") == 2.725480556997868
    assert shannon_entropy("some text", unit="hartley") == 0.8204514002553331
    assert shannon_entropy("some text", unit="natural") == 1.8891591637540215


def test_IC():
    with open("tests/files/hello", "rb") as f:
        data = f.read()
    assert index_of_coincidence(data) == 0
