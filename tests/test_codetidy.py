from chepy import Chepy


def test_minify_json():
    assert len(Chepy("tests/files/test.json").load_file().minify_json().o) == 5648


def test_beautify_json():
    assert (
        len(Chepy("tests/files/test.json").load_file().minify_json().beautify_json().o)
        > 6000
    )


def test_to_uppercase():
    assert Chepy("some String").to_upper_case(by="word").o == "Some String"
    assert Chepy("some String").to_upper_case(by="sentence").o == "Some string"
    assert Chepy("some String").to_upper_case(by="all").o == "SOME STRING"


def test_to_snake_case():
    assert Chepy("helloWorld").to_snake_case().o == "hello_world"


def test_to_camel_case():
    assert Chepy("some Data_test").to_camel_case().o == "someDataTest"
    assert Chepy("some Data_test").to_camel_case(ignore_space=True).o == "some DataTest"


def test_to_kebab_case():
    assert Chepy("Some data_test").to_kebab_case().o == "some-data-test"


def test_remove_whitespace():
    assert (
        Chepy("some    long space\n\ttab space\flol").remove_whitespace().o
        == "somelongspacetabspacelol"
    )


def test_swap_case():
    assert Chepy("SoMe TeXt").swap_case().o == "sOmE tExT"


def test_lower_case():
    assert Chepy("HelLo WorLd").to_lower_case().o == "hello world"


def test_leet_speak():
    assert Chepy("somexValue").to_leetspeak().o == "50m3%V@1u3"
    assert Chepy("somexValue").to_leetspeak(False).o == "50m3xVa1u3"
