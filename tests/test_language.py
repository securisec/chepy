from chepy import Chepy


def test_search_perl_unicode_props():
    assert len(Chepy("I am 합시다").search_perl_unicode_props("Hangul").o) == 3


def test_find_emojis():
    assert len(Chepy("hello 😍 🇰🇷 🇺🇸").find_emojis().o) == 3


def test_encode_utf_16_le():
    assert Chepy("안녕").encode("utf_16_le").to_hex().o == b"48c555b1"


def test_decode_utf_16_le():
    assert Chepy("48c555b1").hex_to_str().decode("utf_16_le").o.decode() == "안녕"


def test_encode_utf_16_be():
    assert Chepy("안녕").encode("utf_16_be").to_hex().o == b"c548b155"


def test_decode_utf_16_be():
    assert Chepy("c548b155").hex_to_str().decode("utf_16_be").o.decode() == "안녕"


def test_encode_utf_7():
    assert Chepy("안녕").encode("utf_7").o == b"+xUixVQ-"


def test_decode_utf_7():
    assert Chepy("+xUixVQ-").decode("utf_7").o.decode() == "안녕"


def test_encode_cp500():
    assert Chepy("hello").encode("cp500").to_hex().o == b"8885939396"


def test_decode_cp500():
    assert Chepy("8885939396").hex_to_str().decode("cp500").o == b"hello"


def test_encode_cp037():
    assert Chepy("hello").encode("cp037").to_hex().o == b"8885939396"


def test_decode_cp037():
    assert Chepy("8885939396").hex_to_str().decode("cp037").o == b"hello"


def test_encode_cp874():
    assert Chepy("สวัสดี").encode("cp874").to_hex().o == b"cac7d1cab4d5"


def test_decode_cp874():
    assert Chepy("cac7d1cab4d5").hex_to_str().decode("cp874").o.decode() == "สวัสดี"


def test_encode_cp932():
    assert Chepy("こんにちは").encode("cp932").to_hex().o == b"82b182f182c982bf82cd"


def test_decode_cp932():
    assert (
        Chepy("82b182f182c982bf82cd").hex_to_str().decode("cp932").o.decode() == "こんにちは"
    )


def test_encode_gbk():
    assert Chepy("你好").encode("gbk").to_hex().o == b"c4e3bac3"


def test_decode_gbk():
    assert Chepy("c4e3bac3").hex_to_str().decode("gbk").o.decode() == "你好"


def test_encode_gb2312():
    assert Chepy("你好").encode("gb2312").to_hex().o == b"c4e3bac3"


def test_decode_gb2312():
    assert Chepy("c4e3bac3").hex_to_str().decode("gb2312").o.decode() == "你好"


def test_encode_cp949():
    assert Chepy("안녕").encode("cp949").to_hex().o.decode() == "bec8b3e7"


def test_decode_cp949():
    assert Chepy("bec8b3e7").hex_to_str().decode("cp949").o.decode() == "안녕"


def test_encode_cp950():
    assert Chepy("你好").encode("cp950").to_hex().o.decode() == "a741a66e"


def test_decode_cp950():
    assert Chepy("a741a66e").hex_to_str().decode("cp950").o.decode() == "你好"


def test_encode_cp1250():
    assert Chepy("Plzeň").encode("cp1250").to_hex().o.decode() == "506c7a65f2"


def test_decode_cp1250():
    assert Chepy("506c7a65f2").hex_to_str().decode("cp1250").o.decode() == "Plzeň"


def test_encode_cp1251():
    assert Chepy("Привет").encode("cp1251").to_hex().o.decode() == "cff0e8e2e5f2"


def test_decode_cp1251():
    assert Chepy("cff0e8e2e5f2").hex_to_str().decode("cp1251").o.decode() == "Привет"


def test_encode_cp1252():
    assert Chepy("garçon").encode("cp1252").to_hex().o.decode() == "676172e76f6e"


def test_decode_cp1252():
    assert Chepy("676172e76f6e").hex_to_str().decode("cp1252").o.decode() == "garçon"


def test_encode_cp1253():
    assert Chepy("δοκιμή").encode("cp1253").to_hex().o.decode() == "e4efeae9ecde"


def test_decode_cp1253():
    assert Chepy("e4efeae9ecde").hex_to_str().decode("cp1253").o.decode() == "δοκιμή"


def test_encode_cp1254():
    assert Chepy("Ölçek").encode("cp1254").to_hex().o.decode() == "d66ce7656b"


def test_decode_cp1254():
    assert Chepy("d66ce7656b").hex_to_str().decode("cp1254").o.decode() == "Ölçek"


def test_encode_cp1255():
    assert Chepy("מבחן").encode("cp1255").to_hex().o.decode() == "eee1e7ef"


