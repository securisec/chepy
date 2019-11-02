from pathlib import Path
from chepy import Chepy

path = str(Path().absolute() / "tests/files/test.pem")


def test_parse_pem():
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

