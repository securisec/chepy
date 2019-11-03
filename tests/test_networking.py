from chepy import Chepy


def test_defang_url():
    assert (
        Chepy("https://app.google.com/?lol=some data&a=1").defang_url().o
        == "hxxps://app[.]google[.]com/?lol=some data&a=1"
    )


def test_refang_url():
    assert (
        Chepy("hxxps://app[.]google[.]com/?lol=some data&a=1").refang_url().o
        == "https://app.google.com/?lol=some data&a=1"
    )


def test_defang_ip():
    assert Chepy("2001:4860:4860::8844").defang_ip().o == "2001[:]4860[:]4860[:][:]8844"


def test_refang_ip():
    assert Chepy("127[.]0[.]0[.]1").refang_ip().o == "127.0.0.1"


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

