import os
import tempfile
from pathlib import Path
from chepy import Chepy


def test_states():
    c = Chepy("AA", "BB").debug()
    state1 = c.to_hex().o
    c.change_state(1)
    state2 = c.to_hex().o
    assert state1 == b"4141"
    assert state2 == b"4242"


def test_substring():
    assert Chepy("some data").debug(True).substring("s(ome)", 1).o == b"ome"
    assert Chepy("some data").substring("s(ome)").o == b"some"


def test_get_state():
    assert Chepy("state 1", "/state/2").get_state(1) == "/state/2"


def test_create_state():
    assert Chepy("some data").create_state().states == {0: "some data", 1: {}}


def test_copy_state():
    assert Chepy("some data").create_state().copy_state(1).states == {
        0: "some data",
        1: "some data",
    }
    assert Chepy("some data").copy_state().states == {0: "some data", 1: "some data"}


def test_set_state():
    assert Chepy("some data").set_state("new data").o == b"new data"


def test_run_script():
    assert Chepy("A").to_hex().run_script("tests/files/script.py", True).o == b"4141"
    assert Chepy("A").to_hex().run_script("tests/files/script.py").o == b"41"


def test_fork():
    c = Chepy("A", "B")
    assert Chepy("A", "B").fork(
        [("to_hex",), ("hmac_hash", {"key": "secret", "digest": "md5"})]
    ).states == {
        0: b"3e90033ea5422dafd81470dde4ffb37b",
        1: b"c474a4a957fe2018e2bffef53887ae22",
    }
    assert c.fork([(c.to_hex,)]).states == {0: b"41", 1: b"42"}


def test_save_buffer():
    c = Chepy("A").save_buffer(0).str_to_hex().save_buffer(1)
    assert c.buffers[0] == "A"
    assert c.buffers[1] == b"41"


def test_load_buffer():
    c = Chepy("A").save_buffer(0).to_hex().save_buffer(0)
    assert c.buffers[0] == b"41"
    assert c.load_buffer(0).state == b"41"


# def test_http_request():
#     assert Chepy("https://example.com").http_request().get_by_key("status").o == 200


def test_get_by_key():
    data2 = {
        "menu": {
            "id": "file",
            "value": "File",
            "popup": {
                "menuitem": [
                    {"value": "New", "onclick": "CreateNewDoc()"},
                    {"value": "Open", "onclick": "OpenDoc()"},
                    {"value": "Close", "onclick": "CloseDoc()"},
                ]
            },
        }
    }
    assert Chepy(data2).get_by_key("menu.popup.menuitem[1].value").o == b"Open"
    assert Chepy(data2).get_by_key("menu.popup.menuitem[].value").o == [
        "New",
        "Open",
        "Close",
    ]
    assert Chepy(data2).get_by_key("menu.popup.menuitem[0].value").o == b"New"
    assert Chepy(data2).get_by_key("menu").o.get("id") == "file"
    assert Chepy([{"a": "b"}, {"a": "d"}]).get_by_key("[].a").o == ["b", "d"]


def test_delete_state():
    assert Chepy("lol").create_state().delete_state(1).states == {0: "lol"}


def test_delete_buffer():
    assert Chepy("lol").save_buffer().save_buffer().delete_buffer(0).states == {
        0: "lol"
    }


def test___str__():
    assert str(Chepy("abc")) == "abc"
    assert str(Chepy(bytearray(b"abc"))) == "abc"


def test_convert_to_bytes():
    assert Chepy(b"A")._convert_to_bytes() == b"A"
    assert Chepy("A")._convert_to_bytes() == b"A"
    assert Chepy(1)._convert_to_bytes() == b"1"
    assert Chepy({"a": "b"})._convert_to_bytes() == b"{'a': 'b'}"
    assert Chepy(["a"])._convert_to_bytes() == b"['a']"
    assert Chepy(True)._convert_to_bytes() == b"True"
    assert Chepy(bytearray("a", "utf8"))._convert_to_bytes() == b"a"
    assert str(Chepy(bytearray(b"abc"))) == "abc"


def test_convert_to_str():
    assert Chepy(b"A")._convert_to_str() == "A"
    assert Chepy("A")._convert_to_str() == "A"
    assert Chepy(1)._convert_to_str() == "1"
    assert Chepy({"a": "b"})._convert_to_str() == "{'a': 'b'}"
    assert Chepy(["a"])._convert_to_str() == "['a']"
    assert Chepy(True)._convert_to_str() == "True"
    assert Chepy(bytearray("a", "utf8"))._convert_to_str() == "a"


def test_convert_to_bytearray():
    assert Chepy("a")._convert_to_bytearray() == bytearray(b"a")


def test_write_to_file():
    Chepy("A").write_to_file(".test")
    with open(".test", "r") as f:
        assert f.read() == "A"
    os.remove(".test")


def test_load_dir():
    assert len(Chepy("tests/files/").load_dir().states) >= 10


def test_load_file_binary():
    assert type(Chepy("tests/files/pkcs12").load_file(True).o) == bytearray


def test_show_recipe():
    assert Chepy("4142").from_hex().recipe == [
        {
            "function": "from_hex",
            "args": {"delimiter": None, "join_by": "", "replace": b"%|0x"},
        }
    ]


def test_run_recipe():
    assert (
        Chepy("bG9sCg==")
        .run_recipe(
            recipes=[
                {
                    "function": "from_base64",
                    "args": {"custom": None},
                },
                {"function": "swap_case", "args": {}},
            ]
        )
        .o
        == b"LOL\n"
    )


