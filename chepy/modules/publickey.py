from OpenSSL import crypto as _pyssl_crypto
from OpenSSL._util import lib as _pyssl_cryptolib
from ..core import Core


class Publickey(Core):
    def parse_x509_pem(self):
        """X.509 is an ITU-T standard for a public key infrastructure (PKI) 
        and Privilege Management Infrastructure (PMI). It is commonly involved 
        with SSL/TLS security.<br><br>This operation displays the contents of 
        a certificate in a human readable format, similar to the openssl command line tool.
        
        Returns
        -------
        Chepy
            A Chepy object. 
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
        self._holder = info
        return self

    def parse_x509_der_hex(self):
        """X.509 is an ITU-T standard for a public key infrastructure (PKI) 
        and Privilege Management Infrastructure (PMI). It is commonly involved 
        with SSL/TLS security.<br><br>This operation displays the contents of 
        a certificate in a human readable format, similar to the openssl command line tool.
        
        Returns
        -------
        Chepy
            A Chepy object. 
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
        self._holder = info
        return self

    def pem_to_der_hex(self):
        """Converts PEM (Privacy Enhanced Mail) format to a hexadecimal 
        DER (Distinguished Encoding Rules) string.
        
        Returns
        -------
        Chepy
            The Chepy object.
        """
        cert_pem = _pyssl_crypto.load_certificate(
            _pyssl_crypto.FILETYPE_PEM, self._holder
        )
        self._holder = _pyssl_crypto.dump_certificate(
            _pyssl_crypto.FILETYPE_ASN1, cert_pem
        )
        return self
