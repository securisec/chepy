from chepy import Chepy


def test_rot_47():
    assert Chepy("some").rot_47().output == "D@>6"


def test_rotate():
    assert Chepy("some data").rotate(20).output == "migy xunu"


def test_xor_utf():
    assert Chepy("some data").xor("UD", "utf").output.decode() == "&+8!u 404"


def test_xor_base64():
    assert Chepy("&+8!u 404").xor("VUQ=", "base64").output.decode() == "some data"


def test_xor_hex():
    assert Chepy("some data").xor("5544", "hex").output.decode() == "&+8!u 404"


def test_xor_binary():
    assert (
        Chepy("./tests/files/hello", True)
        .to_hex()
        .xor("A", "utf")
        .to_hex()
        .o.decode()[0:6]
        == "222727"
    )
