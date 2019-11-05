from chepy import Chepy


def test_reverse():
    assert Chepy("abcdefg").reverse().output == "gfedcba"


def test_reverse_1():
    assert Chepy("abcdefgh").reverse(4).output == "efghabcd"


def test_count_occurances():
    assert (
        Chepy("AABCDADJAKDJHKSDAJSDdaskjdhaskdjhasdkja").count_occurances("ja").output
        == 2
    )


def test_to_uppercase():
    assert Chepy("some String").to_upper_case(by="word").o == "Some String"


def test_to_snake_case():
    assert Chepy("helloWorld").to_snake_case().o == "hello_world"


def test_to_camel_case():
    assert Chepy("some Data_test").to_camel_case().o == "someDataTest"


def test_to_kebab_case():
    assert Chepy("Some data_test").to_kebab_case().o == "some-data-test"

