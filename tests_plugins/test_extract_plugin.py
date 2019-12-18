from chepy import Chepy


def test_extract_common_secrets():
    assert (
        len(
            Chepy("tests/files/vuln_code")
            .load_file()
            .extract_common_secrets()
            .get_by_key("KEY")
            .o
        )
        == 6
    )
