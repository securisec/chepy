import re
from chepy import Chepy


def test_image_resize():
    assert len(Chepy("logo.png").read_file().resize_image(128, 128, "png").o) == 1596
    assert (
        len(Chepy("logo.png").read_file().resize_image(128, 128, "png", "hamming").o)
        == 5476
    )
    assert (
        len(Chepy("logo.png").read_file().resize_image(128, 128, "png", "box").o)
        == 4866
    )
    assert (
        len(Chepy("logo.png").read_file().resize_image(128, 128, "png", "bilinear").o)
        == 5920
    )
    assert (
        len(Chepy("logo.png").read_file().resize_image(128, 128, "png", "antialias").o)
        == 7737
    )


def test_split_color_channels():
    assert len(Chepy("logo.png").load_file().split_color_channels("png").o) == 3


def test_rotate_image():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().rotate_image(180, "png").o
    assert c1 != c2


def test_grayscale_image():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().grayscale_image("png").o
    assert c1 != c2


def test_blur_image():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().blur_image("png").o
    c3 = Chepy("logo.png").load_file().blur_image(extension="png", gaussian=True).o
    assert c1 != c2
    assert c1 != c3


def test_invert_image():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().invert_image("png").o
    assert c1 != c2


def test_image_opacity():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().image_opacity(10, "png").o
    assert c1 != c2


def test_image_contrast():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().image_contrast(10, "png").o
    assert c1 != c2


def test_image_brightness():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().image_brightness(10, "png").o
    assert c1 != c2


def test_image_sharpness():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().image_sharpness(10, "png").o
    assert c1 != c2


def test_image_color():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().image_color(10, "png").o
    assert c1 != c2


def test_image_add_text():
    c1 = Chepy("logo.png").load_file().o
    c2 = Chepy("logo.png").load_file().image_add_text("some text").o
    assert c1 != c2


def test_convert_image():
    assert (
        Chepy("logo.png").load_file().convert_image("jpeg").to_hex().o[0:6] == b"ffd8ff"
    )


def test_lsb_by_channel():
    assert re.search(
        b"4E34B38257200616FB75CD869B8C3CF0",
        Chepy("tests/files/lsb.png").read_file().lsb_dump_by_channel().from_binary().o,
    )


def test_msb_by_channel():
    assert re.search(
        b"MSB_really_sucks",
        Chepy("tests/files/msb.png")
        .read_file()
        .msb_dump_by_channel("b", True)
        .from_binary()
        .o,
    )
