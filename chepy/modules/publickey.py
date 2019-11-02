from OpenSSL import crypto as _pyssl_crypto
from OpenSSL._util import lib as _pyssl_cryptolib
from ..core import Core


class Publickey(Core):
    def parse_x509_pem(self) -> dict:
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
