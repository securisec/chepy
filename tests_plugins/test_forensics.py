from chepy import Chepy


# def test_file_mime():
#     assert Chepy("logo.png").load_file().file_mime().o == "image/png"


# def test_file_magic():
#     assert (
#         Chepy("logo.png").read_file().file_magic().o
#         == "PNG image data, 1920 x 1080, 8-bit/color RGBA, non-interlaced"
#     )


def test_get_metadata():
    assert Chepy("logo.png").load_file().get_metadata().o == {
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
