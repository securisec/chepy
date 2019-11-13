from chepy import Chepy


def test_states():
    c = Chepy("AA", "BB")
    state1 = c.to_hex().o
    c.change_state(1)
    state2 = c.to_hex().o
    assert state1 == b"4141"
    assert state2 == b"4242"


def test_subsection():
    assert Chepy("some data").subsection("s(ome)", 1).o == "ome"
    assert Chepy("some data").subsection("s(ome)").o == "some"


def test_get_state():
    assert Chepy("state 1", "/state/2").get_state(1) == "/state/2"


def test_create_state():
    assert Chepy("some data").create_state().states == {0: "some data", 1: {}}


def test_copy_state():
    c = Chepy("some data")
    c.create_state()
    c.copy_state(1)
    assert c.states == {0: "some data", 1: "some data"}


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


def test_http_request():
    assert Chepy("https://example.com").http_request().get_by_key("status").o == 200

