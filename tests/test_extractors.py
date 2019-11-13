from pathlib import Path
from chepy import Chepy


def test_extract_strings():
    assert len(Chepy("tests/files/hello").load_file().extract_strings().o) == 29


def test_extract_ips():
    assert len(Chepy("127.0.0.1\n::80").extract_ips().o) == 2


def test_extract_email():
    assert len(Chepy("tests/files/test.der").load_file().extract_email().o) == 2