def test_decode_cp1255():
    assert Chepy("eee1e7ef").hex_to_str().decode("cp1255").o.decode() == "מבחן"


def test_encode_cp1256():
    assert Chepy("اختبار").encode("cp1256").to_hex().o.decode() == "c7cecac8c7d1"


def test_decode_cp1256():
    assert Chepy("c7cecac8c7d1").hex_to_str().decode("cp1256").o.decode() == "اختبار"


def test_encode_cp1257():
    assert Chepy("pārbaude").encode("cp1257").to_hex().o.decode() == "70e2726261756465"


def test_decode_cp1257():
    assert (
        Chepy("70e2726261756465").hex_to_str().decode("cp1257").o.decode() == "pārbaude"
    )


def test_encode_cp1258():
    assert (
        Chepy("tạm biệt").encode("cp1258").to_hex().o.decode()
        == "745c75316561316d2062695c753165633774"
    )


def test_decode_cp1258():
    assert (
        Chepy("745c75316561316d2062695c753165633774")
        .hex_to_str()
        .decode("cp1258")
        .unicode_to_str()
        .o.decode()
        == "tạm biệt"
    )


def test_str_to_unice():
    assert Chepy("籯").str_to_unicode().o == b"\\u7c6f"


def test_encode_iso8859_2():
    assert Chepy("Plzeň").encode("iso8859_2").to_hex().o.decode() == "506c7a65f2"


def test_decode_iso8859_2():
    assert Chepy("506c7a65f2").hex_to_str().decode("iso8859_2").o.decode() == "Plzeň"


def test_encode_iso8859_3():
    assert Chepy("garçon").encode("iso8859_3").to_hex().o.decode() == "676172e76f6e"


def test_decode_iso8859_3():
    assert Chepy("676172e76f6e").hex_to_str().decode("iso8859_3").o.decode() == "garçon"


def test_encode_iso8859_4():
    assert (
        Chepy("garçon").encode("iso8859_4").to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_4():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode("iso8859_4").o == b"gar\\xe7on"
    )


def test_encode_iso8859_5():
    assert (
        Chepy("garçon").encode("iso8859_5").to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_5():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode("iso8859_5").o == b"gar\\xe7on"
    )


def test_encode_iso8859_6():
    assert (
        Chepy("garçon").encode("iso8859_6").to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_6():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode("iso8859_6").o == b"gar\\xe7on"
    )


def test_encode_iso8859_7():
    assert (
        Chepy("garçon").encode("iso8859_7").to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_7():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode("iso8859_7").o == b"gar\\xe7on"
    )


def test_encode_iso8859_8():
    assert (
        Chepy("garçon").encode("iso8859_8").to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_8():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode("iso8859_8").o == b"gar\\xe7on"
    )


def test_encode_iso8859_9():
    assert Chepy("garçon").encode("iso8859_9").to_hex().o.decode() == "676172e76f6e"


def test_decode_iso8859_9():
    assert Chepy("676172e76f6e").hex_to_str().decode("iso8859_9").o.decode() == "garçon"


def test_encode_iso8859_10():
    assert (
        Chepy("garçon").encode("iso8859_10").to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_10():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode("iso8859_10").o == b"gar\\xe7on"
    )


def test_encode_iso8859_11():
    assert (
        Chepy("garçon").encode("iso8859_11").to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_11():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode("iso8859_11").o == b"gar\\xe7on"
    )


def test_encode_iso8859_13():
    assert (
        Chepy("garçon").encode("iso8859_13").to_hex().o.decode() == "6761725c7865376f6e"
    )


def test_decode_iso8859_13():
    assert (
        Chepy("6761725c7865376f6e").hex_to_str().decode("iso8859_13").o == b"gar\\xe7on"
    )


def test_encode_iso8859_14():
    assert Chepy("garçon").encode("iso8859_14").to_hex().o.decode() == "676172e76f6e"


def test_decode_iso8859_14():
    assert (
        Chepy("676172e76f6e").hex_to_str().decode("iso8859_14").o.decode() == "garçon"
    )


def test_encode_iso8859_15():
    assert Chepy("garçon").encode("iso8859_15").to_hex().o.decode() == "676172e76f6e"


def test_decode_iso8859_15():
    assert (
        Chepy("676172e76f6e").hex_to_str().decode("iso8859_15").o.decode() == "garçon"
    )


def test_remove_diacritics():
    assert Chepy("François Chào").remove_diacritics().o == b"Francois Chao"


def test_us_ascii_7_bit():
    assert (
        Chepy("걳걵걮걻걢갴걳갳걟갱갲갸걟갱갵걟걢갱건걟걲갳걭갴거거갱걮걧걽").encode_us_ascii_7_bit().o
        == b"sun{b4s3_128_15_b1t_r3m4pp1ng}"
    )
