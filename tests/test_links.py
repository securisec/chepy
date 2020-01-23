from chepy import Chepy


def test_pastebin_to_raw():
    assert (
        Chepy("https://pastebin.com/abCD").pastebin_to_raw().o
        == "https://pastebin.com/raw/abCD"
    )


def test_github_to_raw():
    assert (
        Chepy(
            "https://github.com/securisec/chepy/blob/master/README.md"
        ).github_to_raw().o
        == "https://raw.githubusercontent.com/securisec/chepy/master/README.md"
    )


# def test_to_unix_ts():
#     assert Chepy("Sun Nov 10 17:57:29 2019").to_unix_ts().o == 1573426649
