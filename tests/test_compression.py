from chepy import Chepy
import re


def test_fix_zip_header():
    assert (
        Chepy(
            "4834434b1400000008003a9d7f502a0ae5b6230000002a00000008001c00666c61672e747874555409000340d5835e40d5835e75780b000104e803000004e8030000f3f109ae2e294a4ccf4c8ecf2bcd4d4a2d8acfcd2f4a8dcfc9cc4e8dcf4512aee50200504b01021e031400000008003a9d7f502a0ae5b6230000002a000000080018000000000001000000808100000000666c61672e747874555405000340d5835e75780b000104e803000004e8030000504b050600000000010001004e000000650000000000"
        )
        .from_hex()
        .fix_zip_header()
        .unzip_one("flag.txt")
        .trim()
        .o
        == b"LLS{tragic_number_more_like_magic_number}"
    )


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


def test_zip_compress():
    c = Chepy("some data").zip_compress("file").o
    assert c[:2] == b"PK"
    assert b"some data" in c


def test_zip_compress_symlink():
    c = Chepy("some data").zip_compress_symlink("file", "target").o
    assert c[:2] == b"PK"
    assert b"target" in c


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
        .hex_to_bytes()
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


def test_raw_deflate_inflate():
    assert Chepy("securisec").raw_deflate().raw_inflate().o == b"securisec"


def test_lz4_compress():
    assert (
        Chepy("data").lz4_compress().to_hex().o
        == b"04224d1868400400000000000000cd040000806461746100000000"
    )


def test_lz4_decompress():
    assert (
        Chepy("04224d1868400400000000000000cd040000806461746100000000")
        .from_hex()
        .lz4_decompress()
        .o
        == b"data"
    )

def test_lz77():
    input_str = "(0,0,O)(0,0,M)(0,0,G)(1,1,G)(3,3, )(0,0,Y)(10,1,U)(4,1,A)(0,0,R)(0,0,E)(4,1,C)(0,0,L)(9,1,S)(6,2,T)(5,1, )(3,1,H)(7,2,F)(13,1,A)(1,1,A)(2,2,G)(36,7,C)(28,5,C)(6,5,W)(3,1,L)(1,1, )(0,0,N)(10,1,W)(40,3,I)(15,1, )(3,3,T)(48,6,G)(5,1,E)(0,0,K)(22,1,{)(25,1,I)(38,1,E)(1,1,E)(3,3,E)(7,7,E)(15,15,_)(38,3,O)(2,2,O)(5,5,O)(11,11,O)(3,3,_)(63,23,})"
    array_of_arrays = []
    regex = r"\((\d+),(\d+),([A-Z\s_{}]+)\)"
    matches = re.findall(regex, input_str)

    for match in matches:
        param1, param2, param3 = match
        array_of_arrays.append([int(param1), int(param2), param3])

    assert b'EKO{' in Chepy(array_of_arrays).lz77_decompress().o

    assert Chepy('OMGGGGGG').lz77_compress(1).o[1] == [0, 0, 'M']