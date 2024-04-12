from chepy import Chepy


def test_add():
    assert Chepy("40").add(1).to_int().o == 51
    assert Chepy("hello").add("ff").o == b"gdkkn"
    assert Chepy(9).add("01").o == b":"


def test_multiply():
    assert Chepy("0x40").multiply(2).o == 128


def test_divide():
    assert Chepy("0x40").divide(2).o == 32


def test_divide_float():
    assert Chepy("179").divide(178).to_hex().o == b"17b8803f"


def test_power():
    assert Chepy("0x02").power(2).o == 4


def test_sum():
    assert Chepy(["0x40", 10]).sum().o == 74


def test_mean():
    assert Chepy(["0x40", 10]).mean().o == 37


def test_median():
    assert Chepy(["0x40", 10, 20]).median().o == 20


def test_sub():
    assert Chepy("40").sub(1).o == b"3/"
    assert Chepy("hello").sub("10").o == b"XU\\\\_"
    assert Chepy("hello").sub(10).o == b"^[bbe"
    # assert Chepy(9).add('01').o == b':'


def test_subtract():
    assert Chepy("10 9 x").subtract().o == 1


def test_addition():
    assert Chepy("10 9 x").addition().o == 19


def test_int_to_base():
    assert Chepy("067165").int_to_base(8).o == 28277


def test_bitwise_operations():
    assert Chepy("A").bit_shift_right(3).o == b"\x08"
    assert Chepy(b"414243").bit_shift_right().o == b"\x1a\x18\x1a\x19\x1a\x19"
    assert Chepy("A").bit_shift_left().o == b"\x82"
    assert Chepy("414243").from_hex().bit_shift_left(7).o == b"\x80\x00\x80"
