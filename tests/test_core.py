import os
from chepy import Chepy


def test_states():
    c = Chepy("AA", "BB")
    state1 = c.to_hex().o
    c.change_state(1)
    state2 = c.to_hex().o
    assert state1 == b"4141"
    assert state2 == b"4242"


def test_substring():
    assert Chepy("some data").substring("s(ome)", 1).o == "ome"
    assert Chepy("some data").substring("s(ome)").o == "some"


def test_get_state():
    assert Chepy("state 1", "/state/2").get_state(1) == "/state/2"


def test_create_state():
    assert Chepy("some data").create_state().states == {0: "some data", 1: {}}


def test_copy_state():
    c = Chepy("some data")
    c.create_state()
    c.copy_state(1)
    assert c.states == {0: "some data", 1: "some data"}


def test_set_state():
    assert Chepy("some data").set_state("new data").o == "new data"


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
    assert str(Chepy(bytearray(b"abc"))) == "bytearray in state"


def test_convert_to_bytes():
    assert Chepy(b"A")._convert_to_bytes() == b"A"
    assert Chepy("A")._convert_to_bytes() == b"A"
    assert Chepy(1)._convert_to_bytes() == b"1"
    assert Chepy({"a": "b"})._convert_to_bytes() == b"{'a': 'b'}"
    assert Chepy(["a"])._convert_to_bytes() == b"['a']"
    assert Chepy(True)._convert_to_bytes() == b"True"
    assert Chepy(bytearray("a", "utf8"))._convert_to_bytes() == b"a"
    assert str(Chepy(bytearray(b"abc"))) == "bytearray in state"


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


def test_get_type():
    assert Chepy("a").get_type() == "str"


def test_write_to_file():
    Chepy(b"\x41").write_to_file(".test", as_binary=True)
    with open(".test", "r") as f:
        assert f.read() == "A"
    Chepy("A").write_to_file(".test")
    with open(".test", "r") as f:
        assert f.read() == "A"
    os.remove(".test")
