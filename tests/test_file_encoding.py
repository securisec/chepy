from pathlib import Path
from chepy import Chepy

path = str(Path().absolute() / "tests/files/encoding")


def test_read_file():
    c = Chepy(path).load_file()
    assert c.out[0:10] == b"=0GDAqREMS"


def test_rot_13():
    c = Chepy(path).load_file()
    assert c.rot_13().out[:10] == b"=0TQNdERZF"


def test_reverse():
    c = Chepy(path).load_file()
    assert c.reverse().out[0:10] == b"E0SMERSADy"


def test_flag():
    c = Chepy(path).load_file()
    assert (
        c.reverse().rot_13().from_base64().from_base32().str_from_hexdump().out
        == b"StormCTF{Spot3:DcEC6181F48e3B9D3dF77Dd827BF34e0}"
    )
