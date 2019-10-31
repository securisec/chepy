import string
import binascii
import base64
import base58
import regex as re
from typing import Any

from ..core import Core


class DataFormat(Core):
    def base_58_encode(self) -> "Baked":
        """
        Base58 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property encodes raw data 
        into an ASCII Base58 string.

        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = base58.b58encode(self._convert_to_bytes())
        return self

    def base_58_decode(self) -> "Baked":
        """
        Base58 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base58 string.
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = base58.b58decode(self._holder)
        return self

    def base_32_encode(self) -> "Baked":
        self._holder = base64.b32encode(self._convert_to_bytes())
        return self

    def base_32_decode(self) -> "Baked":
        self._holder = base64.b32decode(self._holder)
        return self

    def to_int(self):
        self._holder = int(self._holder)
        return self

    def base_64_encode(self) -> "Baked":
        """Base64 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property encodes raw data 
        into an ASCII Base64 string.
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = base64.b64encode(self._convert_to_bytes())
        return self

    def base_64_decode(self) -> "Baked":
        """Base64 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base64 string.
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = base64.b64decode(self._holder)
        return self

    def to_hex(self) -> "Baked":
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    def hex_to_int(self) -> "Baked":
        if self._convert_to_str().startswith("0x"):
            self._holder = int(self._holder, 0)
        else:
            self._holder = int(self._remove_spaces(), 16)
        return self

    def hex_to_binary(self):
        self._holder = binascii.unhexlify(self._convert_to_bytes())
        return self

    def hex_to_str(self, ignore=False) -> "Baked":
        if ignore:
            self._holder = binascii.unhexlify(self._convert_to_bytes()).decode(
                errors="ignore"
            )
        else:
            self._holder = binascii.unhexlify(self._convert_to_bytes())
        return self

    def str_to_hex(self) -> "Baked":
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    def int_to_hex(self):
        self._holder = format(self._convert_to_int(), "x")
        return self

    def binary_to_hex(self):
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    def normalize_hex(self):
        assert r"\x" not in self._holder, "Cannot normalize binary data"
        delimiters = [" ", "0x", "%", ",", ";", ":", r"\\n", "\\r\\n"]
        string = re.sub("|".join(delimiters), "", self._holder)
        assert re.search(r"^[a-fA-F0-9]+$", string) is not None, "Invalid hex"
        self._holder = string
        return self

    def string_from_hexdump(self) -> "Baked":
        if self._is_bytes():
            data = self._holder.decode()
        else:
            data = self._holder
        self._holder = "".join(re.findall(r"\|(.+)\|", data))
        return self
