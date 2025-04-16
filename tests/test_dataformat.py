from chepy import Chepy


def test_eval():
    assert Chepy("1").eval_state().o == 1


def test_base16_encode():
    assert Chepy("test").to_base16().o == b"74657374"


def test_base16_decode():
    assert Chepy("74657374").from_base16().o == b"test"


def test_list_to_bytes():
    assert Chepy([116, 101, 115, 116]).list_to_bytes().o == b"test"
    assert Chepy([116, 101, 115, 116]).list_to_bytes(True).o == b"test"


def test_dict_to_json():
    assert (
        Chepy({"some": "data", "a": ["list", 1, True]}).dict_to_json().o
        == b'{"some": "data", "a": ["list", 1, true]}'
    )


def test_dict_get_items():
    o = Chepy({"a": 1, "b": 2}).dict_get_items("a", "b", "c").o
    assert o[0] == 1 and o[1] == 2 and len(o) == 2
    o = Chepy({"a": 1, "b": 2}).dict_get_items().o
    assert len(o) == 2


def test_json_to_dict():
    assert Chepy('{"some": "data", "a": ["list", 1, true]}').json_to_dict().o == {
        "some": "data",
        "a": ["list", 1, True],
    }


# def test_yaml_to_json():
#     data = """# An employee record
# name: Martin D'vloper
# job: Developer
# skill: Elite
# employed: True
# foods:
# 	- Apple
# 	- Orange
# 	- Strawberry
# 	- Mango
# languages:
# 	perl: Elite
# 	python: Elite
# 	pascal: Lame
# education: |
# 	4 GCSEs
# 	3 A-Levels
# 	BSc in the Internet of Things
# """
#     assert (
#         Chepy(data).yaml_to_json().o != ""
#         # == '{"name":"Martin D\'vloper","job":"Developer","skill":"Elite","employed":true,"foods":["Apple","Orange","Strawberry","Mango"],"languages":{"perl":"Elite","python":"Elite","pascal":"Lame"},"education":"4 GCSEs\\n3 A-Levels\\nBSc in the Internet of Things\\n"}'
#     )


def test_json_to_yaml():
    data = '{"name": "Martin D\'vloper", "job": "Developer", "skill": "Elite", "employed": true, "foods": ["Apple", "Orange", "Strawberry", "Mango"], "languages": {"perl": "Elite", "python": "Elite", "pascal": "Lame"}, "education": "4 GCSEs\\n3 A-Levels\\nBSc in the Internet of Things\\n"}'
    assert (
        Chepy(data).json_to_yaml().o.decode()
        == """name: Martin D'vloper
job: Developer
skill: Elite
employed: true
foods:
  - Apple
  - Orange
  - Strawberry
  - Mango
languages:
  perl: Elite
  python: Elite
  pascal: Lame
education: '4 GCSEs

  3 A-Levels

  BSc in the Internet of Things

  '
"""
    )


def test_from_base58():
    assert Chepy("2UDrs31qcWSPi").from_base58().out.decode() == "some data"


def test_to_base85():
    assert Chepy("some data").to_base85().out.decode() == "F)Po,+Cno&@/"


def test_from_base85():
    assert Chepy("F)Po,+Cno&@/").from_base85().out.decode() == "some data"


def test_base32():
    assert Chepy("some data").to_base32().out.decode() == "ONXW2ZJAMRQXIYI="
    assert (
        Chepy("""MFWWC5DFOVZHGQ2UIZ5XA2LDGBPXONBVNY3V6ZZQGBSF63RQOVTWQXZVGBPWSXZXGAYGWX3TN5WT
GX3DOIZTI5BROYZV63BRMIZXE5BRGM2V6YLEMU4DQMRQMV6Q====""")
        .from_base32()
        .o
        == b"amateursCTF{pic0_w45n7_g00d_n0ugh_50_i_700k_som3_cr34t1v3_l1b3rt135_ade8820e}"
    )


