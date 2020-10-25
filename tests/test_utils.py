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
    assert len(Chepy("some lol random lolol data").split_by("lo", trim=False).o) == 4


def test_split_by_n():
    assert Chepy("some string").split_by_n(2).o[2] == " s"


def test_select_n():
    assert Chepy(["a", 1, "lol", "", True]).select_every_n(3).o == ["a", ""]


def test_unique():
    assert len(Chepy('["a", "a", 1]').str_list_to_list().unique().o) == 2


def test_sorted_list():
    assert Chepy(["a", "b", "1", "2"]).sort_list().o == ["1", "2", "a", "b"]
    assert Chepy(["a", "b", "1", "2"]).sort_list(reverse=True).o == ["b", "a", "2", "1"]


def test_sort_dict_key():
    assert Chepy(
        {"z": "string", "a": True, "zz": 1, "aaa": {"bb": "data"}, "ccc": [1, "a"]}
    ).sort_dict_key().o == {
        "a": True,
        "aaa": {"bb": "data"},
        "ccc": [1, "a"],
        "z": "string",
        "zz": 1,
    }
    assert Chepy(
        {"z": "string", "a": True, "zz": 1, "aaa": {"bb": "data"}, "ccc": [1, "a"]}
    ).sort_dict_key(reverse=True).o == {
        "zz": 1,
        "z": "string",
        "ccc": [1, "a"],
        "aaa": {"bb": "data"},
        "a": True,
    }


def test_sort_dict_value():
    assert Chepy(
        {"z": "string", "a": "True", "zz": "1", "aaa": {"bb": "data"}, "ccc": [1, "a"]}
    ).sort_dict_value().o == {
        "zz": "1",
        "a": "True",
        "ccc": [1, "a"],
        "z": "string",
        "aaa": {"bb": "data"},
    }
    assert Chepy({"a": 2, "b": 1}).sort_dict_value().o == {"b": 1, "a": 2}


def test_filter_list():
    assert Chepy(
        '[{"a": 1}, {"b": 2}, {"a": 1, "b": 3}]'
    ).str_list_to_list().filter_list("b", False).o == [{"b": 2}, {"a": 1, "b": 3}]
    assert Chepy(["a", "aa", "bb"]).filter_list("aa?").o == ["a", "aa"]
    assert Chepy([b"a", b"aa", b"bb"]).filter_list("aa?").o == [b"a", b"aa"]
    assert Chepy([b"a", b"aa", b"bb"]).filter_list("b+").o == b"bb"


def test_filter_dict_key():
    assert Chepy({"some": "dict", "another": "val"}).filter_dict_key("ano").o == {
        "another": "val"
    }


def test_filter_dict_value():
    assert Chepy({b"some": b"dict", b"another": "val"}).filter_dict_value("val").o == {
        b"another": "val"
    }


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


def test_pad():
    assert Chepy("lol").pad(7, char="a").o == "lola"
    assert Chepy("lol").pad(7, direction="right", char="a").o == "alol"


def test_count():
    assert Chepy("some text").count().get_by_key("t").o == 2


def test_set():
    assert len(Chepy("some text").set().o) == 7


def test_filter_list_by_length():
    assert len(Chepy([1, 2, 33, 444]).filter_list_by_length(2).o) == 2
    assert len(Chepy([1, 2, 33, 444]).filter_list_by_length(2, True).o) == 1


def test_regex_to_str():
    assert len(Chepy("lol([a-c])").regex_to_str().o) == 4
    assert len(Chepy("lol([a-c])").regex_to_str(all_combo=True).o) == 3

