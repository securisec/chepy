from chepy import Chepy


def test_detect_file_type():
    Chepy("tests/files/hello").load_file().get_mime(
        set_state=True
    ).o == "application/x-executable"
    assert True
    Chepy("tests/files/encoding").load_file().get_mime(set_state=True).o == "text/plain"
    assert True


def test_get_metadata():
    assert Chepy("logo.png").load_file().get_metadata(set_state=True).o == {
        "Bits/pixel": "32",
        "Compression": "deflate",
        "Compression rate": "138.6x",
        "Creation date": "2019-11-30 21:40:30",
        "Endianness": "Big endian",
        "Image DPI height": "3780 DPI",
        "Image DPI width": "3780 DPI",
        "Image height": "1080 pixels",
        "Image width": "1920 pixels",
        "MIME type": "image/png",
        "Pixel format": "RGBA",
    }


def test_embedded():
    Chepy("logo.png").load_file().embedded_files()
    assert True
