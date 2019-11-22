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


def test_gzip_compress():
    assert Chepy("A").to_hex().gzip_compress().to_hex().slice(0, 6).o == b"1f8b08"


def test_gzip_decompress():
    assert Chepy("A").to_hex().gzip_compress().gzip_decompress().o == b"41"


def test_bzip():
    c = Chepy("some data").bzip_compress()
    assert (
        c.state
        == b'BZh91AY&SY\x9f\xe2\xaa\x9d\x00\x00\x03\x91\x80@\x00&\x02\x8c\x00 \x00"\x1ahz\x10\xc0\x86k\xef\n\x82\xeeH\xa7\n\x12\x13\xfcUS\xa0'
    )
    assert c.bzip_decompress().o == b"some data"


def test_zlib_compress():
    assert (
        Chepy("some text").zlib_compress().to_hex().o
        == b"78da2bcecf4d552849ad28010011e8039a"
    )


def test_zlib_decompress():
    assert (
        Chepy("789c0580a10d000008c35ee1b9ca05c104e737b761ca5711e8039a")
        .hex_to_binary()
        .zlib_decompress()
        .o
        == b"some text"
    )

