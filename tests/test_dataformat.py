from chepy import Chepy


def test_dict_to_json():
    assert (
        Chepy({"some": "data", "a": ["list", 1, True]}).dict_to_json().o
        == '{"some": "data", "a": ["list", 1, true]}'
    )


def test_json_to_dict():
    assert Chepy('{"some": "data", "a": ["list", 1, true]}').json_to_dict().o == {
        "some": "data",
        "a": ["list", 1, True],
    }


def test_yaml_to_json():
    data = """# An employee record
name: Martin D'vloper
job: Developer
skill: Elite
employed: True
foods:
    - Apple
    - Orange
    - Strawberry
    - Mango
languages:
    perl: Elite
    python: Elite
    pascal: Lame
education: |
    4 GCSEs
    3 A-Levels
    BSc in the Internet of Things
"""
    assert (
        Chepy(data).yaml_to_json().o
        == '{"name": "Martin D\'vloper", "job": "Developer", "skill": "Elite", "employed": true, "foods": ["Apple", "Orange", "Strawberry", "Mango"], "languages": {"perl": "Elite", "python": "Elite", "pascal": "Lame"}, "education": "4 GCSEs\\n3 A-Levels\\nBSc in the Internet of Things\\n"}'
    )


def test_json_to_yaml():
    data = '{"name": "Martin D\'vloper", "job": "Developer", "skill": "Elite", "employed": true, "foods": ["Apple", "Orange", "Strawberry", "Mango"], "languages": {"perl": "Elite", "python": "Elite", "pascal": "Lame"}, "education": "4 GCSEs\\n3 A-Levels\\nBSc in the Internet of Things\\n"}'
    assert (
        Chepy(data).json_to_yaml().o
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


def test_base_58_decode():
    assert Chepy("2UDrs31qcWSPi").base_58_decode().output.decode() == "some data"


def test_base_85_encode():
    assert Chepy("some data").base_85_encode().output.decode() == "F)Po,+Cno&@/"


def test_base_85_decode():
    assert Chepy("F)Po,+Cno&@/").base_85_decode().output.decode() == "some data"


def test_base_32_encode():
    assert Chepy("some data").base_32_encode().output.decode() == "ONXW2ZJAMRQXIYI="


def test_base_64_encode():
    assert Chepy("some data").base_64_encode().output.decode() == "c29tZSBkYXRh"


def test_base_58_encode():
    assert Chepy("some data").base_58_encode().output.decode() == "2UDrs31qcWSPi"


def test_to_hex():
    assert Chepy("AAA").to_hex().out().decode() == "414141"


def test_hex_to_int():
    assert Chepy("0x123").hex_to_int().output == 291


def test_int_to_hex():
    assert Chepy(101).int_to_hex().o == "65"


def test_url_encode():
    assert (
        Chepy("https://google.com/?lol=some data&a=1").url_encode(safe="/:").o
        == "https://google.com/%3Flol%3Dsome+data%26a%3D1"
    )


def test_url_decode():
    assert (
        Chepy("https://google.com/%3Flol%3Dsome+data%26a%3D1").url_decode().o
        == "https://google.com/?lol=some data&a=1"
    )


def test_to_list():
    assert Chepy("[1,2,'lol', true]").str_to_list().o == [1, 2, "lol", True]


def test_normalize_hex():
    assert Chepy("41:42:CE").normalize_hex().o == "4142CE"
    assert Chepy("0x410x420xce").normalize_hex().o == "4142ce"
    assert (
        Chepy("tests/files/hello", True).normalize_hex(True).o[0:6].decode() == "cffaed"
    )


def test_bytearray_to_str():
    assert Chepy(bytearray("lolol", "utf")).bytearray_to_str().o == "lolol"


def test_get_by_index():
    assert Chepy([1, "a", True]).get_by_index(2).state == True


def test_get_by_key():
    assert Chepy('{"some": "data"}').json_to_dict().get_by_key("some").o == "data"

