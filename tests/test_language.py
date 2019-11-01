from chepy import Chepy


def test_unicode_languages():
    assert len(Chepy("I am 합시다").unicode_languages("Hangul")) == 3


def test_find_emojis():
    assert len(Chepy("hello 😍 🇰🇷 🇺🇸").find_emojis()) == 3


def test_encode_utf_16_le():
    assert Chepy("안녕").encode_utf_16_le().to_hex().o.decode() == "48c555b1"


def test_decode_utf_16_le():
    assert Chepy("48c555b1").hex_to_str().decode_utf_16_le().o == "안녕"


def test_encode_utf_16_be():
    assert Chepy("안녕").encode_utf_16_be().to_hex().o.decode() == "c548b155"


def test_decode_utf_16_be():
    assert Chepy("c548b155").hex_to_str().decode_utf_16_be().o == "안녕"


def test_encode_utf_7():
    assert Chepy("안녕").encode_utf_7().o.decode() == "+xUixVQ-"


def test_decode_utf_7():
    assert Chepy("+xUixVQ-").decode_utf_7().o == "안녕"


def test_encode_cp500():
    assert Chepy("hello").encode_cp500().to_hex().o.decode() == "8885939396"


def test_decode_cp500():
    assert Chepy("8885939396").hex_to_str().decode_cp500().o == "hello"


def test_encode_cp037():
    assert Chepy("hello").encode_cp037().to_hex().o.decode() == "8885939396"


def test_decode_cp037():
    assert Chepy("8885939396").hex_to_str().decode_cp037().o == "hello"


def test_encode_cp874():
    assert Chepy("สวัสดี").encode_cp874().to_hex().o.decode() == "cac7d1cab4d5"


def test_decode_cp874():
    assert Chepy("cac7d1cab4d5").hex_to_str().decode_cp874().o == "สวัสดี"


def test_encode_cp932():
    assert Chepy("こんにちは").encode_cp932().to_hex().o.decode() == "82b182f182c982bf82cd"


def test_decode_cp932():
    assert Chepy("82b182f182c982bf82cd").hex_to_str().decode_cp932().o == "こんにちは"


def test_encode_gbk():
    assert Chepy("你好").encode_gbk().to_hex().o.decode() == "c4e3bac3"


def test_decode_gbk():
    assert Chepy("c4e3bac3").hex_to_str().decode_gbk().o == "你好"


def test_encode_gb2312():
    assert Chepy("你好").encode_gb2312().to_hex().o.decode() == "c4e3bac3"


def test_decode_gb2312():
    assert Chepy("c4e3bac3").hex_to_str().decode_gb2312().o == "你好"


def test_encode_cp949():
    assert Chepy("안녕").encode_cp949().to_hex().o.decode() == "bec8b3e7"


def test_decode_cp949():
    assert Chepy("bec8b3e7").hex_to_str().decode_cp949().o == "안녕"


def test_encode_cp950():
    assert Chepy("你好").encode_cp950().to_hex().o.decode() == "a741a66e"


def test_decode_cp950():
    assert Chepy("a741a66e").hex_to_str().decode_cp950().o == "你好"


def test_encode_cp1250():
    assert Chepy("Plzeň").encode_cp1250().to_hex().o.decode() == "506c7a65f2"


def test_decode_cp1250():
    assert Chepy("506c7a65f2").hex_to_str().decode_cp1250().o == "Plzeň"


def test_encode_cp1251():
    assert Chepy("Привет").encode_cp1251().to_hex().o.decode() == "cff0e8e2e5f2"


def test_decode_cp1251():
    assert Chepy("cff0e8e2e5f2").hex_to_str().decode_cp1251().o == "Привет"


def test_encode_cp1252():
    assert Chepy("garçon").encode_cp1252().to_hex().o.decode() == "676172e76f6e"


def test_decode_cp1252():
    assert Chepy("676172e76f6e").hex_to_str().decode_cp1252().o == "garçon"


def test_encode_cp1253():
    assert Chepy("δοκιμή").encode_cp1253().to_hex().o.decode() == "e4efeae9ecde"


def test_decode_cp1253():
    assert Chepy("e4efeae9ecde").hex_to_str().decode_cp1253().o == "δοκιμή"


def test_encode_cp1254():
    assert Chepy("Ölçek").encode_cp1254().to_hex().o.decode() == "d66ce7656b"


