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


def test_zip_list_files():
    assert len(Chepy("tests/files/test.zip").load_file().zip_list_files().o) == 2


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


def test_lzma_compress():
    assert (
        Chepy("some data").lzma_compress().to_hex().o
        == b"fd377a585a000004e6d6b4460200210116000000742fe5a3010008736f6d65206461746100000000bb22facdd6fa557b000121096c18c5d51fb6f37d010000000004595a"
    )


def test_lzma_decompress():
    assert (
        Chepy(
            "fd377a585a000004e6d6b4460200210116000000742fe5a3010008736f6d65206461746100000000bb22facdd6fa557b000121096c18c5d51fb6f37d010000000004595a"
        )
        .from_hex()
        .lzma_decompress()
        .o
        == b"some data"
    )


def test_tar_list_files():
    assert Chepy("tests/files/test.tar.gz").read_file().tar_list_files().o == [
        "test.js",
        "test.json",
    ]
    assert Chepy("tests/files/test.tar.gz").read_file().tar_list_files(mode="gz").o == [
        "test.js",
        "test.json",
    ]


def test_tar_extract_one():
    assert (
        b"comment"
        in Chepy("tests/files/test.tar.gz").read_file().tar_extract_one("test.js").o
    )
    assert (
        b"comment"
        in Chepy("tests/files/test.tar.gz")
        .read_file()
        .tar_extract_one("test.js", mode="gz")
        .o
    )


def test_tar_extract_all():
    assert len(Chepy("tests/files/test.tar.gz").read_file().tar_extract_all().o) == 2
    assert (
        len(Chepy("tests/files/test.tar.gz").read_file().tar_extract_all(mode="gz").o)
        == 2
    )


def test_tar_compress():
    assert len(Chepy("logo.png").read_file().tar_compress("some.png").o) > 50000
    assert (
        len(Chepy("logo.png").read_file().tar_compress("some.png", mode="").o) > 50000
    )
