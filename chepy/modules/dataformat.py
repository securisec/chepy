import string
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

    def string_from_hexdump(self) -> "Baked":
        if self._is_bytes():
            data = self._holder.decode()
        else:
            data = self._holder
        self._holder = "".join(re.findall(r"\|(.+)\|", data))
        return self