def test_to_base64():
    assert Chepy("some data").to_base64().out.decode() == "c29tZSBkYXRh"
    assert Chepy("test").to_base64(alphabet="url_safe").o == b"dGVzdA"
    assert (
        Chepy("some random? data").to_base64(alphabet="itoa64").o
        == b"QqxhNG/mMKtYPqoz64FVR42="
    )
    data = "some random data"
    assert Chepy(data).to_base64("rot13").o == b"p29gMFOlLJ5xo20tMTS0LD=="
    assert Chepy(data).to_base64("radix_64").o == b"SszjPI1oOMvaRsqWP65qOG=="
    assert Chepy(data).to_base64("xml").o == b"c29tZSByYW5kb20gZGF0YQ"
    assert Chepy(data).to_base64("xxencoding").o == b"QqxhNG-mMKtYPqoUN43oME"
    assert Chepy(data).to_base64("filename_safe").o == b"c29tZSByYW5kb20gZGF0YQ=="
    assert Chepy(data).to_base64("z64").o == b"sSZJpi1OomVArSQwp65Qog=="
    assert Chepy(data).to_base64("unix_crypt").o == b"QqxhNG/mMKtYPqoUN43oME"


def test_from_base64():
    assert Chepy("c29tZSByYW5kb20/IGRhdGE").from_base64().o == b"some random? data"
    assert (
        Chepy("QqxhNG/mMKtYPqoz64FVR42=").from_base64(alphabet="itoa64").o
        == b"some random? data"
    )
    assert Chepy("dGVzdA").from_base64(alphabet="url_safe").o == b"test"
    assert (
        Chepy("""YW1hdGV1cnNDVEZ7cGljMF93NDVuN19nMDBkX24wdWdoXzUwX2lfNzAwa19zb20zX2NyMzR0MXYz
X2wxYjNydDEzNV9hZGU4ODIwZX0=""")
        .from_base64()
        .o
        == b"amateursCTF{pic0_w45n7_g00d_n0ugh_50_i_700k_som3_cr34t1v3_l1b3rt135_ade8820e}"
    )
    assert Chepy("q6lIr6YwtSZOr6g=").from_base64("z64").o == b"hello world"
    assert Chepy("nTIfoT8tq29loTD=").from_base64("rot13").o == b"hello world"
    data = b"some random data"
    assert Chepy("c29tZSByYW5kb20gZGF0YQ").from_base64("xml").o == data
    assert Chepy("QqxhNG-mMKtYPqoUN43oME").from_base64("xxencoding").o == data
    assert Chepy("c29tZSByYW5kb20gZGF0YQ==").from_base64("filename_safe").o == data
    assert Chepy("sSZJpi1OomVArSQwp65Qog==").from_base64("z64").o == data
    assert Chepy("QqxhNG/mMKtYPqoUN43oME").from_base64("unix_crypt").o == data


def test_decode_bytes():
    assert (
        Chepy(
            b'{"flag":{" b":"MjQ3Q1RGe2RhODA3OTVmOGE1Y2FiMmUwMzdkNzM4NTgwN2I5YTkxfQ=="}}\x17\x8by\x90[\xc38E"\xf2\xb8\xfe\xf0\x95\xcc\x16.7\xabc\x92\xc0\x92'
        )
        .decode_bytes()
        .extract_base64()
        .from_base64()
        .o
        == b"247CTF{da80795f8a5cab2e037d7385807b9a91}"
    )


def test_to_base58():
    assert Chepy("some data").to_base58().out.decode() == "2UDrs31qcWSPi"


def test_to_hex():
    assert Chepy("AAA").to_hex().out.decode() == "414141"
    assert Chepy("AAA").to_hex(delimiter=" ").out.decode() == "41 41 41"