def test_decode_cp1254():
    assert Chepy("d66ce7656b").hex_to_str().decode_cp1254().o == "Ölçek"


def test_encode_cp1255():
    assert Chepy("מבחן").encode_cp1255().to_hex().o.decode() == "eee1e7ef"


def test_decode_cp1255():
    assert Chepy("eee1e7ef").hex_to_str().decode_cp1255().o == "מבחן"


def test_encode_cp1256():
    assert Chepy("اختبار").encode_cp1256().to_hex().o.decode() == "c7cecac8c7d1"


def test_decode_cp1256():
    assert Chepy("c7cecac8c7d1").hex_to_str().decode_cp1256().o == "اختبار"


def test_encode_cp1257():
    assert Chepy("pārbaude").encode_cp1257().to_hex().o.decode() == "70e2726261756465"


def test_decode_cp1257():
    assert Chepy("70e2726261756465").hex_to_str().decode_cp1257().o == "pārbaude"


def test_encode_cp1258():
    assert Chepy("Chào").encode_cp1258().to_hex().o.decode() == "4368e06f"


def test_decode_cp1258():
    assert Chepy("4368e06f").hex_to_str().decode_cp1258().o == "Chào"


def test_encode_iso8859_2():
    assert Chepy("Plzeň").encode_iso8859_2().to_hex().o.decode() == "506c7a65f2"


def test_decode_iso8859_2():
    assert Chepy("506c7a65f2").hex_to_str().decode_iso8859_2().o == "Plzeň"


def test_encode_iso8859_3():
    assert Chepy("garçon").encode_iso8859_3().to_hex().o.decode() == "676172e76f6e"


def test_decode_iso8859_3():
    assert Chepy("676172e76f6e").hex_to_str().decode_iso8859_3().o == "garçon"


def test_encode_iso8859_4():
    assert (
        Chepy("garçon").encode_iso8859_4().to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_4():
    assert Chepy("6761725c7865376f6e").hex_to_str().decode_iso8859_4().o == "gar\\xe7on"


def test_encode_iso8859_5():
    assert (
        Chepy("garçon").encode_iso8859_5().to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_5():
    assert Chepy("6761725c7865376f6e").hex_to_str().decode_iso8859_5().o == "gar\\xe7on"


def test_encode_iso8859_6():
    assert (
        Chepy("garçon").encode_iso8859_6().to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_6():
    assert Chepy("6761725c7865376f6e").hex_to_str().decode_iso8859_6().o == "gar\\xe7on"


def test_encode_iso8859_7():
    assert (
        Chepy("garçon").encode_iso8859_7().to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_7():
    assert Chepy("6761725c7865376f6e").hex_to_str().decode_iso8859_7().o == "gar\\xe7on"


def test_encode_iso8859_8():
    assert (
        Chepy("garçon").encode_iso8859_8().to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_8():
    assert Chepy("6761725c7865376f6e").hex_to_str().decode_iso8859_8().o == "gar\\xe7on"


def test_encode_iso8859_9():
    assert Chepy("garçon").encode_iso8859_9().to_hex().o.decode() == "676172e76f6e"


def test_decode_iso8859_9():
    assert Chepy("676172e76f6e").hex_to_str().decode_iso8859_9().o == "garçon"


def test_encode_iso8859_10():
    assert (
        Chepy("garçon").encode_iso8859_10().to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_10():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode_iso8859_10().o == "gar\\xe7on"
    )


def test_encode_iso8859_11():
    assert (
        Chepy("garçon").encode_iso8859_11().to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_11():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode_iso8859_11().o == "gar\\xe7on"
    )


def test_encode_iso8859_13():
    assert (
        Chepy("garçon").encode_iso8859_13().to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_13():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode_iso8859_13().o == "gar\\xe7on"
    )


def test_encode_iso8859_14():
    assert Chepy("garçon").encode_iso8859_14().to_hex().o.decode() == "676172e76f6e"


def test_decode_iso8859_14():
    assert Chepy("676172e76f6e").hex_to_str().decode_iso8859_14().o == "garçon"


def test_encode_iso8859_15():
    assert Chepy("garçon").encode_iso8859_15().to_hex().o.decode() == "676172e76f6e"


def test_decode_iso8859_15():
    assert Chepy("676172e76f6e").hex_to_str().decode_iso8859_15().o == "garçon"

