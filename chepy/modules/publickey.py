from OpenSSL import crypto as _pyssl_crypto
from OpenSSL._util import lib as _pyssl_cryptolib
from Crypto.PublicKey import RSA

from ..core import ChepyCore


class Publickey(ChepyCore):
    def parse_x509_pem(self):
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
        cert = _pyssl_crypto.load_certificate(
            _pyssl_crypto.FILETYPE_PEM, self._convert_to_str()
        )
        issuer = cert.get_issuer()
        subject = cert.get_subject()
        pubkey = cert.get_pubkey()
        bio = _pyssl_crypto._new_mem_buf()
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
        self.state = info
        return self

    def parse_x509_der_hex(self):
        """Parse X509 cert in DER format
        
        X.509 is an ITU-T standard for a public key infrastructure (PKI) 
        and Privilege Management Infrastructure (PMI). It is commonly involved 
        with SSL/TLS security.<br><br>This operation displays the contents of 
        a certificate in a human readable format, similar to the openssl command line tool.
        
        Returns:
            Chepy: A Chepy object. 
        """
        cert = _pyssl_crypto.load_certificate(
            _pyssl_crypto.FILETYPE_ASN1, self._convert_to_bytes()
        )
        issuer = cert.get_issuer()
        subject = cert.get_subject()
        pubkey = cert.get_pubkey()
        bio = _pyssl_crypto._new_mem_buf()
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
        self.state = info
        return self

    def public_from_x509(self):
        """Get public key from x509 certificate
        
        Returns:
            Chepy: The Chepy object. 
        """
        crtObj = _pyssl_crypto.load_certificate(_pyssl_crypto.FILETYPE_PEM, self.state)
        pubKeyObject = crtObj.get_pubkey()
        pubKeyString = _pyssl_crypto.dump_publickey(
            _pyssl_crypto.FILETYPE_PEM, pubKeyObject
        )
        self.state = pubKeyString
        return self

    def pem_to_der_hex(self):
        """Convert PEM cert to DER format
        
        Converts PEM (Privacy Enhanced Mail) format to a hexadecimal 
        DER (Distinguished Encoding Rules) string.
        
        Returns:
            Chepy: The Chepy object.
        """
        cert_pem = _pyssl_crypto.load_certificate(
            _pyssl_crypto.FILETYPE_PEM, self.state
        )
        self.state = _pyssl_crypto.dump_certificate(
            _pyssl_crypto.FILETYPE_ASN1, cert_pem
        )
        return self

    def der_hex_to_pem(self):
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
        cert_pem = _pyssl_crypto.load_certificate(
            _pyssl_crypto.FILETYPE_ASN1, self._convert_to_bytes()
        )
        self.state = _pyssl_crypto.dump_certificate(
            _pyssl_crypto.FILETYPE_PEM, cert_pem
        )
        return self

    def parse_public_pem(self):
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

    def parse_private_pem(self):
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
