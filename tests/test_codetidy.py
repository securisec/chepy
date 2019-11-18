from chepy import Chepy


def test_minify_json():
    assert len(Chepy("tests/files/test.json").load_file().minify_json().o) == 5664


def test_beautify_json():
    assert (
        len(Chepy("tests/files/test.json").load_file().minify_json().beautify_json().o)
        == 7420
    )


def test_minify_xml():
    assert len(Chepy("tests/files/test.xml").load_file().minify_xml().o) == 6392


def test_beautify_xml():
    assert (
        len(Chepy("tests/files/test.xml").load_file().minify_xml().beautify_xml().o)
        == 7690
    )

