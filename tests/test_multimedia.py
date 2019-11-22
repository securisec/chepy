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
