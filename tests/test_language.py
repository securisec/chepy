from chepy import Chepy


def test_unicode_languages():
    assert len(Chepy("I am 합시다").unicode_languages("Hangul")) == 3


def test_find_emojis():
    assert len(Chepy("hello 😍 🇰🇷 🇺🇸").find_emojis()) == 3

def test_encode_utf_16_be():
    assert Chepy("안녕").encode_utf_16_be().to_hex().o.decode() == 'c548b155' 