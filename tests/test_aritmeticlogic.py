from chepy import Chepy


def test_bit_shift_right():
    assert Chepy("hello").str_bit_shift_right(2).to_hex().o == b"1a191b1b1b"