def test_from_hex():
    assert Chepy("414141").from_hex().out.decode() == "AAA"
    assert (
        Chepy("41;41;41").from_hex(delimiter=";", join_by="%").out.decode() == "A%A%A"
    )
    assert (
        Chepy("%41;41;41").from_hex(delimiter=";", join_by="%").out.decode() == "A%A%A"
    )
    assert (
        Chepy("%41;0x41;%41").from_hex(delimiter=";", join_by="%").out.decode()
        == "A%A%A"
    )


def test_hex_to_int():
    assert Chepy("0x123").hex_to_int().out == 291
    assert Chepy("123").hex_to_int().out == 291


def test_hex_to_bytes():
    assert Chepy("ab00").hex_to_bytes().o == b"\xab\x00"


def test_int_to_hex():
    assert Chepy(101).int_to_hex().o == b"65"
    assert Chepy(-0x2152411021524111).int_to_hex().o == b"deadbeefdeadbeef"


def test_hex_to_str():
    assert Chepy("4100").hex_to_str().o == b"A\x00"
    assert Chepy("4100").hex_to_str(ignore=True).o == b"A\x00"


def test_to_url_encoding():
    assert (
        Chepy("https://google.com/?lol=some data&a=1").to_url_encoding(safe="/:").o
        == b"https://google.com/%3Flol%3Dsome+data%26a%3D1"
    )
    assert Chepy("a").to_url_encoding(all_chars=True).to_url_encoding().o == b"%2561"


def test_from_url_encoding():
    assert (
        Chepy("https://google.com/%3Flol%3Dsome+data%26a%3D1").from_url_encoding().o
        == b"https://google.com/?lol=some data&a=1"
    )


def test_str_list_to_list():
    assert Chepy("[1,2,'lol', true]").str_list_to_list().o == [1, 2, "lol", True]


def test_list_to_str():
    assert Chepy(["a", "b", "c"]).list_to_str(",").o == b"a,b,c"
    assert Chepy([1, 2, 3]).list_to_str((".")).o == b"1.2.3"
    assert Chepy([b"a", b"b"]).list_to_str(b".").o == b"a.b"


def test_join():
    assert Chepy(["a", "b", "c", True]).join(":").o == b"a:b:c:True"


def test_to_int():
    assert Chepy("1").to_int().o == 1
    assert Chepy("AQAB").from_base64().to_int().o == 65537


def test_normalize_hex():
    assert Chepy("41:42:CE").normalize_hex().o == b"4142CE"
    assert Chepy("0x410x420xce").normalize_hex().o == b"4142ce"
    assert (
        Chepy("tests/files/hello").load_file().normalize_hex(True).o[0:6] == b"cffaed"
    )


def test_bytearray_to_str():
    assert Chepy(bytearray("lolol", "utf")).bytearray_to_str().o == b"lolol"


def test_get_by_index():
    assert Chepy([1, "a", True]).get_by_index(2).state


def test_to_bytes():
    assert Chepy({"some": "val", "kl": 1}).to_bytes().o == b"{'some': 'val', 'kl': 1}"


def test_from_bytes():
    assert (
        Chepy(b'{"some": "val", "kl": 1}').from_bytes().o == b'{"some": "val", "kl": 1}'
    )


def test_to_list():
    assert Chepy("abc").to_list().o == ["a", "b", "c"]
    assert Chepy(bytearray(b"abc")).to_list().o == [97, 98, 99]
    assert Chepy(b"abc").to_list().o == [97, 98, 99]


def test_str_to_dict():
    assert Chepy(b"{'some': 'dict'}").str_to_dict().o == {"some": "dict"}


def test_int_to_str():
    assert Chepy(41).int_to_str().o == b"41"


def test_to_charcode():
    assert Chepy("aㅎ").to_charcode().o == b"97 12622"


def test_from_charcode():
    assert Chepy("314e-61-20-41").from_charcode(base=16).o == b"\xe3\x85\x8ea A"
    assert Chepy("314e 61 20 41").from_charcode(base=16).o == b"\xe3\x85\x8ea A"
    assert Chepy("97 98 99").from_charcode().o == b"abc"


