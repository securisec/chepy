from chepy import Chepy


def test_uuid():
    assert len(Chepy('').generate_uuid().o) == 36

