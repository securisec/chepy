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


def test_remove_whitespace():
    assert (
        Chepy("some    long space\n\ttab space\flol").remove_whitespace().o
        == "somelongspacetabspacelol"
    )


def test_swap_case():
    assert Chepy("SoMe TeXt").swap_case().o == "sOmE tExT"


def test_lower_case():
    assert Chepy("HelLo WorLd").to_lower_case().o == "hello world"


def test_search():
    assert (
        len(Chepy("loLolololoL").regex_search("ol", ignore_case=True).str_to_list().o)
        == 5
    )


def test_remove_nullbytes():
    assert (
        Chepy("./tests/files/hello")
        .load_file()
        .remove_nullbytes()
        .binary_to_hex()
        .o[0:4]
        .decode()
        == "cffa"
    )


def test_split_by():
    assert len(Chepy("some lol random lolol data").split_by("lo").o) == 4


def test_unique():
    assert len(Chepy('["a", "a", 1]').str_to_list().unique().o) == 2


def test_sorted():
    assert Chepy(["a", "b", "1", "2"]).sorted().o == ["1", "2", "a", "b"]


def test_filter():
    assert Chepy('[{"a": 1}, {"b": 2}, {"a": 1, "b": 3}]').str_to_list().filter_by(
        "b"
    ).o == [{"b": 2}, {"a": 1, "b": 3},]


def test_slick():
    assert Chepy("some data").slice(3, 6).o == "e d"


def test_find_replace():
    assert Chepy("some some data").find_replace(r"some\s", "data").o == "datadatadata"