def test_to_decimal():
    assert Chepy("aㅎ").to_decimal().o == b"97 12622"


def test_from_decimal():
    assert Chepy(12622).from_decimal().o == b"\xe3\x85\x8e"
    assert Chepy("97-98-99").from_decimal().o == b"abc"


def test_to_binary():
    assert Chepy("abc").to_binary().o == b"01100001 01100010 01100011"
    assert Chepy("8081").from_hex().to_binary().o == b"10000000 10000001"


def test_from_binary():
    assert Chepy("011001000110 000101110100 0110000 1").from_binary().o == b"data"
    assert Chepy("01100100 01100001 01110100 01100001").from_binary().o == b"data"
    assert (
        Chepy("0001100100 0001100001 0001110100 0001100001")
        .from_binary(byte_length=10)
        .o
        == b"data"
    )
    assert (
        Chepy("000001100100 000001100001 000001110100 000001100001")
        .from_binary(byte_length=12)
        .o
        == b"data"
    )
    assert (
        Chepy(
            "00000000000001110011 00000000000001101111 00000000000001101101 00000000000001100101 00000000000000100000 00000000000001100100 00000000000001100001 00000000000001110100 00000000000001100001"
        )
        .from_binary(byte_length=20)
        .o
        == b"some data"
    )


def test_to_octal():
    assert Chepy("abㅎ").to_octal().o == b"141 142 30516"


def test_from_octral():
    assert Chepy("141 142 30516").from_octal().o == b"ab\xe3\x85\x8e"


def test_html_encode():
    assert (
        Chepy('https://google.com&a="lol"').to_html_entity(format="named").o
        == b"https&colon;&sol;&sol;google&period;com&amp;a&equals;&quot;lol&quot;"
    )
    assert (
        Chepy('https://google.com&a="lol"').to_html_entity(format="numeric").o
        == b"https&#58;&#47;&#47;google&#46;com&#38;a&#61;&#34;lol&#34;"
    )
    assert (
        Chepy('https://google.com&a="lol"').to_html_entity(format="hex").o
        == b"https&#x3a;&#x2f;&#x2f;google&#x2e;com&#x26;a&#x3d;&#x22;lol&#x22;"
    )
    assert (
        Chepy('https://google.com&a="lol"')
        .to_html_entity(format="hex", all_chars=True)
        .o
        == b"&#x68;&#x74;&#x74;&#x70;&#x73;&#x3a;&#x2f;&#x2f;&#x67;&#x6f;&#x6f;&#x67;&#x6c;&#x65;&#x2e;&#x63;&#x6f;&#x6d;&#x26;&#x61;&#x3d;&#x22;&#x6c;&#x6f;&#x6c;&#x22;"
    )


def test_html_decode():
    assert (
        Chepy(
            "&#x68;&#x74;&#x74;&#x70;&#x73;&#x3a;&#x2f;&#x2f;&#x67;&#x6f;&#x6f;&#x67;&#x6c;&#x65;&#x2e;&#x63;&#x6f;&#x6d;&#x26;&#x61;&#x3d;&#x22;&#x6c;&#x6f;&#x6c;&#x22;"
        )
        .from_html_entity()
        .o
        == b'https://google.com&a="lol"'
    )


def test_from_punycode():
    assert Chepy(b"mnchen-3ya").from_punycode().o == b"m\xc3\xbcnchen"


def test_to_punycode():
    assert Chepy("münchen").to_punycode().o == b"mnchen-3ya"


def test_encode_bruteforce():
    assert (
        Chepy("münchen한").encode_bruteforce().get_by_key("ascii").o
        == b"m\\xfcnchen\\ud55c"
    )


def test_decode_bruteforce():
    assert (
        Chepy("m\xfcnchen\ud55c").decode_bruteforce().get_by_key("utf_8").o
        == b"m\xc3\xbcnchen\xed\x95\x9c"
    )


def test_to_braille():
    assert Chepy("secret message").to_braille().o.decode() == "⠎⠑⠉⠗⠑⠞⠀⠍⠑⠎⠎⠁⠛⠑"


