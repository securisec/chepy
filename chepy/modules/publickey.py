from typing import Literal, TypeVar

import lazy_import

RSA = lazy_import.lazy_module("Crypto.PublicKey.RSA")
ECC = lazy_import.lazy_module("Crypto.PublicKey.ECC")
OpenSSL = lazy_import.lazy_module("OpenSSL")

from ..core import ChepyCore, ChepyDecorators

PublickeyT = TypeVar("PublickeyT", bound="Publickey")


class Publickey(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    def _convert_cert_to_obj(self, cert):
        issuer = cert.get_issuer()
        subject = cert.get_subject()
        pubkey = cert.get_pubkey()
        info = {
            "version": cert.get_version(),
            "serial": cert.get_serial_number(),
            "algo": cert.get_signature_algorithm(),
            "before": cert.get_notBefore(),
            "after": cert.get_notAfter(),
            "issuer": {
                "C": issuer.C,
                "ST": issuer.ST,
                "L": issuer.L,
                "O": issuer.O,
                "OU": issuer.OU,
                "CN": issuer.CN,
                "email": issuer.emailAddress,
            },
            "subject": {
                "C": subject.C,
                "ST": subject.ST,
                "L": subject.L,
                "O": subject.O,
                "OU": subject.OU,
                "CN": subject.CN,
                "email": subject.emailAddress,
            },
            "pubkey": {"bits": pubkey.bits()},
        }
        return info

    @ChepyDecorators.call_stack
    def parse_x509_pem(self) -> PublickeyT:
        """Parse X509 cert in PEM format

        X.509 is an ITU-T standard for a public key infrastructure (PKI)
        and Privilege Management Infrastructure (PMI). It is commonly involved
        with SSL/TLS security. This operation displays the contents of
        a certificate in a human readable format, similar to the openssl command line tool.

        Returns:
            Chepy: A Chepy object.

        Examples:
            >>> Chepy(path).load_file().parse_x509_pem().o
            {
                "version": 0,
                ...
                "after": b"20201101152508Z",
                "issuer": {
                    "C": "US",
                    ...
                    "email": "none@email.com",
                },
                "subject": {
                    "C": "US",
                    ...
                    "email": "none@email.com",
                },
                "pubkey": {"bits": 1024},
            }
        """
        cert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, self._convert_to_str()
        )
        info = self._convert_cert_to_obj(cert)
        self.state = info
        return self

    @ChepyDecorators.call_stack
    def parse_x509_der_hex(self) -> PublickeyT:
        """Parse X509 cert in DER format

        X.509 is an ITU-T standard for a public key infrastructure (PKI)
        and Privilege Management Infrastructure (PMI). It is commonly involved
        with SSL/TLS security.<br><br>This operation displays the contents of
        a certificate in a human readable format, similar to the openssl command line tool.

        Returns:
            Chepy: A Chepy object.
        """
        cert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_ASN1, self._convert_to_bytes()
        )
        info = self._convert_cert_to_obj(cert)
        self.state = info
        return self

    @ChepyDecorators.call_stack
    def public_from_x509(self) -> PublickeyT:
        """Get public key from x509 certificate

        Returns:
            Chepy: The Chepy object.
        """
        crt_obj = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, self.state
        )
        pub_key_object = crt_obj.get_pubkey()
        pub_key_string = OpenSSL.crypto.dump_publickey(
            OpenSSL.crypto.FILETYPE_PEM, pub_key_object
        )
        self.state = pub_key_string
        return self

    @ChepyDecorators.call_stack
    def pem_to_der_hex(self) -> PublickeyT:
        """Convert PEM cert to DER format

        Converts PEM (Privacy Enhanced Mail) format to a hexadecimal
        DER (Distinguished Encoding Rules) string.

        Returns:
            Chepy: The Chepy object.
        """
        cert_pem = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, self.state
        )
        self.state = OpenSSL.crypto.dump_certificate(
            OpenSSL.crypto.FILETYPE_ASN1, cert_pem
        )
        return self

    @ChepyDecorators.call_stack
    def der_hex_to_pem(self) -> PublickeyT:
        """Convert DER format to PEM cert.

        Converts a hexadecimal DER (Distinguished Encoding Rules)
        string into PEM (Privacy Enhanced Mail) format.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy(str(Path().absolute() / "tests/files/test.der"))
            >>> c.load_file()
            >>> c.der_hex_to_pem()
            >>> c.o.decode()
            -----BEGIN CERTIFICATE-----
            MIICeTCCAeICCQDi5dgCpKMeHTANBgkqhkiG9w0BAQsFADCBgDELMAkGA1UEBhMC
            VVMxDDAKBgNVBAgMA2xvbDEMMAoGA1UEBwwDbnljMRIwEAYDVQQKDAlzZWN1cmlz
            ...
            wQSFm54UNQ/vjM12yZ+C5c3268Vo8jSP7mI5R3wn6XztjUSXkDg5/3IL3kojti/h
            nyhBHx2QCVke7BxWw3HWkbZ/1BKl0HnCGyd5HDTuOtlBmTS+QrJoNpdsn0zq4fvc
            igbV1IJdKTBAiZzaOQ==
            -----END CERTIFICATE-----
        """
        cert_pem = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_ASN1, self._convert_to_bytes()
        )
        self.state = OpenSSL.crypto.dump_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert_pem
        )
        return self

    @ChepyDecorators.call_stack
    def parse_public_pem(self) -> PublickeyT:
        """Parse pubkey PEM to get n and e

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("tests/files/public.pem").load_file().parse_public_pem().get_by_key("e").o
            65537
        """
        key = RSA.importKey(self.state)
        self.state = {"n": key.n, "e": key.e}
        return self

    @ChepyDecorators.call_stack
    def parse_private_pem(self) -> PublickeyT:
        """Parse private key PEM

        Returns:
            Chepy: The Chepy object.
        """
        key = RSA.importKey(self.state)
        self.state = {
            "d": key.d,
            "e": key.e,
            "n": key.n,
            "p": key.p,
            "q": key.q,
            "u": key.u,
        }
        return self

    @ChepyDecorators.call_stack
    def dump_pkcs12_cert(self, password: str) -> PublickeyT:
        """Get the private key and cert from pkcs12 cert

        Args:
            password (str): Password for certificate

        Returns:
            Chepy: The Chepy object.
        """
        if isinstance(password, str):
            password = password.encode()
        pk12 = OpenSSL.crypto.load_pkcs12(self._convert_to_bytes(), password)
        self.state = {
            "private": OpenSSL.crypto.dump_privatekey(
                OpenSSL.crypto.FILETYPE_PEM, pk12.get_privatekey()
            ),
            "cert": OpenSSL.crypto.dump_certificate(
                OpenSSL.crypto.FILETYPE_PEM, pk12.get_certificate()
            ),
        }
        return self

    @ChepyDecorators.call_stack
    def generate_rsa_keypair(
        self,
        bits: int = 1024,
        format: Literal["PEM", "DER"] = "PEM",
        passphrase: str = None,
    ) -> PublickeyT:
        """Generate RSA key pair

        Args:
            bits (int, optional): Length of keys. Defaults to 1024.
            format (Literal[, optional): Output format type. Defaults to 'PEM'.
            passphrase (str, optional): Passphrase for keys. Defaults to None.

        Returns:
            Chepy: The Chepy object.
        """
        key = RSA.generate(bits)
        pub = key.public_key().exportKey(passphrase=passphrase, format=format)
        priv = key.exportKey(passphrase=passphrase, format=format)
        self.state = {"public": pub, "private": priv}
        return self

    @ChepyDecorators.call_stack
    def generate_ecc_keypair(
        self,
        curve: Literal['p256', 'p384', 'p521'] = 'p256',
        format: Literal["PEM", "DER"] = "PEM"
    ) -> PublickeyT:
        """Generate RSA key pair

        Args:
            curve (Literal[, optional): Curve for keys. Defaults to p256.
            format (Literal[, optional): Output format type. Defaults to 'PEM'.

        Returns:
            Chepy: The Chepy object.
        """
        key = ECC.generate(curve=curve)
        pub = key.public_key().export_key(format=format)
        priv = key.export_key(format=format)
        self.state = {"public": pub, "private": priv}
        return self
