import binascii
import string
import base64
import re
from typing import Any

from ..core import Core


class DataFormat(Core):
    @property
    def base_32_encode(self) -> "Chepy":
        self._holder = base64.b32encode(self._convert_to_bytes())
        return self

    @property
    def base_64_encode(self) -> "Chepy":
        self._holder = base64.b64encode(self._convert_to_bytes())
        return self

    @property
    def base_32_decode(self) -> "Chepy":
        self._holder = base64.b32decode(self._holder)
        return self

    @property
    def base_64_decode(self) -> "Chepy":
        self._holder = base64.b64decode(self._holder)
        return self

    @property
    def string_from_hexdump(self) -> "Chepy":
        if self._is_bytes():
            data = self._holder.decode()
        else:
            data = self._holder
        self._holder = "".join(re.findall(r"\|(.+)\|", data))
        return self

    @property
    def to_hex(self) -> "Chepy":
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    @property
    def hex_to_int(self) -> "Chepy":
        if self._holder.startswith("0x"):
            self._holder = int(self._holder, 0)
        else:
            self._holder = int(self._remove_spaces(), 16)
        return self