def test_from_braille():
    assert Chepy("⠎⠑⠉⠗⠑⠞⠀⠍⠑⠎⠎⠁⠛⠑").from_braille().o == b"secret message"


def test_trim():
    assert Chepy("\nlol ").trim().o == b"lol"


def test_to_hexdump():
    assert Chepy("some").to_hexdump().o.split() == [
        b"00000000:",
        b"73",
        b"6F",
        b"6D",
        b"65",
        b"some",
    ]


def test_from_hexdump():
    assert Chepy("some").to_hexdump().from_hexdump().o == b"some"


def test_nato_convert():
    assert Chepy("abc:1").to_nato().o == b"Alpha Bravo Charlie : 1"
    assert (
        Chepy("Lima Alpha Kilo Echo Mike India Charlie Hotel India Golf Alpha November")
        .from_nato()
        .o
        == b"LAKEMICHIGAN"
    )
    assert (
        Chepy("Lima-Alpha-Kilo-Echo-Mike-India-Charlie-Hotel-India-Golf-Alpha-November")
        .from_nato()
        .o
        == b"LAKEMICHIGAN"
    )
    assert (
        Chepy(
            "Whiskey Hotel Four Tango Dash Alpha Romeo Three Dash Yankee Oscar Uniform Dash Sierra One November Kilo India November Golf Dash Four Bravo Zero Uniform Seven"
        )
        .from_nato()
        .o
        == b"WH4T-AR3-YOU-S1NKING-4B0U7"
    )


def test_swap_values():
    assert Chepy("abcd").swap_values("0", "3").o == b"dbca"
    assert Chepy("abcd").swap_values([0, 1], [3, 2]).o == b"dcba"
    assert Chepy([1, 2, 3]).swap_values("0", "2").o == [3, 2, 1]


def test_swap_strings():
    assert Chepy("oY u").swap_strings(2).o == b"You "


def test_to_string():
    assert Chepy(1).to_string().o == b"1"


def test_stringify():
    assert Chepy("aa").stringify().o == b'"aa"'
    assert Chepy(123).stringify().o == b"123"
    # assert Chepy("\xaa").stringify().o == '"\\u00aa"'
    assert Chepy(True).stringify().o == b"true"
    assert Chepy({"a": 1}).stringify(False).o == b'{"a": 1}'


def test_select():
    assert Chepy("abcd").select(0, 2).o == b"ab"
    assert Chepy("abcd").select(2).o == b"cd"
    assert Chepy("abcd").select("(b|c)").o == b"bcd"


def test_length():
    assert Chepy("abcd").length().o == 4


def test_leetcode():
    assert len(Chepy("ab@ cd").to_leetcode(replace_space="_").o) == 6


def test_substitute():
    assert (
        Chepy("synt{q41q8pq98s00o204r9800998rps8427r}")
        .substitute(
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        )
        .o
        == b"flag{d41d8cd98f00b204e9800998ecf8427e}"
    )


def test_remove_nonprintable():
    assert Chepy(b"aa").remove_nonprintable().o == b"aa"
    assert (
        Chepy(
            "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
        )
        .remove_nonprintable()
        .o
        == b""
    )
    assert Chepy("41ae42").from_hex().remove_nonprintable(replace_with=" ").o == b"A B"
    assert Chepy("41ae42").from_hex().remove_nonprintable(replace_with=b" ").o == b"A B"


def test_base91():
    data = b"flag{some_flag}"
    out = b"@iH<,{_{W$OsuxXi%]D"
    assert Chepy(data).to_base91().o == out
    assert Chepy(out).from_base91().o == data


def test_swap_endianness():
    assert Chepy("4142").from_hex().swap_endianness().o == b"\x00\x00BA"
    assert Chepy("4142").from_hex().swap_endianness(pad_incomplete=False).o == b"BA"


