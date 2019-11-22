from chepy import Chepy


def test_image_resize():
    assert len(Chepy("logo.png").read_file().resize_image(128, 128, "png").o) == 1525
    assert (
        len(Chepy("logo.png").read_file().resize_image(128, 128, "png", "hamming").o)
        == 1525
    )
    assert (
        len(Chepy("logo.png").read_file().resize_image(128, 128, "png", "box").o)
        == 1525
    )
    assert (
        len(Chepy("logo.png").read_file().resize_image(128, 128, "png", "bilinear").o)
        == 1525
    )
    assert (
        len(Chepy("logo.png").read_file().resize_image(128, 128, "png", "antialias").o)
        == 1525
    )


def test_split_color_channels():
    assert len(Chepy("logo.png").load_file().split_color_channels().o) == 3


def test_roate_image():
    c1 = Chepy("logo.png").load_file()
    c2 = Chepy("logo.png").load_file().rotate_image(180)
    assert c1 != c2
