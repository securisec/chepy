from pathlib import Path
from chepy import Chepy

path = str(Path().absolute() / "tests/files/test.pem")


def test_parse_x509_pem():
    assert Chepy(path, True).parse_x509_pem().o == {
        "version": 0,
        "serial": 16349711528102141469,
        "algo": b"sha256WithRSAEncryption",
        "before": b"20191102152508Z",
        "after": b"20201101152508Z",
        "issuer": {
            "C": "US",
            "ST": "lol",
            "L": "nyc",
            "O": "securisec",
            "OU": "coder",
            "CN": "securisec",
            "email": "none@email.com",
        },
        "subject": {
            "C": "US",
            "ST": "lol",
            "L": "nyc",
            "O": "securisec",
            "OU": "coder",
            "CN": "securisec",
            "email": "none@email.com",
        },
        "pubkey": {"bits": 1024},
    }


def test_parse_x509_der_hex():
    assert Chepy(
        str(Path().absolute() / "tests/files/test.der"), True
    ).parse_x509_der_hex().o == {
        "version": 0,
        "serial": 16349711528102141469,
        "algo": b"sha256WithRSAEncryption",
        "before": b"20191102152508Z",
        "after": b"20201101152508Z",
        "issuer": {
            "C": "US",
            "ST": "lol",
            "L": "nyc",
            "O": "securisec",
            "OU": "coder",
            "CN": "securisec",
            "email": "none@email.com",
        },
        "subject": {
            "C": "US",
            "ST": "lol",
            "L": "nyc",
            "O": "securisec",
            "OU": "coder",
            "CN": "securisec",
            "email": "none@email.com",
        },
        "pubkey": {"bits": 1024},
    }


def test_pem_to_der():
    assert Chepy(path, True).pem_to_der_hex().to_hex().o.decode()[0:6] == "308202"

