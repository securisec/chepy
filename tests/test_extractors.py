from pathlib import Path
from chepy import Chepy


def test_extract_strings():
    assert len(Chepy("tests/files/hello").load_file().extract_strings().o) == 29


def test_extract_ips():
    assert len(Chepy("127.0.0.1\n::80").extract_ips().o) == 2


def test_extract_email():
    assert (
        len(Chepy("tests/files/test.der").load_file().extract_email(is_binary=True).o)
        == 2
    )


def test_extract_mac_address():
    assert (
        len(
            Chepy("01:23:45:67:89:ab | 127.0.0.1 | fE:dC:bA:98:76:54")
            .extract_mac_address()
            .o
        )
        == 2
    )


def test_extract_urls():
    assert (
        len(
            Chepy(
                "https://google.com, https://google.com/app&lo=lol, \
                http://localhost:800, file://test, ftp://test,]"
            )
            .extract_urls()
            .o
        )
        == 5
    )


def test_extract_domains():
    assert (
        len(
            Chepy(
                "https://google.com, https://google.com/app&lo=lol, \
                http://localhost:800, file://test, ftp://test,]"
            )
            .extract_domains()
            .o
        )
        == 3
    )


def test_xpath():
    assert (
        Chepy("tests/files/test.html")
        .load_file()
        .xpath_selector("//title/text()")
        .get_by_index(0)
        .o
        == "Example Domain"
    )


def test_css():
    assert (
        Chepy("http://example.com")
        .http_request()
        .css_selector("title")
        .get_by_index(0)
        .o
        == "<title>Example Domain</title>"
    )


def test_jpath():
    assert (
        Chepy("tests/files/test.json")
        .load_file()
        .jpath_selector("[*].name.first")
        .get_by_index(2)
        .o
        == "Long"
    )


def test_html_comments():
    assert len(Chepy("tests/files/test.html").load_file().html_comments().o) == 3


def test_js_comments():
    assert len(Chepy("tests/files/test.js").load_file().js_comments().o) == 3


def test_html_tag():
    assert Chepy("tests/files/test.html").load_file().html_tags("p").o == [
        {"tag": "p", "attributes": {"someval": "someval", "ano-ther": "another"}},
        {"tag": "p", "attributes": {}},
    ]

