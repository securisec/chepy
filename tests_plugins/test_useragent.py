from chepy import Chepy


def test_parse_user_agent():
    ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0"
    assert Chepy(ua).parse_user_agent().o == {
        "user_agent": {"family": "Firefox", "major": "62", "minor": "0", "patch": None},
        "os": {
            "family": "Mac OS X",
            "major": "10",
            "minor": "10",
            "patch": None,
            "patch_minor": None,
        },
        "device": {"family": "Other", "brand": None, "model": None},
        "string": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0",
    }
