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
    assert Chepy("127.0.0.1").defang_ip().o == "127[.]0[.]0[.]1"


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


def test_parse_uri():
    assert Chepy("http://example.com/resource?foo=bar#fragment").parse_uri().o == {
        "scheme": "http",
        "location": "example.com",
        "path": "/resource",
        "params": "",
        "query": {"foo": ["bar"]},
        "fragment": "fragment",
    }


def test_parse_ip_range():
    assert len(Chepy("10.10.10.1/24").parse_ip_range().o) == 254


def test_parse_ipv6():
    assert Chepy("2001:4860:4860::8888").parse_ipv6().o == {
        "long": "2001:4860:4860:0000:0000:0000:0000:8888",
        "short": "2001:4860:4860::8888",
    }


def test_get_cert():
    assert Chepy("google.com").get_ssl_cert().o["subject"]["countryName"] == "US"

