from pathlib import Path
from chepy import Chepy

path = str(Path().absolute() / "tests/files/encoding")


def test_read_file():
    c = Chepy(path).load_file()
    assert c.output[0:10] == "=0GDAqREMS"


def test_rot_13():
    c = Chepy(path).load_file()
    assert c.rot_13().output[:10] == "=0TQNdERZF"


def test_reverse():
    c = Chepy(path).load_file()
    assert c.reverse().output[0:10] == "E0SMERSADy"


def test_flag():
    c = Chepy(path).load_file()
    assert (
        c.reverse().rot_13().base_64_decode().base_32_decode().hexdump_to_str().output
        == "StormCTF{Spot3:DcEC6181F48e3B9D3dF77Dd827BF34e0}"
    )
