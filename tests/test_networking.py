from chepy import Chepy


def test_defang_url():
    assert (
        Chepy("https://app.google.com/?lol=some data&a=1").defang_url().o
        == b"hxxps://app[.]google[.]com/?lol=some data&a=1"
    )


def test_refang_url():
    assert (
        Chepy("hxxps://app[.]google[.]com/?lol=some data&a=1").refang_url().o
        == b"https://app.google.com/?lol=some data&a=1"
    )


def test_defang_ip():
    assert (
        Chepy("2001:4860:4860::8844").defang_ip().o == b"2001[:]4860[:]4860[:][:]8844"
    )
    assert Chepy("127.0.0.1").defang_ip().o == b"127[.]0[.]0[.]1"


def test_refang_ip():
    assert Chepy("127[.]0[.]0[.]1").refang_ip().o == b"127.0.0.1"


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
    assert Chepy("google.com").get_ssl_cert().o["subject"]["commonName"] != ""


def test_int_to_ip():
    assert Chepy("2130706433").int_to_ip().o == b"127.0.0.1"
    assert Chepy("127.0.0.1").ip_to_int().o == 2130706433
