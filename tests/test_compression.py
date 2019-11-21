from chepy import Chepy


def test_zip_info():
    assert (
        Chepy("tests/files/test.zip")
        .read_file()
        .zip_info()
        .get_by_index(0)
        .get_by_key("encrypted")
        .o
        == True
    )


def test_zip_extract_one():
    assert (
        Chepy("tests/files/test.zip").read_file().unzip_one("lol.txt", "password").o
        == b"lol\n"
    )


def test_zip_extract_all():
    assert (
        Chepy("tests/files/test.zip")
        .load_file()
        .unzip_all("password")
        .get_by_index(1)
        .o
        == b"StormCTF{Misc2:B73dba52ceDA4dDccb31Ec1b1cDa24Ff}"
    )


def test_create_zip():
    assert (
        Chepy("A").to_hex().create_zip_file("some.txt").to_hex().slice(0, 8).o
        == b"504b0304"
    )