def test_bruteforce_base_xx():
    assert Chepy("dGVzdA==").bruteforce_from_base_xx().o["base64"] == b"test"


def test_long_to_bytes():
    assert (
        Chepy(
            "11515195063862318899931685488813747395775516287289682636499965282714637259206269"
        )
        .long_to_bytes()
        .o
        == b"crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}"
    )


def test_bytes_to_long():
    assert (
        Chepy("crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}").bytes_to_long().o
        == 11515195063862318899931685488813747395775516287289682636499965282714637259206269
    )


def test_concat():
    assert Chepy("lol").concat(b"data").o == b"loldata"
    assert Chepy(["a"]).concat(b"data").o == b"['a']data"


def test_to_wingdings():
    assert (
        Chepy("f︎l︎a︎g︎{︎e︎0︎7︎9︎1︎c︎e︎6︎8︎f︎7︎1︎8︎1︎8︎8︎c︎0︎3︎7︎8︎b︎1︎c︎0︎a︎3︎b︎d︎c︎9︎e︎}︎").to_wingdings().o.decode()
        == "♐︎●︎♋︎♑︎❀︎♏︎📁︎🖮︎🖲︎📂︎♍︎♏︎⌛︎🖰︎♐︎🖮︎📂︎🖰︎📂︎🖰︎🖰︎♍︎📁︎🗏︎🖮︎🖰︎♌︎📂︎♍︎📁︎♋︎🗏︎♌︎♎︎♍︎🖲︎♏︎❝︎"
    )


def test_from_windings():
    assert (
        Chepy("♐︎●︎♋︎♑︎❀︎♏︎📁︎🖮︎🖲︎📂︎♍︎♏︎⌛︎🖰︎♐︎🖮︎📂︎🖰︎📂︎🖰︎🖰︎♍︎📁︎🗏︎🖮︎🖰︎♌︎📂︎♍︎📁︎♋︎🗏︎♌︎♎︎♍︎🖲︎♏︎❝︎")
        .from_wingdings()
        .o.decode()
        == "f︎l︎a︎g︎{︎e︎0︎7︎9︎1︎c︎e︎6︎8︎f︎7︎1︎8︎1︎8︎8︎c︎0︎3︎7︎8︎b︎1︎c︎0︎a︎3︎b︎d︎c︎9︎e︎}︎"
    )


def test_to_base36():
    assert (
        Chepy("BDSEC{_tW1n_H3X_c1Ph3r_}").to_base36().o
        == b"19119108 1394555 22173 728462295"
    )
    assert (
        Chepy("BDSEC{_tW1n_H3X_c1Ph3r_}").to_base36(":").o
        == b"19119108:1394555:22173:728462295"
    )


def test_from_base36():
    assert (
        Chepy(b"19119108 1394555 22173 728462295").from_base36().o
        == b"BDSEC tW1n H3X c1Ph3r".lower()
    )
    assert (
        Chepy(b"19119108:1394555:22173:728462295")
        .from_base36(delimiter=":", join_by=" ")
        .o
        == b"BDSEC tW1n H3X c1Ph3r".lower()
    )


def test_to_twin_hex():
    assert (
        Chepy("BDSEC{_tW1n_H3X_c1Ph3r_}").to_twin_hex().to_twin_hex().o
        == b"1e25v768h1e66dw61v1hv1kl6aa1ei1pw1pv1ju1kj5ps1bb6lw624"
    )


def test_from_twin_hex():
    assert (
        Chepy("1e25v768h1e66dw61v1hv1kl6aa1ei1pw1pv1ju1kj5ps1bb6lw624")
        .from_twin_hex()
        .from_twin_hex()
        .o
        == b"BDSEC{_tW1n_H3X_c1Ph3r_}"
    )


def test_pickle():
    out = Chepy("hello").to_pickle().o
    assert out == b"\x80\x04\x95\t\x00\x00\x00\x00\x00\x00\x00\x8c\x05hello\x94."
    assert Chepy(out).from_pickle(True).o == b"hello"
    assert Chepy(out).from_pickle().o == out


