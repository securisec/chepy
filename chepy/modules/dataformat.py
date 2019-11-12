import string
import binascii
import base64
import base58
import json
import yaml
import regex as re
from urllib.parse import quote_plus as _urllib_quote_plus
from urllib.parse import unquote_plus as _urllib_unquote_plus
from typing import Any

from ..core import Core


class DataFormat(Core):
    def list_to_str(self, join_by=" "):
        """Join an array by `join_by`
        
        Args:
            join_by (str, optional): String character to join by, by default ' '
        
        Returns:
            Chepy: The Chepy object. 
        """
        assert isinstance(self.state, list), "Data in state not a list"
        self.state = join_by.join(self.state)
        return self

    def str_to_list(self):
        """Convert a string list to a list
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = json.loads(re.sub(r"'", '"', self._convert_to_str()))
        return self

    def json_to_dict(self):
        """Convert a JSON string to a dict object
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = json.loads(self._convert_to_str())
        return self

    def dict_to_json(self):
        """Convert a dict object to a JSON string
        
        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, dict), "Not a dict object"
        self.state = json.dumps(self.state)
        return self

    def yaml_to_json(self):
        """Convert yaml to a json string
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = json.dumps(yaml.safe_load(self.state))
        return self

    def json_to_yaml(self):
        """Convert a json string to yaml structure
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = yaml.dump(
            json.loads(self.state),
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
        return self

    def base_58_encode(self):
        """Encode as Base58
        
        Base58 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property encodes raw data 
        into an ASCII Base58 string.

        Returns:
            Chepy: The Chepy object. 
        """
        self.state = base58.b58encode(self._convert_to_bytes())
        return self

    def base_58_decode(self):
        """Decode as Base58
        
        Base58 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base58 string.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = base58.b58decode(self.state)
        return self

    def base_85_encode(self):
        """Encode as Base58

        Base85 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base58 string.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = base64.a85encode(self._convert_to_bytes())
        return self

    def base_85_decode(self):
        """Decode as Base85

        Base85 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base58 string.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = base64.a85decode(self._convert_to_bytes())
        return self

    def base_32_encode(self):
        """Encode as Base32
        
        Base32 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers. It uses a smaller set of characters than 
        Base64, usually the uppercase alphabet and the numbers 2 to 7.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = base64.b32encode(self._convert_to_bytes())
        return self

    def base_32_decode(self):
        """Decode as Base32
        
        Base32 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers. It uses a smaller set of characters than 
        Base64, usually the uppercase alphabet and the numbers 2 to 7.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = base64.b32decode(self.state)
        return self

    def to_int(self):
        """Converts the string representation of a number into an int
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = int(self.state)
        return self

    def base_64_encode(self):
        """Encode as Base64
        
        Base64 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property encodes raw data 
        into an ASCII Base64 string.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = base64.b64encode(self._convert_to_bytes())
        return self

    def base_64_decode(self):
        """Decode as Base64
        
        Base64 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base64 string.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = base64.b64decode(self.state)
        return self

    def to_hex(self):
        """Converts a string to its hex representation
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = binascii.hexlify(self._convert_to_bytes())
        return self

    def hex_to_int(self):
        """Converts hex into its intiger represantation
        
        Returns:
            Chepy: The Chepy object. 
        """
        if self._convert_to_str().startswith("0x"):
            self.state = int(self.state, 0)
        else:
            self.state = int(self.state, 16)
        return self

    def hex_to_binary(self):
        """Hex to binary hex
        
        Converts a hex string to its binary form. Example: 
        41 becomes \\x41
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = binascii.unhexlify(self._convert_to_bytes())
        return self

    def hex_to_str(self, ignore: bool = False):
        """Decodes a hex string to ascii ignoring any decoding errors
        
        Args:
            ignore (bool, optional): Ignore errors, by default False
        
        Returns:
            Chepy: The Chepy object. 
        """
        if ignore:
            self.state = binascii.unhexlify(self._convert_to_bytes()).decode(
                errors="ignore"
            )
        else:
            self.state = binascii.unhexlify(self._convert_to_bytes())
        return self

    def str_to_hex(self):
        """Converts a string to a hex string
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = binascii.hexlify(self._convert_to_bytes())
        return self

    def int_to_hex(self):
        """Converts an integer into its hex equivalent
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = format(self._convert_to_int(), "x")
        return self

    def int_to_str(self):
        """Converts an integer into a string
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str()
        return self

    def binary_to_hex(self):
        """Converts binary data into a hex string
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = binascii.hexlify(self._convert_to_bytes())
        return self

    def normalize_hex(self, is_bytearray=False):
        """Normalize a hex string
        
        Removes special encoding characters from a hex string like %, 
        0x, , :, ;, \\n and \\r\\n

        Args:
            is_bytearray (bool, optional): Set to True if state is a bytearray
        
        Returns:
            Chepy: The Chepy object. 
        """
        if is_bytearray:
            self.state = binascii.hexlify(bytearray(self.state))
            return self
        else:
            delimiters = [" ", "0x", "%", ",", ";", ":", r"\\n", "\\r\\n"]
            string = re.sub("|".join(delimiters), "", self.state)
            # assert re.search(r"^[a-fA-F0-9]+$", string) is not None, "Invalid hex"
            self.state = string
            return self

    def hexdump_to_str(self):
        """Extract a string from a hexdump
        
        Returns:
            Chepy: The Chepy object.
        """
        # TODO make new line aware \n \r\n \0a etc
        self.state = "".join(re.findall(r"\|(.+)\|", self._convert_to_str()))
        return self

    def url_encode(self, safe: str = ""):
        """URL encode
        
        Encodes problematic characters into percent-encoding, 
        a format supported by URIs/URLs.
        
        Args:
            safe (str, optional): String of characters that will not be encoded, by default ""
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = _urllib_quote_plus(self._convert_to_str(), safe=safe)
        return self

    def url_decode(self):
        """Converts URI/URL percent-encoded characters back to their raw values.
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = _urllib_unquote_plus(self._convert_to_str())
        return self

    def bytearray_to_str(self, encoding: str = "utf8", errors: str = "replace"):
        """Convert a python bytearray to string
        
        Args:
            encoding (str, optional): String encoding. Defaults to 'utf8'.
            errors (str, optional): How errors should be handled. Defaults to replace. 
        
        Raises:
            TypeError: If state is not a bytearray

        Returns:
            Chepy: The Chepy object.
        """
        if isinstance(self.state, bytearray):
            self.state = self.state.decode(encoding, errors=errors)
            return self
        else:
            raise TypeError("State is not a bytearray")

    def get_by_index(self, index: int):
        """Get an item by specifying an index
        
        Args:
            index (int): Index number to get
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = self.state[index]
        return self

    def get_by_key(self, key: str):
        """Get an object from a dict by key
        
        Args:
            key (str): A valid key
        
        Returns:
            Chepy: The Chepy object.
        """
        if isinstance(self.state, dict):
            self.state = self.state.get(key)
            return self
        else:
            raise TypeError("State is not a dictionary")

