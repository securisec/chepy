import pefile
import elftools.elf.elffile as _pyelf
from elftools.elf.relocation import RelocationSection
from OpenSSL import crypto
from OpenSSL.crypto import _lib, _ffi, X509

from chepy.core import ChepyDecorators, ChepyCore


class PEFile(ChepyCore):
    def _pe_object(self, fast: bool = True):
        """Returns a pefile.PE instance
        
        Args:
            fast (bool, optional): If binary should be fast loaded. Defaults to False.
        """
        return pefile.PE(data=self._load_as_file().getvalue(), fast_load=fast)

    @ChepyDecorators.call_stack
    def pe_get_certificates(self):
        """Get certificates used to sign pe file
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("tests/files/ff.exe).read_file().pe_get_certificates().o
            [
                {
                    'version': 2,
                    'serial': 17154717934120587862167794914071425081,
                    'algo': b'sha1WithRSAEncryption',
                    'before': b'20061110000000Z',
                    'after': b'20311110000000Z',
                    'issuer': {
                        'C': 'US',
                        'ST': None,
                        'L': None,
                        'O': 'DigiCert Inc',
                        'OU': 'www.digicert.com',
                        'CN': 'DigiCert Assured ID Root CA',
                        'email': None
                    },
                    ...
                ...
            }
        """

        def get_certificates(self):  # pragma: no cover
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

    @ChepyDecorators.call_stack
    def pe_imports(self):
        """Get all the imports from a PE file
        
        Returns:
            Chepy: The Chepy object. 
        """
        pe = self._pe_object()
        pe.parse_data_directories()

        hold = {}

        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            hold[entry.dll] = {imp.name: hex(imp.address) for imp in entry.imports}

        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def pe_exports(self):
        """Get all the exports from a PE file
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("tests/files/ff.exe").read_file().pe_exports().o
               {
                    b'KERNEL32.dll': {
                        b'AcquireSRWLockExclusive': '0x140051ff8',
                        b'AssignProcessToJobObject': '0x140052000',
                        b'AttachConsole': '0x140052008',
                        ...
                    b'ntdll.dll': {
                        ...
                    }
                }
        """
        pe = self._pe_object()
        pe.parse_data_directories()

        hold = {}

        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            hold[exp.name] = hex(pe.OPTIONAL_HEADER.ImageBase + exp.address)

        self.state = hold
        return self


class ELFFile(ChepyCore):
    def _elf_object(self):
        """Returns an ELFFile object
        """
        return _pyelf.ELFFile(self._load_as_file())

    @ChepyDecorators.call_stack
    def elf_imports(self):
        """Get imports from an ELF file
        
        Returns:
            Chepy: The Chepy object. 
        """
        hold = {}
        e = self._elf_object()
        for section in e.iter_sections():
            if isinstance(section, RelocationSection):
                symbol_table = e.get_section(section["sh_link"])
                symbols = []
                for relocation in section.iter_relocations():
                    symbol = symbol_table.get_symbol(relocation["r_info_sym"]).name
                    if symbol:
                        symbols.append(symbol)
                hold[section.name] = symbols

        self.state = hold
        return self
