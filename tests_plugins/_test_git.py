from chepy import Chepy


def test_git_author():
    assert Chepy("chepy/chepy_plugins").git_authors().o.get("securisec")


def test_git_code_search():
    assert len(Chepy("chepy/chepy_plugins").git_search_code("markdown").o) > 0

