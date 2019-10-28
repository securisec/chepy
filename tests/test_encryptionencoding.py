from chepy import Chepy


def test_rot_47():
    assert Chepy("some").rot_47.output == "D@>6"


def test_rotate():
    assert Chepy("some data").rotate(20).output == "migy xunu"