def test_recipe():
    temp = str(Path(tempfile.gettempdir()) / os.urandom(24).hex())
    Chepy("tests/files/encoding").load_file().reverse().rot_13().from_base64(
        remove_whitespace=False
    ).from_base32(remove_whitespace=False).str_from_hexdump().save_recipe(temp)

    assert (
        Chepy("tests/files/encoding").load_recipe(temp).o
        == b"StormCTF{Spot3:DcEC6181F48e3B9D3dF77Dd827BF34e0}"
    )
    Path(temp).unlink()


def test_loop():
    assert (
        Chepy("VmpGb2QxTXhXWGxTYmxKV1lrZDRWVmx0ZEV0alZsSllaVWRHYWxWVU1Eaz0=")
        .loop(6, "from_base64")
        .o
        == b"securisec"
    )
    c = Chepy("VmpGb2QxTXhXWGxTYmxKV1lrZDRWVmx0ZEV0alZsSllaVWRHYWxWVU1Eaz0=")
    assert c.loop(6, c.from_base64).o == b"securisec"


def test_loop_list():
    c = Chepy(["an", "array"])
    c.loop_list("to_hex").loop_list("hmac_hash", {"key": "secret"})
    assert c.o == [
        b"5cbe6ca2a66b380aec1449d4ebb0d40ac5e1b92e",
        b"30d75bf34740e8781cd4ec7b122e3efd8448e270",
    ]
    c1 = Chepy(["an", "array"])
    c1.loop_list("to_hex").loop_list(c.hmac_hash, {"key": "secret"})
    assert c1.o == [
        b"5cbe6ca2a66b380aec1449d4ebb0d40ac5e1b92e",
        b"30d75bf34740e8781cd4ec7b122e3efd8448e270",
    ]


def test_loop_dict():
    data = [{"some": "val"}, {"some": "another"}, {"lol": "lol"}, {"another": "aaaa"}]
    c = Chepy(data)
    c.loop_list("loop_dict", {"keys": ["some", "lol"], "callback": "to_upper_case"})
    assert c.o == [
        {"some": b"VAL"},
        {"some": b"ANOTHER"},
        {"lol": b"LOL"},
        {"another": "aaaa"},
    ]

    d = Chepy({"some": "hahahaha", "lol": b"aahahah"})
    d.loop_dict(["some"], d.to_upper_case)
    assert d.o == {"some": b"HAHAHAHA", "lol": b"aahahah"}

    e = Chepy({"some": "hahahaha", "lol": "aahahah"})
    e.loop_dict(["some"], "hmac_hash", {"key": "secret"})
    assert e.o == {
        "some": b"99f77ec06a3c69a4a95371a7888245ba57f47f55",
        "lol": "aahahah",
    }


def test_reset():
    assert Chepy("41", "42").from_hex().reset().states == {0: "41", 1: "42"}


def test_load_from_url():
    assert isinstance(
        Chepy("https://s2.googleusercontent.com/s2/favicons?domain=apple.com")
        .load_from_url()
        .o,
        bytes,
    )


def test_for_each():
    assert Chepy(["41", "42"]).for_each([("from_hex",), ("to_hex",)]).o == [
        b"41",
        b"42",
    ]
    assert Chepy(["41", "42"]).for_each([("from_hex",), ("to_hex",)], "").o == b"4142"


def test_subsection():
    assert (
        Chepy("he41ll42o").subsection(r"\d{2}", methods=[("from_hex",)]).o == b"heAllBo"
    )
    c = Chepy("he41ll42o")
    assert (
        c.subsection(
            b"\d{2}", methods=[(c.from_hex,), (c.hmac_hash, {"key": "secret"})]
        ).o
        == b"he955a367a4c01f58118021054729c7fb54b5de94ell9cba467d60276777ce655337e060fa0aebfcc780o"
    )


def test_callback():
    def cb(data):
        return data * 2

    assert Chepy("abc").callback(cb).o == b"abcabc"


def test_get_by_index():
    assert Chepy("abc").get_by_index(0).o == b"a"
    assert Chepy("abc").get_by_index(0, 2).o == ["a", "c"]


def test_register():
    # test set register
    c1 = Chepy("hello")
    assert c1._registers == {}
    c1.set_register("a", "test")
    assert c1._registers == {"a": "test"}
    # test register
    # test get_register

    data = """key = 'cGFzc3dvcmRwYXNzd29yZA=='

out = c52f0da8f2217771f4f4cd06e2f014f9
"""

    c = Chepy(data)
    c.register("key = '(.+)'", unicode=True)
    c.regex_search("out = (.+)").get_by_index(0).from_hex()
    c.aes_decrypt(c.get_register("$R0"), key_format="base64", mode="ECB")
    assert c.o == b"hello"
    # test get_register
    assert c.get_register("$R0") == "cGFzc3dvcmRwYXNzd29yZA=="

    data = """key = 'cGFzc3dvcmRwYXNzd29yZA=='

out = c52f0da8f2217771f4f4cd06e2f014f9
"""

    c = Chepy(data)
    c.register(b"key = '(.+)'", ignore_case=True, multiline=True, dotall=True)
    c.regex_search("out = (.+)").get_by_index(0).from_hex()
    c.aes_decrypt(c.get_register("$R0"), key_format="base64", mode="ECB")
    assert c.o == b"hello"


def test_ixs():
    assert Chepy("b").prefix("a").o == b"ab"
    assert Chepy("b").suffix("a").o == b"ba"
