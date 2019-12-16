from chepy import Chepy


def test_markdown_to_html():
    assert Chepy("#one").markdown_to_html().o == "<h1>one</h1>"
