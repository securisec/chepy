from chepy import Chepy


def test_pe_get_certs():
    assert (
        Chepy("tests/files/ff.exe")
        .read_file()
        .pe_get_certificates()
        .get_by_index(0)
        .get_by_key("serial")
        .o
        == 17154717934120587862167794914071425081
    )

