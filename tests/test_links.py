from chepy import Chepy


def test_pastebin_to_raw():
    assert (
        Chepy("https://pastebin.com/abCD").pastebin_to_raw().o
        == b"https://pastebin.com/raw/abCD"
    )


def test_github_to_raw():
    assert (
        Chepy("https://github.com/securisec/chepy/blob/master/README.md")
        .github_to_raw()
        .o
        == b"https://raw.githubusercontent.com/securisec/chepy/master/README.md"
    )


def test_google_search_ei_to_epoch():
    assert Chepy("Bh8hYqykHc64mAXkkoTgCg==").google_search_ei_to_epoch().o == 1646337798


# def test_to_unix_timestamp():
#     assert Chepy("Sun Nov 10 17:57:29 2019").to_unix_timestamp().o == 1573426649
