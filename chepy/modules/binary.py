import pefile
from OpenSSL import crypto
from OpenSSL.crypto import _lib, _ffi, X509

from chepy.core import ChepyDecorators, ChepyCore


class PEFile(ChepyCore):
    def _pe_object(self, fast: bool = False):
        """Returns a pefile.PE instance
        
        Args:
            fast (bool, optional): If binary should be fast loaded. Defaults to False.
        """
        return pefile.PE(data=self._load_as_file().getvalue(), fast_load=fast)

    def pe_get_certificates(self):
        """Get certificates used to sign pe file
        
        Returns:
            Chepy: The Chepy object. 
        """

        def get_certificates(self): # pragma: no cover
            certs = _ffi.NULL
            if self.type_is_signed():
                certs = self._pkcs7.d.sign.cert
            elif self.type_is_signedAndEnveloped():
                certs = self._pkcs7.d.signed_and_enveloped.cert

            pycerts = []
            for i in range(_lib.sk_X509_num(certs)):
                pycert = X509.__new__(X509)
                pycert._x509 = _lib.sk_X509_value(certs, i)
                pycerts.append(pycert)

            if not pycerts:
                return None
            return tuple(pycerts)

        pe = self._pe_object()

        address = pe.OPTIONAL_HEADER.DATA_DIRECTORY[
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
        ].VirtualAddress
        size = pe.OPTIONAL_HEADER.DATA_DIRECTORY[
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
        ].Size

        hold = []
        if address == 0:  # pragma: no cover
            self._warning_logger("PE file is not signed")
            self.state = None
        else:
            signature = pe.write()[address + 8 :]

            pkcs = crypto.load_pkcs7_data(crypto.FILETYPE_ASN1, bytes(signature))
            certs = get_certificates(pkcs)

            for c in certs:
                dump_c = crypto.dump_certificate(crypto.FILETYPE_PEM, c)
                cert = crypto.load_certificate(crypto.FILETYPE_PEM, dump_c)
                issuer = cert.get_issuer()
                subject = cert.get_subject()
                pubkey = cert.get_pubkey()
                bio = crypto._new_mem_buf()
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
                hold.append(info)

        self.state = hold
        return self

