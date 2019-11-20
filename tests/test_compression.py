from chepy import Chepy


def test_zip_info():
    assert (
        Chepy("tests/files/test.zip")
        .read_file()
        .zip_info()
        .get_by_index(0)
        .get_by_key("encrypted")
        .o
        == False
    )

