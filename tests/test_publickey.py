from pathlib import Path
from chepy import Chepy

path = str(Path().absolute() / "tests/files/test.pem")


def test_parse_x509_pem():
    assert Chepy(path).load_file().parse_x509_pem().o == {
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
        str(Path().absolute() / "tests/files/test.der")
    ).load_file().parse_x509_der_hex().o == {
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
    assert Chepy(path).load_file().pem_to_der_hex().to_hex().o.decode()[0:6] == "308202"


def test_der_hex_to_pem():
    assert (
        Chepy(str(Path().absolute() / "tests/files/test.der"))
        .load_file()
        .der_hex_to_pem()
        .o.decode()
        == """-----BEGIN CERTIFICATE-----
MIICeTCCAeICCQDi5dgCpKMeHTANBgkqhkiG9w0BAQsFADCBgDELMAkGA1UEBhMC
VVMxDDAKBgNVBAgMA2xvbDEMMAoGA1UEBwwDbnljMRIwEAYDVQQKDAlzZWN1cmlz
ZWMxDjAMBgNVBAsMBWNvZGVyMRIwEAYDVQQDDAlzZWN1cmlzZWMxHTAbBgkqhkiG
9w0BCQEWDm5vbmVAZW1haWwuY29tMB4XDTE5MTEwMjE1MjUwOFoXDTIwMTEwMTE1
MjUwOFowgYAxCzAJBgNVBAYTAlVTMQwwCgYDVQQIDANsb2wxDDAKBgNVBAcMA255
YzESMBAGA1UECgwJc2VjdXJpc2VjMQ4wDAYDVQQLDAVjb2RlcjESMBAGA1UEAwwJ
c2VjdXJpc2VjMR0wGwYJKoZIhvcNAQkBFg5ub25lQGVtYWlsLmNvbTCBnzANBgkq
hkiG9w0BAQEFAAOBjQAwgYkCgYEA1L6ceV3tvkHtMHI5vOwr+cjW/H0yINh9PYHy
+CS9MmrX12pe/m1FLapMUu5HgQZAKrtldccb3WiGQNprs/Wce1g8hmvD0pAXffij
Q+vjvHVU3l+up1ocL6IPpxrQVz0bzpQ4sMRK0CdZgjf4y4HL188qMNgYGOZBgttF
Xxoz41UCAwEAATANBgkqhkiG9w0BAQsFAAOBgQChhviBdift0P/j00TYxnPPNS58
wQSFm54UNQ/vjM12yZ+C5c3268Vo8jSP7mI5R3wn6XztjUSXkDg5/3IL3kojti/h
nyhBHx2QCVke7BxWw3HWkbZ/1BKl0HnCGyd5HDTuOtlBmTS+QrJoNpdsn0zq4fvc
igbV1IJdKTBAiZzaOQ==
-----END CERTIFICATE-----
"""
    )


def test_parse_public():
    assert (
        Chepy("tests/files/public.pem").load_file().parse_public_pem().get_by_key("e").o
        == 65537
    )


def test_parse_private():
    assert (
        Chepy("tests/files/private.pem")
        .load_file()
        .parse_private_pem()
        .get_by_key("p")
        .o
        == 12567061504848007717323266435513666403545525206525105210732583342352560503165028238964437465562703567713719610893680829859726382850796095548144718531640607
    )

