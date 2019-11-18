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
    assert (
        Chepy("AABCDADJAKDJHKSDAJSDdaskjdhaskdjhasdkja")
        .count_occurances("ja", True)
        .output
        == 1
    )


def test_search():
    assert (
        len(
            Chepy("loLolololoL")
            .regex_search("ol", ignore_case=True)
            .str_list_to_list()
            .o
        )
        == 5
    )
    assert (
        len(
            Chepy("loLolololoL")
            .regex_search(
                "ol",
                ignore_case=True,
                multiline=True,
                dotall=True,
                unicode=True,
                extended=True,
            )
            .str_list_to_list()
            .o
        )
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
    assert len(Chepy('["a", "a", 1]').str_list_to_list().unique().o) == 2


def test_sorted():
    assert Chepy(["a", "b", "1", "2"]).sorted().o == ["1", "2", "a", "b"]


def test_filter():
    assert Chepy('[{"a": 1}, {"b": 2}, {"a": 1, "b": 3}]').str_list_to_list().filter_by(
        "b"
    ).o == [{"b": 2}, {"a": 1, "b": 3}]


def test_slice():
    assert Chepy("some data").slice(3, 6).o == "e d"


def test_find_replace():
    assert Chepy("some some data").find_replace(r"some\s", "data").o == "datadatadata"


def test_escape_string():
    assert Chepy("$ome' d@ta").escape_string().o == "\\$ome'\\ d@ta"


def test_unescape_string():
    assert Chepy("\\$ome' d@ta").unescape_string().o == "$ome' d@ta"


def test_color_hex_to_rgb():
    assert Chepy("ffb4ad").color_hex_to_rgb().o == (255, 180, 173)


def test_diff():
    c = Chepy("a long sentence haha").save_buffer().to_upper_case(by="word")
    c.state += " hehe"
    c.find_replace("lo", "").diff(buffer=0)
    assert c.o == "{a->A} {-lo}ng {s->S}entence {h->H}aha{+ hehe}"
    d = (
        Chepy("a long sentence haha", "a long sentence haha")
        .save_buffer()
        .to_upper_case(by="word")
    )
    d.state += " hehe"
    d.find_replace("lo", "").diff(state=1)
    assert d.o == "{a->A} {-lo}ng {s->S}entence {h->H}aha{+ hehe}"

