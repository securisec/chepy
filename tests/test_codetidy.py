import string
from chepy import Chepy


def test_minify_json():
    assert len(Chepy("tests/files/test.json").load_file().minify_json().o) == 5648


def test_beautify_json():
    assert (
        len(Chepy("tests/files/test.json").load_file().minify_json().beautify_json().o)
        > 6000
    )


def test_to_uppercase():
    assert Chepy("some String").to_upper_case(by="word").o == b"Some String"
    assert Chepy("some String").to_upper_case(by="sentence").o == b"Some string"
    assert Chepy("some String").to_upper_case(by="all").o == b"SOME STRING"


def test_to_snake_case():
    assert Chepy("helloWorld").to_snake_case().o == b"hello_world"


def test_to_camel_case():
    assert Chepy("some Data_test").to_camel_case().o == b"someDataTest"
    assert (
        Chepy("some Data_test").to_camel_case(ignore_space=True).o == b"some DataTest"
    )


def test_to_kebab_case():
    assert Chepy("Some data_test").to_kebab_case().o == b"some-data-test"


def test_remove_whitespace():
    assert (
        Chepy("some    long space\n\ttab space\flol").remove_whitespace().o
        == b"somelongspacetabspacelol"
    )


def test_swap_case():
    assert Chepy("SoMe TeXt").swap_case().o == b"sOmE tExT"


def test_lower_case():
    assert Chepy("HelLo WorLd").to_lower_case().o == b"hello world"


def test_leet_speak():
    assert Chepy("somexValue").to_leetspeak().o == b"50m3%V@1u3"
    assert Chepy("somexValue").to_leetspeak(False).o == b"50m3xVa1u3"


def test_random_case():
    data = string.ascii_letters * 5
    assert Chepy(data).random_case().o != data
