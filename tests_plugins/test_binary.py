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


def test_pe_imports():
    assert (
        len(
            Chepy("tests/files/ff.exe")
            .read_file()
            .pe_imports()
            .get_by_key(b"api-ms-win-crt-filesystem-l1-1-0.dll", split_key=None)
            .o
        )
        == 2
    )


def test_pe_exports():
    assert len(Chepy("tests/files/ff.exe").read_file().pe_exports().o) == 94


def test_elf_imports():
    assert (
        len(
            Chepy("tests/files/elf").load_file().elf_imports().get_by_key(".rela.dyn",split_key=None).o
        )
        == 9
    )
