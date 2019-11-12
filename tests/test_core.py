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

