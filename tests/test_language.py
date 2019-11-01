from chepy import Chepy


def test_unicode_languages():
    assert len(Chepy("I am 합시다").unicode_languages("Hangul")) == 3


def test_find_emojis():
    assert len(Chepy("hello 😍 🇰🇷 🇺🇸").find_emojis()) == 3

def test_encode_utf_16_le():
    assert Chepy("안녕").encode_utf_16_le().to_hex().o.decode() == '48c555b1' 

def test_decode_utf_16_le():
    assert Chepy("48c555b1").hex_to_str().decode_utf_16_le().o == '안녕' 

def test_encode_utf_16_be():
    assert Chepy("안녕").encode_utf_16_be().to_hex().o.decode() == 'c548b155' 

def test_decode_utf_16_be():
    assert Chepy("c548b155").hex_to_str().decode_utf_16_be().o == '안녕' 

def test_encode_utf_7():
    assert Chepy("안녕").encode_utf_7().o.decode() == '+xUixVQ-' 

def test_decode_utf_7():
    assert Chepy("+xUixVQ-").decode_utf_7().o == '안녕' 

def test_encode_cp500():
    assert Chepy("hello").encode_cp500().to_hex().o.decode() == '8885939396' 

def test_decode_cp500():
    assert Chepy("8885939396").hex_to_str().decode_cp500().o == 'hello' 

def test_encode_cp037():
    assert Chepy("hello").encode_cp500().to_hex().o.decode() == '8885939396' 

def test_decode_cp037():
    assert Chepy("8885939396").hex_to_str().decode_cp500().o == 'hello' 