def test_bacon():
    out = Chepy("hello").to_bacon().o
    assert out == b"AABBB AABAA ABABB ABABB ABBBA"
    assert Chepy(out).from_bacon().o == b"HELLO"
    assert Chepy("hello").to_bacon(A="0", B="1").from_bacon(A="0", B="1").o == b"HELLO"


def test_upside_down():
    assert Chepy("hello").to_upside_down().from_upside_down().o == b"hello"
    assert Chepy("hello").to_upside_down(True).from_upside_down(True).o == b"hello"


def test_messagepack():
    assert Chepy("hello").to_messagepack().from_messagepack().o == b"hello"
    assert Chepy("hello").to_messagepack().from_messagepack().o == b"hello"
    assert Chepy(["hello"]).to_messagepack().from_messagepack().o == ["hello"]
    assert Chepy({"a": "hello"}).to_messagepack().from_messagepack().o == {"a": "hello"}


def test_unicode_escape():
    data = "MMMMM‌‍aaaaaaa‌‍ssss‌‌oooooonnnnnCCC‌‌CCCC"
    assert (
        Chepy(data).unicode_escape(padding=4, uppercase_hex=True).o
        == b"MMMMM\u0000200C\u0000200Daaaaaaa\u0000200C\u0000200Dssss\u0000200C\u0000200CoooooonnnnnCCC\u0000200C\u0000200CCCCC"
    )
    assert (
        Chepy(data).unicode_escape().o
        == b"MMMMM\u200c\u200daaaaaaa\u200c\u200dssss\u200c\u200coooooonnnnnCCC\u200c\u200cCCCC"
    )


def test_to_base():
    assert Chepy(0).to_base().o == b"0"
    assert Chepy(15295865526991442899).to_base(16).o == b"d445d4a7e477d3d3"


def test_from_base():
    assert Chepy("d445d4a7e477d3d3").from_base(16).o == 15295865526991442899


def test_rotate_right():
    assert Chepy("d445d4a7e477d3d3").from_hex().rotate_right(radix=4).o == b"MTMzNw=="
    assert (
        Chepy("d445d4a7e477d3d3").from_hex().rotate_right(radix=4, carry=True).o
        == b"=D]J~G}="
    )


def test_rotate_left():
    assert Chepy("d445d4a7e477d3d3").from_hex().rotate_left(radix=4).o == b"MTMzNw=="
    assert (
        Chepy("d445d4a7e477d3d3").from_hex().rotate_left(radix=4, carry=True).o
        == b"D]J~G}=="
    )


def test_base62():
    assert (
        Chepy(b"hello !!123!! world\xcc").to_base62().o
        == b"EtWxGEdLPmwchEzFHWNyyyI3p1w"
    )
    assert Chepy("3bfP0XZgTym6SsUKeZS5Z6qoKa").from_base62().o == b"hello !!123!! world"


def test_cut():
    assert Chepy("abcd").cut(1, 2).o == b"b"
    assert Chepy("abcd").cut(1, 3).o == b"bc"
    assert Chepy({"a": 1}).cut(1, 3).o == b"'a"
    assert Chepy({"a": None}).cut(6, 9).o == b"Non"


def test_flatten():
    assert Chepy(["a", 1, True]).flatten().o == ["a", 1, True]
    assert Chepy([["a"], [1], [True]]).flatten().o == ["a", 1, True]


