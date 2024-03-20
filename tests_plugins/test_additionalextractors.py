from chepy import Chepy


def test_jpath():
    assert (
        Chepy("tests/files/test.json")
        .load_file()
        .jpath_selector("[*].name.first")
        .get_by_index(2)
        .o
        == b"Long"
    )


# def test_php_deserialzie():
#     assert Chepy(
#         'a:3:{i:1;s:6:"elem 1";i:2;s:6:"elem 2";i:3;s:7:" elem 3";}'
#     ).php_deserialize().o == {1: b"elem 1", 2: b"elem 2", 3: b" elem 3"}


def test_minify_xml():
    assert len(Chepy("tests/files/test.xml").load_file().minify_xml().o) == 6392


def test_beautify_xml():
    assert (
        len(Chepy("tests/files/test.xml").load_file().minify_xml().beautify_xml().o)
        == 7690
    )
