import binascii
import string
import base64
import base58
import re
from typing import Any

from ..core import Core


class DataFormat(Core):
    
    def base_58_encode(self) -> "Chepy":
        """
        Base58 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property encodes raw data 
        into an ASCII Base58 string.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = base58.b58encode(self._convert_to_bytes())
        return self

    
    def base_58_decode(self) -> "Chepy":
        """
        Base58 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base58 string.
        
        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = base58.b58decode(self._holder)
        return self

    
    def base_64_encode(self) -> "Chepy":
        """Base64 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property encodes raw data 
        into an ASCII Base64 string.
        
        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = base64.b64encode(self._convert_to_bytes())
        return self

    
    def base_64_decode(self) -> "Chepy":
        """Base64 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base64 string.
        
        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = base64.b64decode(self._holder)
        return self

    
    def base_32_encode(self) -> "Chepy":
        self._holder = base64.b32encode(self._convert_to_bytes())
        return self

    
    def base_32_decode(self) -> "Chepy":
        self._holder = base64.b32decode(self._holder)
        return self

    
    def string_from_hexdump(self) -> "Chepy":
        if self._is_bytes():
            data = self._holder.decode()
        else:
            data = self._holder
        self._holder = "".join(re.findall(r"\|(.+)\|", data))
        return self

    
    def to_hex(self) -> "Chepy":
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    
    def hex_to_int(self) -> "Chepy":
        if self._holder.startswith("0x"):
            self._holder = int(self._holder, 0)
        else:
            self._holder = int(self._remove_spaces(), 16)
        return self
