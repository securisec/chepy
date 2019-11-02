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
