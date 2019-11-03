import string
import binascii
import base64
import base58
import regex as re
from urllib.parse import quote_plus as _urllib_quote_plus
from urllib.parse import unquote_plus as _urllib_unquote_plus
from typing import Any

from ..core import Core


class DataFormat(Core):
    def list_to_str(self, join_by=" "):
        """Join an array by `join_by`
        
        Parameters
        ----------
        join_by : str, optional
            String character to join by, by default ' '
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = join_by.join(self._holder)
        return self

    def base_58_encode(self) -> "Baked":
        """Base58 is a notation for encoding arbitrary byte data using a 
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
        """Base58 is a notation for encoding arbitrary byte data using a 
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
        """ Base32 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers. It uses a smaller set of characters than 
        Base64, usually the uppercase alphabet and the numbers 2 to 7.
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = base64.b32encode(self._convert_to_bytes())
        return self

    def base_32_decode(self) -> "Baked":
        """ Base32 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers. It uses a smaller set of characters than 
        Base64, usually the uppercase alphabet and the numbers 2 to 7.
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = base64.b32decode(self._holder)
        return self

    def to_int(self) -> "Baked":
        """Converts the string representation of a number into an int
        
        Returns
        -------
        Baked
            The Baked object.
        """
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
        """Converts a string to its hex representation
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    def hex_to_int(self) -> "Baked":
        """Converts hex into its intiger represantation
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        if self._convert_to_str().startswith("0x"):
            self._holder = int(self._holder, 0)
        else:
            self._holder = int(self._remove_spaces(), 16)
        return self

    def hex_to_binary(self):
        """Converts a hex string to its binary form. Example: 
        41 becomes \\x41
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = binascii.unhexlify(self._convert_to_bytes())
        return self

    def hex_to_str(self, ignore: bool = False) -> "Baked":
        """Decodes a hex string to ascii ignoring any decoding errors
        
        Parameters
        ----------
        ignore : bool, optional
            Ignore errors, by default False
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        if ignore:
            self._holder = binascii.unhexlify(self._convert_to_bytes()).decode(
                errors="ignore"
            )
        else:
            self._holder = binascii.unhexlify(self._convert_to_bytes())
        return self

    def str_to_hex(self) -> "Baked":
        """Converts a string to a hex string
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    def int_to_hex(self):
        """Converts an integer into its hex equivalent
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = format(self._convert_to_int(), "x")
        return self

    def binary_to_hex(self):
        """Converts binary data into a hex string
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    def normalize_hex(self):
        """Removes special encoding characters from a hex string like %, 
        0x, , :, ;, \\n and \\r\\n
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        assert r"\x" not in self._holder, "Cannot normalize binary data"
        delimiters = [" ", "0x", "%", ",", ";", ":", r"\\n", "\\r\\n"]
        string = re.sub("|".join(delimiters), "", self._holder)
        assert re.search(r"^[a-fA-F0-9]+$", string) is not None, "Invalid hex"
        self._holder = string
        return self

    def string_from_hexdump(self) -> "Baked":
        # TODO make new line aware \n \r\n \0a etc
        if self._is_bytes():
            data = self._holder.decode()
        else:
            data = self._holder
        self._holder = "".join(re.findall(r"\|(.+)\|", data))
        return self

    def url_encode(self, safe: str = ""):
        """Encodes problematic characters into percent-encoding, 
        a format supported by URIs/URLs.
        
        Parameters
        ----------
        safe : str, optional
            String of characters that will not be encoded, by default ""
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = _urllib_quote_plus(self._convert_to_str(), safe=safe)
        return self

    def url_decode(self) -> "Baked":
        """Converts URI/URL percent-encoded characters back to their raw values.
        
        Returns
        -------
        Baked
            A Baked object.
        """
        self._holder = _urllib_unquote_plus(self._convert_to_str())
        return self