def test_utf21():
    flag = [
        0,
        2,
        168,
        0,
        17,
        0,
        0,
        134,
        0,
        5,
        64,
        0,
        35,
        0,
        1,
        236,
        0,
        6,
        224,
        0,
        119,
        0,
        1,
        152,
        0,
        27,
        128,
        0,
        232,
        0,
        7,
        144,
        0,
        47,
        128,
        0,
        192,
        0,
        13,
        192,
        0,
        51,
        0,
        1,
        248,
        0,
        23,
        192,
        0,
        178,
        0,
        3,
        0,
        0,
        58,
        128,
        1,
        124,
        0,
        6,
        160,
        0,
        55,
        0,
        3,
        168,
        0,
        28,
        0,
        0,
        98,
        0,
        6,
        64,
        0,
        16,
        128,
        1,
        244,
    ]
    assert Chepy(bytes(flag)).from_utf21().o == b"UDCTF{7w3nty_0n3?_Y0u_57up1d!}"
    assert Chepy("UDCTF{7w3nty_0n3?_Y0u_57up1d!}").to_utf21().o == bytes(flag)


def test_uuencode():
    data = """HI ZERO IM TRYING A NEW ENCRYPTION

EKO{UUENC0DED_ENCRYPTED?}"""
    assert (
        b"EKO{UUENC0DED_ENCRYPTED?}"
        in Chepy(data).to_uuencode().from_uuencode().remove_nullbytes().o
    )


def test_quoted_printable():
    assert Chepy("Exupéry").to_quoted_printable().o == b"Exup=C3=A9ry"
    assert Chepy("Exup=C3=A9ry").from_quoted_printable().o == "Exupéry".encode()


def test_rison():
    data = {"b": True, "c": {"d": [1, 2]}}
    assert Chepy(data).to_rison().o == b"(b:!t,c:(d:!(1,2)))"
    assert Chepy("(b:!t,c:(d:!(1,2)))").from_rison().o == data


def test_base92():
    data = "hello"
    assert Chepy(data).to_base92().o == b"Fc_$aOB"
    assert Chepy("").to_base92().o == b"~"
    assert Chepy(b"Fc_$aOB").from_base92().o == b"hello"
    assert Chepy("~").from_base92().o == b""


def test_base45():
    assert Chepy("+8D VDL2").from_base45().o == b"hello"
    assert Chepy("hello").to_base45().o == b"+8D VDL2"


def test_inc_dec_bytes():
    assert (
        Chepy("gmbh|cc265ceg113b731ec768c9eg95b98175~").decrement_bytes(1).o
        == b"flag{bb154bdf002a620db657b8df84a87064}"
    )
    assert (
        Chepy("flag{bb154bdf002a620db657b8df84a87064}").increment_bytes(1).o
        == b"gmbh|cc265ceg113b731ec768c9eg95b98175~"
    )


def test_parse_csv():
    csv_data = """index,url,title,visit
1,http://example.com,Example,1
2,http://example.org,Example Org,2
3,http://example.net,Example Net,3"""
    assert (
        Chepy(csv_data).parse_csv().get_by_index(0).get_by_key("title").o == b"Example"
    )


def test_parse_sqlite():
    data = "U1FMaXRlIGZvcm1hdCAzABAAAQEAQCAgAAAABAAAAAIAAAAAAAAAAAAAAAMAAAAEAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAC5m6A0AAAABD6QAD6QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABaAQcXExMBgRt0YWJsZWZvb2ZvbwJDUkVBVEUgVEFCTEUgImZvbyIgKAoJImlkIglJTlRFR0VSLAoJInZhbHVlIglURVhULAoJUFJJTUFSWSBLRVkoImlkIikKKQ0AAAACD+4AD/gP7gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAgMAF2hlbGxvBgEDABNiYXI="
    assert (
        Chepy(data)
        .from_base64()
        .parse_sqlite("select * from foo;")
        .get_by_index(0)
        .get_by_key("value")
        .o
        == b"bar"
    )


def test_italics():
    assert (
        Chepy("hello 123 !@$@# world").to_italics().out_as_any
        == "𝘩𝘦𝘭𝘭𝘰 123 !@$@# 𝘸𝘰𝘳𝘭𝘥"
    )
    assert (
        Chepy("𝘩𝘦𝘭𝘭𝘰 123 !@$@# 𝘸𝘰𝘳𝘭𝘥").from_italics().out_as_any
        == "hello 123 !@$@# world"
    )
