from chepy import Chepy


def test_bit_shift_right():
    assert Chepy("hello").str_bit_shift_right(2).to_hex().o == b"1a191b1b1b"


def test_add():
    assert Chepy("0x40").add(1).o == 65


def test_multiply():
    assert Chepy("0x40").multiply(2).o == 128


def test_divide():
    assert Chepy("0x40").divide(2).o == 32


def test_power():
    assert Chepy("0x02").power(2).o == 4


def test_sum():
    assert Chepy(["0x40", 10]).sum().o == 74


def test_mean():
    assert Chepy(["0x40", 10]).mean().o == 37


def test_median():
    assert Chepy(["0x40", 10, 20]).median().o == 20


def test_subtract():
    assert Chepy(["0x02", "0x04"]).loop_list("subtract", {"n": 1}).o == [1, 3]


def test_int_to_base():
    assert Chepy("067165").int_to_base(8).o == 28277
