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
    assert Chepy("some data").debug(True).substring("s(ome)", 1).o == "ome"
    assert Chepy("some data").substring("s(ome)").o == "some"


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
    assert Chepy("some data").set_state("new data").o == "new data"


def test_run_script():
    assert Chepy("A").to_hex().run_script("tests/files/script.py", True).o == b"4141"
    assert Chepy("A").to_hex().run_script("tests/files/script.py").o == b"41"


def test_fork():
    c = Chepy("A", "B")
    assert Chepy("A", "B").fork(
        [("to_hex",), ("hmac_hash", {"key": "secret", "digest": "md5"})]
    ).states == {
        0: "3e90033ea5422dafd81470dde4ffb37b",
        1: "c474a4a957fe2018e2bffef53887ae22",
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


def test_http_request():
    assert Chepy("https://example.com").http_request().get_by_key("status").o == 200


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


def test_out_as_str():
    assert Chepy(b"a").out_as_str() == "a"
    assert Chepy("a").out_as_str() == "a"


def test_out_as_bytes():
    assert Chepy(b"a").out_as_bytes() == b"a"
    assert Chepy("a").out_as_bytes() == b"a"


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
    assert Chepy("4142").from_hex()._stack == [{"function": "from_hex", "args": {}}]


def test_run_recipe():
    assert (
        Chepy("bG9sCg==")
        .run_recipe(
            recipes=[
                {
                    "function": "base64_decode",
                    "args": {"custom": None, "fix_padding": True},
                },
                {"function": "swap_case", "args": {}},
            ]
        )
        .o
        == "LOL\n"
    )


def test_recipe():
    temp = str(Path(tempfile.gettempdir()) / os.urandom(24).hex())
    Chepy(
        "tests/files/encoding"
    ).load_file().reverse().rot_13().base64_decode().base32_decode().str_from_hexdump().save_recipe(
        temp
    )

    assert (
        Chepy("tests/files/encoding").load_recipe(temp).o
        == "StormCTF{Spot3:DcEC6181F48e3B9D3dF77Dd827BF34e0}"
    )
    Path(temp).unlink()


def test_loop():
    assert (
        Chepy("VmpGb2QxTXhXWGxTYmxKV1lrZDRWVmx0ZEV0alZsSllaVWRHYWxWVU1Eaz0=")
        .loop(6, "base64_decode")
        .o
        == b"securisec"
    )


def test_loop_list():
    c = Chepy(["an", "array"])
    c.loop_list("to_hex").loop_list("hmac_hash", {"key": "secret"})
    assert c.o == [
        "5cbe6ca2a66b380aec1449d4ebb0d40ac5e1b92e",
        "30d75bf34740e8781cd4ec7b122e3efd8448e270",
    ]
    c1 = Chepy(["an", "array"])
    c1.loop_list("to_hex").loop_list("hmac_hash", {"key": "secret"})
    assert c1.o == [
        "5cbe6ca2a66b380aec1449d4ebb0d40ac5e1b92e",
        "30d75bf34740e8781cd4ec7b122e3efd8448e270",
    ]


def test_loop_dict():
    data = [{"some": "val"}, {"some": "another"}, {"lol": "lol"}, {"another": "aaaa"}]
    c = Chepy(data)
    c.loop_list("loop_dict", {"keys": ["some", "lol"], "callback": "to_upper_case"})
    assert c.o == [
        {"some": "VAL"},
        {"some": "ANOTHER"},
        {"lol": "LOL"},
        {"another": "aaaa"},
    ]

    d = Chepy({"some": "hahahaha", "lol": "aahahah"})
    d.loop_dict(["some"], "to_upper_case")
    assert d.o == {"some": "HAHAHAHA", "lol": "aahahah"}

    e = Chepy({"some": "hahahaha", "lol": "aahahah"})
    e.loop_dict(["some"], "hmac_hash", {"key": "secret"})
    assert e.o == {"some": "99f77ec06a3c69a4a95371a7888245ba57f47f55", "lol": "aahahah"}


def test_reset():
    assert Chepy("41", "42").from_hex().reset().states == {0: "41", 1: "42"}


def test_load_from_url():
    assert (
        type(
            Chepy("https://s2.googleusercontent.com/s2/favicons?domain=apple.com")
            .load_from_url()
            .o
        )
        == bytes
    )


def test_for_each():
    assert Chepy(["41", "42"]).for_each([("from_hex",), ("to_hex",)]).o == [
        b"41",
        b"42",
    ]
