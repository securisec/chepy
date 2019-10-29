from pathlib import Path
from chepy import Chepy


def test_read_file():
    c = Chepy(str(Path().absolute() / "tests/encoding"), True)
    assert c.output[0:10] == "=0GDAqREMS"


def test_rot_13():
    c = Chepy(str(Path().absolute() / "tests/encoding"), True)
    assert c.rot_13().output[:10] == "=0TQNdERZF"


def test_reverse():
    c = Chepy(str(Path().absolute() / "tests/encoding"), True)
    assert c.reverse().output[0:10] == "E0SMERSADy"


def test_flag():
    c = Chepy(str(Path().absolute() / "tests/encoding"), True)
    assert (
        c.reverse()
        .rot_13()
        .base_64_decode()
        .base_32_decode()
        .string_from_hexdump()
        .output
        == "StormCTF{Spot3:DcEC6181F48e3B9D3dF77Dd827BF34e0}"
    )
