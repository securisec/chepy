from ..core import ChepyCore as ChepyCore, ChepyDecorators as ChepyDecorators
from typing import Any, TypeVar

RSA: Any
OpenSSL: Any
PublickeyT = TypeVar('PublickeyT', bound='Publickey')

class Publickey(ChepyCore):
    def __init__(self, *data: Any) -> None: ...
    state: Any = ...
    def parse_x509_pem(self) -> PublickeyT: ...
    def parse_x509_der_hex(self) -> PublickeyT: ...
    def public_from_x509(self) -> PublickeyT: ...
    def pem_to_der_hex(self) -> PublickeyT: ...
    def der_hex_to_pem(self) -> PublickeyT: ...
    def parse_public_pem(self) -> PublickeyT: ...
    def parse_private_pem(self) -> PublickeyT: ...
    def dump_pkcs12_cert(self, password: str) -> PublickeyT: ...
