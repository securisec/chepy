from chepy import Chepy


def test_search():
    assert Chepy("abcdefg123 and again abcdefg124").search(r"abc(de)fg(12)(\d)").o == [
        (b"de", b"12", b"3"),
        (b"de", b"12", b"4"),
    ]


def test_search_list():
    assert Chepy(
        ["InfoSeCon2023{1af5856c70878f8566085bc13849ef4d}", True, 123, ["a", "b"]]
    ).search_list("Info.+").o == [[b"InfoSeCon2023{1af5856c70878f8566085bc13849ef4d}"]]


def test_ctf_flags():
    assert (
        Chepy("tests/files/flags")
        .read_file()
        .search_ctf_flags("pico")
        .get_by_index(0)
        .o
        == b"picoCTF{r3source_pag3_f1ag}"
    )


def test_find_slack_tokenss():
    assert (
        Chepy("tests/files/flags").read_file().search_slack_tokens().get_by_index(0).o
        == b"xoxb-808882645436-350102357778-949755564313-1v9kucs6pv4o208oj4zh9sxqt76a5859"
    )


def test_search_private():
    assert len(Chepy("tests/files/flags").read_file().search_private_key().o) == 1


def test_slack_webhook():
    assert len(Chepy("tests/files/flags").read_file().search_slack_webhook().o) == 1


def test_twilio_key():
    assert len(Chepy("tests/files/flags").read_file().search_twilio_key().o) == 1


def test_aws_key():
    assert len(Chepy("tests/files/flags").read_file().search_aws_key().o) == 1
