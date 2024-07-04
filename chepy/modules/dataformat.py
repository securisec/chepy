import lazy_import
import binascii
import base64
import codecs
import html
import base58
import json
import struct
import pickle
import string
import itertools
import quopri
import io
import csv
import sqlite3
import collections
from random import randint
import regex as re
from .internal.constants import Encoding
from .internal.helpers import (
    detect_delimiter,
    Rotate,
    Uint1Array,
    UUEncoderDecoder,
    Base92,
    Base45,
    _Base64,
    expand_alpha_range,
)

yaml = lazy_import.lazy_module("yaml")
import regex as re
import hexdump
from ast import literal_eval
from typing import TypeVar, Union, List, Literal
from urllib.parse import quote_plus as _urllib_quote_plus
from urllib.parse import unquote_plus as _urllib_unquote_plus

crypto_number = lazy_import.lazy_module("Crypto.Util.number")
msgpack = lazy_import.lazy_module("msgpack")

from ..core import ChepyCore, ChepyDecorators
from chepy.modules.internal.constants import Encoding
import chepy.modules.internal.rison as rison

DataFormatT = TypeVar("DataFormatT", bound="DataFormat")


class DataFormat(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    @ChepyDecorators.call_stack
    def eval_state(self) -> DataFormatT:
        """Eval state as python.
        Handy when converting string representation
        of objects.

        Returns:
            Chepy: The Chepy object
        """
        self.state = literal_eval(self.state)
        return self

    @ChepyDecorators.call_stack
    def bytes_to_ascii(self) -> DataFormatT:
        """Convert bytes (array of bytes) to ascii

        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, list), "Data in state is not a list"
        self.state = bytearray(self.state).decode()
        return self

    @ChepyDecorators.call_stack
    def list_to_str(self, join_by: Union[str, bytes] = " ") -> DataFormatT:
        """Join an array by `join_by`

        Args:
            join_by (Union[str, bytes], optional): String character to join by, by default ' '

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy(["a", "b", "c"]).list_to_str(",").o
            "a,b,c"
        """
        assert isinstance(self.state, list), "Data in state not a list"
        # convert the list of items in state appropriately
        if isinstance(join_by, str):
            self.state = [str(x) for x in self.state]
        elif isinstance(join_by, bytes):
            self.state = [bytes(x) for x in self.state]
        self.state = join_by.join(self.state)
        return self

    @ChepyDecorators.call_stack
    def str_list_to_list(self) -> DataFormatT:
        """Convert a string list to a list

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("[1,2,'lol', true]").str_list_to_list().o
            [1, 2, "lol", True]
        """
        self.state = json.loads(re.sub(r"'", '"', self._convert_to_str()))
        return self

    @ChepyDecorators.call_stack
    def join(self, join_by: Union[str, bytes] = "") -> DataFormatT:
        """Join a list with specified character

        Args:
            join_by (Union[str, bytes], optional): What to join with. Defaults to ""

        Returns:
            Chepy: The Chepy object.
        Examples:
            >>> Chepy(["a", "b", "c"]).join_list(":").o
            "a:b:c"
        """
        assert isinstance(self.state, list), "State is not a list"
        data = [self._to_bytes(x) for x in self.state]
        join_by = self._str_to_bytes(join_by)
        self.state = join_by.join(data)
        return self

    @ChepyDecorators.call_stack
    def json_to_dict(self) -> DataFormatT:
        """Convert a JSON string to a dict object

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy('{"some": "data", "a": ["list", 1, true]}').json_to_dict().o
            {
                "some": "data",
                "a": ["list", 1, True],
            }
        """
        self.state = json.loads(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def dict_to_json(self) -> DataFormatT:
        """Convert a dict object to a JSON string

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy({"some": "data", "a": ["list", 1, True]}).dict_to_json().o
            '{"some":"data","a":["list",1,true]}'
        """
        assert isinstance(self.state, dict), "Not a dict object"
        self.state = json.dumps(self.state)
        return self

    @ChepyDecorators.call_stack
    def dict_get_items(self, *keys: str) -> DataFormatT:
        """Get items from a dict. If no keys are specified, it will return all items.
        Returns:
            Chepy: The Chepy object.
        Examples:
            >>> o = Chepy({"a": 1, "b": 2}).dict_get_items("a", "b", "c").o
            [1, 2]
        """
        assert isinstance(self.state, dict), "Not a dict object"
        if len(keys) == 0:
            self.state = list(self.state.values())
            return self
        o = list()
        for k in keys:
            if self.state.get(k):
                o.append(self.state.get(k))
        self.state = o
        return self

    @ChepyDecorators.call_stack
    def yaml_to_json(self) -> DataFormatT:  # pragma: no cover
        """Convert yaml to a json string

        Returns:
            Chepy: The Chepy object.
        """
        self.state = json.dumps(yaml.safe_load(self.state))
        return self

    @ChepyDecorators.call_stack
    def json_to_yaml(self) -> DataFormatT:
        """Convert a json string to yaml structure

        Returns:
            Chepy: The Chepy object.
        """

        class ChepyYamlDumper(yaml.Dumper):
            def increase_indent(self, flow=False, indentless=False):
                return super(ChepyYamlDumper, self).increase_indent(flow, False)

        self.state = yaml.dump(
            json.loads(self.state),
            Dumper=ChepyYamlDumper,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
        return self

    @ChepyDecorators.call_stack
    def to_base58(self) -> DataFormatT:
        """Encode as Base58

        Base58 is a notation for encoding arbitrary byte data using a
        restricted set of symbols that can be conveniently used by humans
        and processed by computers.This property encodes raw data
        into an ASCII Base58 string.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").to_base58().out.decode()
            "2UDrs31qcWSPi"
        """
        self.state = base58.b58encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def from_base58(self) -> DataFormatT:
        """Decode as Base58

        Base58 is a notation for encoding arbitrary byte data using a
        restricted set of symbols that can be conveniently used by humans
        and processed by computers.This property decodes raw data
        into an ASCII Base58 string.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("2UDrs31qcWSPi").from_base58().out.decode()
            "some data"
        """
        self.state = base58.b58decode(self.state)
        return self

    @ChepyDecorators.call_stack
    def to_base85(self) -> DataFormatT:
        """Encode as Base58

        Base85 is a notation for encoding arbitrary byte data using a
        restricted set of symbols that can be conveniently used by humans
        and processed by computers.This property decodes raw data
        into an ASCII Base58 string.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").to_base85().out.decode()
            "F)Po,+Cno&@/"
        """
        self.state = base64.a85encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def from_base85(self) -> DataFormatT:
        """Decode as Base85

        Base85 is a notation for encoding arbitrary byte data using a
        restricted set of symbols that can be conveniently used by humans
        and processed by computers.This property decodes raw data
        into an ASCII Base58 string.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("F)Po,+Cno&@/").from_base85().out.decode()
            "some data"
        """
        self.state = base64.a85decode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def to_base16(self) -> DataFormatT:
        """Encode state in base16

        Returns:
            Chepy: The Chepy object.
        """
        self.state = base64.b16encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def from_base16(self) -> DataFormatT:
        """Decode state in base16

        Returns:
            Chepy: The Chepy object.
        """
        self.state = base64.b16decode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def to_base32(self) -> DataFormatT:
        """Encode as Base32

        Base32 is a notation for encoding arbitrary byte data using a
        restricted set of symbols that can be conveniently used by humans
        and processed by computers. It uses a smaller set of characters than
        Base64, usually the uppercase alphabet and the numbers 2 to 7.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").base32_encode().out.decode()
            "ONXW2ZJAMRQXIYI="
        """
        self.state = base64.b32encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def from_base32(self, remove_whitespace: bool = True) -> DataFormatT:
        """Decode as Base32

        Base32 is a notation for encoding arbitrary byte data using a
        restricted set of symbols that can be conveniently used by humans
        and processed by computers. It uses a smaller set of characters than
        Base64, usually the uppercase alphabet and the numbers 2 to 7.

        Args:
            remove_whitespace(bool, optional): If true, all whitespaces are removed

        Returns:
            Chepy: The Chepy object.
        """
        if remove_whitespace:
            self.state = self.remove_whitespace().o
        self.state = base64.b32decode(self.state)
        return self

    @ChepyDecorators.call_stack
    def to_base92(self) -> DataFormatT:
        """Encode to Base92

        Returns:
            Chepy: The Chepy object.
        """
        self.state = Base92.b92encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def from_base92(self) -> DataFormatT:
        """Decode from Base92

        Returns:
            Chepy: The Chepy object.
        """
        self.state = Base92.b92decode(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def to_base45(self) -> DataFormatT:
        """Encode to Base45

        Returns:
            Chepy: The Chepy object.
        """
        self.state = Base45().b45encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def from_base45(self) -> DataFormatT:
        """Decode from Base45

        Returns:
            Chepy: The Chepy object.
        """
        self.state = Base45().b45decode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def to_base91(self) -> DataFormatT:  # pragma: no cover
        """Base91 encode
        Reference: https://github.com/aberaud/base91-python/blob/master/base91.py#L69

        Returns:
            Chepy: The Chepy object.
        """
        bindata = self._convert_to_bytes()
        b = 0
        n = 0
        out = ""
        for count in range(len(bindata)):
            byte = bindata[count : count + 1]
            b |= struct.unpack("B", byte)[0] << n
            n += 8
            if n > 13:
                v = b & 8191
                if v > 88:
                    b >>= 13
                    n -= 13
                else:
                    v = b & 16383
                    b >>= 14
                    n -= 14
                out += (
                    Encoding.BASE91_ALPHABET[v % 91] + Encoding.BASE91_ALPHABET[v // 91]
                )
        if n:
            out += Encoding.BASE91_ALPHABET[b % 91]
            if n > 7 or b > 90:
                out += Encoding.BASE91_ALPHABET[b // 91]
        self.state = out
        return self

    @ChepyDecorators.call_stack
    def from_base91(self) -> DataFormatT:  # pragma: no cover
        """Decode as Base91
        Reference: https://github.com/aberaud/base91-python/blob/master/base91.py#L42

        Returns:
            Chepy: The Chepy object.
        """
        encoded_str = self._convert_to_str()
        decode_table = dict((v, k) for k, v in enumerate(Encoding.BASE91_ALPHABET))
        v = -1
        b = 0
        n = 0
        out = bytearray()
        for strletter in encoded_str:
            if strletter not in decode_table:
                continue
            c = decode_table[strletter]
            if v < 0:
                v = c
            else:
                v += c * 91
                b |= v << n
                n += 13 if (v & 8191) > 88 else 14
                while True:
                    out += struct.pack("B", b & 255)
                    b >>= 8
                    n -= 8
                    if not n > 7:
                        break
                v = -1
        if v + 1:
            out += struct.pack("B", (b | v << n) & 255)
        self.state = out
        return self

    @ChepyDecorators.call_stack
    def to_int(self) -> DataFormatT:
        """Converts the string representation of a number into an int

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("1").to_int().o
            1
        """
        self.state = int(self.state)
        return self

    @ChepyDecorators.call_stack
    def to_bytes(self) -> DataFormatT:
        """Converts the data in state to bytes

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy({'some': 'val', 'kl': 1}).to_bytes().o
            b"{'some': 'val', 'kl': 1}"
        """
        self.state = self._convert_to_str().encode()
        return self

    @ChepyDecorators.call_stack
    def from_bytes(self) -> DataFormatT:
        """Decodes bytes to string.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_bytes().decode()
        return self

    @ChepyDecorators.call_stack
    def to_base64(self, alphabet: str = "standard") -> DataFormatT:
        """Encode as Base64

        Base64 is a notation for encoding arbitrary byte data using a
        restricted set of symbols that can be conveniently used by humans
        and processed by computers.This property encodes raw data
        into an ASCII Base64 string.

        Args:
            alphabet (str, optional): Provide a custom charset to base64 with. Valid values are: filename_safe, itoa64, radix_64, rot13, standard, unix_crypt, url_safe, xml, xxencoding, z64

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> # To use a custom character set, use:
            >>> custom = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
            >>> Chepy("Some data").to_base64(custom=custom).o
            b'IqxhNG/YMLFV'
        """
        data = self._convert_to_bytes()
        alphabet = alphabet.strip()

        char_set = expand_alpha_range(
            _Base64.base_64_chars.get(alphabet, alphabet), join_by=""
        )
        if len(char_set) < 63 or len(char_set) > 66:  # pragma: no cover
            raise ValueError(
                "Invalid base64 chars. Should be 63-66 chars. " + str(len(char_set))
            )

        self.state = _Base64.encode_base64(data, alphabet=char_set)
        return self

    @ChepyDecorators.call_stack
    def from_base64(
        self, alphabet: str = "standard", remove_non_alpha: bool = True
    ) -> DataFormatT:
        """Decode as Base64

        Base64 is a notation for encoding arbitrary byte data using a
        restricted set of symbols that can be conveniently used by humans
        and processed by computers.This property decodes raw data
        into an ASCII Base64 string.

        Args:
            alphabet (str, optional): Provide a custom charset to base64 with. Valid values are: filename_safe, itoa64, radix_64, rot13, standard, unix_crypt, url_safe, xml, xxencoding, z64
            remove_whitespace(bool, optional): If true, all whitespaces are removed (Defaults to True)
            remove_non_alpha(bool, optional): If true, all whitespaces are removed. (Defaults to True)

        Returns:
            Chepy: The Chepy object.

        Examples:
            Base64 decode using a custom string
            >>> c = Chepy("QqxhNG/mMKtYPqoz64FVR42=")
            >>> c.from_base64(alphabet="./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
            >>> c.out
            b"some random? data"
        """
        alphabet = alphabet.strip()
        char_set = expand_alpha_range(
            _Base64.base_64_chars.get(alphabet, alphabet), join_by=""
        )
        if len(char_set) < 63 or len(char_set) > 65:  # pragma: no cover
            raise ValueError(
                "Invalid base64 chars. Should be 63-65 chars. " + str(len(char_set))
            )

        data = self._convert_to_str()

        if remove_non_alpha:
            data = re.sub("[^" + char_set + "]", "", data)

        # if is_standard or alphabet == 'url_safe':
        #     data += "=="
        padding_needed = len(data) % 4
        if padding_needed and alphabet != "url_safe":
            data += "=" * (4 - padding_needed)

        # if is_standard:
        #     self.state = base64.b64decode(data)
        # if alphabet == 'url_safe':
        #     self.state = base64.urlsafe_b64decode(data)
        # else:
        self.state = _Base64.decode_base64(data, char_set)
        return self

    @ChepyDecorators.call_stack
    def decode_bytes(self, errors: str = "ignore") -> DataFormatT:
        """Decode bytes to string

        Args:
            errors (str, optional): Ignore or replace error chars. Defaults to 'ignore'.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_bytes().decode(errors=errors)
        return self

    @ChepyDecorators.call_stack
    def to_hex(self, delimiter: str = "") -> DataFormatT:
        """Converts a string to its hex representation

        Args:
            delimiter (str, optional): Delimiter. Defaults to None.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("AAA").to_hex().out.decode()
            "414141"
        """
        if delimiter == "":
            self.state = binascii.hexlify(self._convert_to_bytes())
        else:
            self.state = binascii.hexlify(self._convert_to_bytes(), sep=delimiter)
        return self

    @ChepyDecorators.call_stack
    def from_hex(
        self,
        delimiter: str = None,
        join_by: str = "",
        replace: Union[bytes, None] = b"%|0x",
    ) -> DataFormatT:
        """Convert a non delimited hex string to string

        Args:
            delimiter (str, optional): Delimiter. Defaults to None.
            join_by (str, optional): Join by. Defaults to ' '.
            replace (Union[bytes, None], optional): Regex pattern to replace hex string prefixes. Defaults to b'%x|0x'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("414141").from_hex().out
            b"AAA"
        """
        data = self._convert_to_bytes()
        if replace is not None:
            replace = self._str_to_bytes(replace)
            data = re.sub(replace, b"", data)
        if delimiter is None:
            delimiter = detect_delimiter(data, default_delimiter=None)
        if delimiter is not None:
            self.state = join_by.encode().join(
                list(
                    binascii.unhexlify(x)
                    for x in data.split(self._str_to_bytes(delimiter))
                )
            )
        else:
            self.state = binascii.unhexlify(data)
        return self

    @ChepyDecorators.call_stack
    def hex_to_int(self) -> DataFormatT:
        """Converts hex into its integer representation

        Returns:
            Chepy: The Chepy object.

        Examples:
            Chepy works with hex characters that start with a 0x

            >>> Chepy("0x123").hex_to_int().out
            291

            Without 0x in the hex

            >>> Chepy("123").hex_to_int().out
            291
        """
        if self._convert_to_str().startswith("0x"):
            self.state = int(self.state, 0)
        else:
            self.state = int(self.state, 16)
        return self

    @ChepyDecorators.call_stack
    def hex_to_bytes(self) -> DataFormatT:
        """Hex to bytes hex

        Converts a hex string to its bytes form. Example:
        41 becomes \\x41

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("ab00").hex_to_bytes().o
            b"\\xab\\x00"
        """
        self.state = binascii.unhexlify(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def hex_to_str(self, ignore: bool = False) -> DataFormatT:
        """Decodes a hex string to ascii ignoring any decoding errors

        Args:
            ignore (bool, optional): Ignore errors, by default False

        Returns:
            Chepy: The Chepy object.

        Examples:
            To ignore UnicodeDecode errors, set ignore to True
            >>> Chepy("4100").hex_to_str(ignore=True).o
            "A\x00"
        """
        if ignore:
            self.state = binascii.unhexlify(self._convert_to_bytes()).decode(
                errors="ignore"
            )
        else:
            self.state = binascii.unhexlify(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def str_to_hex(self) -> DataFormatT:
        """Converts a string to a hex string

        Returns:
            Chepy: The Chepy object.
        """
        self.state = binascii.hexlify(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def int_to_hex(self) -> DataFormatT:
        """Converts an integer into its hex equivalent

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy(101).int_to_hex().o
            "65"
        """
        self.state = format(self._convert_to_int(), "x")
        return self

    @ChepyDecorators.call_stack
    def int_to_str(self) -> DataFormatT:
        """Converts an integer into a string

        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_str()
        return self

    @ChepyDecorators.call_stack
    def binary_to_hex(self) -> DataFormatT:
        """Converts binary data into a hex string

        Returns:
            Chepy: The Chepy object.
        """
        self.state = binascii.hexlify(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def normalize_hex(self, is_bytearray=False) -> DataFormatT:
        """Normalize a hex string

        Removes special encoding characters from a hex string like %,
        0x, , :, ;, \\n and \\r\\n

        Args:
            is_bytearray (bool, optional): Set to True if state is a bytearray

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("41:42:CE").normalize_hex().o
            "4142CE"
            >>> Chepy("0x410x420xce").normalize_hex().o
            "4142ce"
        """
        if is_bytearray:
            self.state = binascii.hexlify(bytearray(self.state))
            return self
        else:
            delimiters = [" ", "0x", "%", ",", ";", ":", r"\\n", "\\r\\n"]
            string = re.sub("|".join(delimiters), "", self.state)
            self.state = string
            return self

    @ChepyDecorators.call_stack
    def str_from_hexdump(self) -> DataFormatT:
        """Extract a string from a hexdump

        Returns:
            Chepy: The Chepy object.
        """
        # TODO make new line aware \n \r\n \0a etc
        self.state = "".join(re.findall(r"\|(.+)\|", self._convert_to_str()))
        return self

    @ChepyDecorators.call_stack
    def to_hexdump(self) -> DataFormatT:
        """Convert the state to hexdump

        Returns:
            Chepy: The Chepy object.
        """
        self.state = hexdump.hexdump(self._convert_to_bytes(), result="return")
        return self

    @ChepyDecorators.call_stack
    def from_hexdump(self) -> DataFormatT:
        """Convert hexdump back to str

        Returns:
            Chepy: The Chepy object.
        """
        self.state = hexdump.restore(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def to_url_encoding(self, safe: str = "", all_chars: bool = False) -> DataFormatT:
        """URL encode

        Encodes problematic characters into percent-encoding,
        a format supported by URIs/URLs.

        Args:
            safe (str, optional): String of characters that will not be encoded, by default ""
            all_chars (bool, optional): Encode all characters including safe characters

        Returns:
            Chepy: The Chepy object.

        Examples:
            Url encode while specifying save characters

            >>> Chepy("https://google.com/?lol=some data&a=1").to_url_encoding(safe="/:").o
            "https://google.com/%3Flol%3Dsome+data%26a%3D1"
        """
        data = self._convert_to_str()

        def encode_all(string):
            return "".join("%{0:0>2x}".format(ord(char)) for char in string)

        if all_chars:
            self.state = encode_all(data)
        else:
            self.state = _urllib_quote_plus(data, safe=safe)
        return self

    @ChepyDecorators.call_stack
    def from_url_encoding(self) -> DataFormatT:
        """Converts URI/URL percent-encoded characters back to their raw values.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("https://google.com/%3Flol%3Dsome+data%26a%3D1").from_url_encoding().o
            "https://google.com/?lol=some data&a=1"
        """
        self.state = _urllib_unquote_plus(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def bytearray_to_str(
        self, encoding: str = "utf8", errors: str = "replace"
    ) -> DataFormatT:
        """Convert a python bytearray to string

        Args:
            encoding (str, optional): String encoding. Defaults to 'utf8'.
            errors (str, optional): How errors should be handled. Defaults to replace.

        Raises:
            TypeError: If state is not a bytearray

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy(bytearray("lolol", "utf")).bytearray_to_str().o
            "lolol"
        """
        if isinstance(self.state, bytearray):
            self.state = self.state.decode(encoding, errors=errors)
            return self
        else:  # pragma: no cover
            raise TypeError("State is not a bytearray")

    @ChepyDecorators.call_stack
    def str_to_list(self) -> DataFormatT:
        """Convert string to list

        Converts the string in state to an array of individual characyers

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("abc").str_to_list().o
            ["a", "b", "c"]
        """
        self.state = list(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def str_to_dict(self) -> DataFormatT:
        """Convert string to a dictionary

        Returns:
            Chepy: The Chepy object.
        """
        self.state = yaml.safe_load(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def to_charcode(self, join_by: str = " ", base: int = 16) -> DataFormatT:
        """Convert a string to a list of unicode charcode

        Converts text to its unicode character code equivalent.
        e.g. Γειά σου becomes 0393 03b5 03b9 03ac 20 03c3 03bf 03c5

        Args:
            join_by (str, optional): String to join the charcodes by. Defaults to ' '.
            base (int, optional): Base to use for the charcodes. Defaults to 16.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("aㅎ").to_charcode()
            "61 314e"
        """
        hold = []
        for c in self._convert_to_str():
            hold.append(str(int(hex(ord(c))[2:], base)))
        self.state = join_by.join(hold)
        return self

    @ChepyDecorators.call_stack
    def from_charcode(
        self, delimiter: str = None, join_by: str = "", base: int = 10
    ) -> DataFormatT:
        """Convert array of unicode chars to string

        Args:
            delimiter (str, optional): Delimiter. Defaults to " ".
            join_by (str, optional): Join by. Defaults to "".
            base (int, optional): Base. Defaults to 10.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("314e 61 20 41"]).from_charcode().o
            "ㅎa A"
        """
        data = self._convert_to_str()
        out = []
        if not delimiter:
            delimiter = detect_delimiter(data)
        print("🟢 ", delimiter)
        for c in data.split(delimiter):
            out.append(chr(int(c, base)))
        self.state = join_by.join(out)
        return self

    @ChepyDecorators.call_stack
    def to_decimal(self, join_by: str = " ") -> DataFormatT:
        """Convert characters to decimal

        Args:
            join_by (str, optional): Join the decimal values by this. Defaults to ' '.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("aㅎ").to_decimal().o
            '97 12622'
        """
        self.state = join_by.join(
            str(x) for x in list(ord(s) for s in list(self._convert_to_str()))
        )
        return self

    @ChepyDecorators.call_stack
    def from_decimal(self, delimiter: str = None, join_by: str = "") -> DataFormatT:
        """Convert a list of decimal numbers to string

        Args:
            delimiter (str, optional): Delimiter. Defaults to " ".
            join_by (str, optional): Join by. Defaults to "".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy(12622).from_decimal().o
            "ㅎ"
        """
        data = self._convert_to_str()
        if not delimiter:
            delimiter = detect_delimiter(data)
        self.state = join_by.join(
            list(chr(int(s)) for s in data.strip().split(delimiter))
        )
        return self

    @ChepyDecorators.call_stack
    def to_binary(
        self, join_by: Union[str, bytes] = " ", byte_length: int = 8
    ) -> DataFormatT:
        """Convert string characters to binary

        Args:
            join_by (str, optional): join_by. Defaults to " ".
            byte_length (int, optional): Byte length. Defaults to 8.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("abc").to_binary().o
            b"01100001 01100010 01100011"
        """
        hold = []
        join_by = self._str_to_bytes(join_by)
        # out = list(format(s, "08b").encode() for s in list(self._convert_to_bytes()))
        for s in list(self._convert_to_bytes()):
            hold.append(str(bin(s)[2:].zfill(byte_length)).encode())
        self.state = join_by.join(hold)
        return self

    @ChepyDecorators.call_stack
    def from_binary(self, delimiter: str = None, byte_length: int = 8) -> DataFormatT:
        """Convert a list of binary numbers to string

        Args:
            delimiter (str, optional): Delimiter. Defaults to " ".
            byte_length (int, optional): Byte length. Defaults to 8.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("01100001 01100010 01100011").from_binary().o
            "abc"
        """
        data = self._convert_to_str()
        if not delimiter:
            delimiter = detect_delimiter(data)
        n = int(
            "".join([x[byte_length - 8 :] for x in data.split(delimiter)]),
            2,
        )
        self.state = n.to_bytes((n.bit_length() + 7) // 8, "big")
        return self

    @ChepyDecorators.call_stack
    def to_octal(self, join_by: str = " ") -> DataFormatT:
        """Convert string characters to octal

        Args:
            join_by (str, optional): Join by. Defaults to "".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("abㅎ").to_octal().o
            "141 142 30516"
        """
        self.state = join_by.join(
            list(format(ord(s), "0o") for s in list(self._convert_to_str()))
        )
        return self

    @ChepyDecorators.call_stack
    def from_octal(self, delimiter: str = None, join_by: str = "") -> DataFormatT:
        """Convert a list of octal numbers to string

        Args:
            delimiter (str, optional): Delimiter. Defaults to None.
            join_by (str, optional): Join by. Defaults to "".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("141 142").from_octal().o
            "ab"
        """
        data = self._convert_to_str()
        if not delimiter:
            delimiter = detect_delimiter(data, default_delimiter=delimiter)
        self.state = join_by.join(
            list(chr(int(str(x), 8)) for x in data.split(delimiter))
        )
        return self

    @ChepyDecorators.call_stack
    def to_html_entity(self, format="named", all_chars=False) -> DataFormatT:
        """Encode html entities

        Encode special html characters like & > < etc

        Args:
            format (str): Encoding format. Valid formats are named, numeric and hex. Defaults to named
            all_chars (bool): If all chars should be encoded. By default a-ZA-Z0-9 are skipped. Defaults to False

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy('https://google.com&a="lol"').to_html_entity().o
            "https://google.com&amp;a=&quot;lol&quot;"
        """
        data = self._convert_to_str()
        chars = {k: 1 for k in string.ascii_letters + string.digits}
        hold = ""
        for d in data:
            if not all_chars and chars.get(d) is not None:
                hold += d
                continue
            if format == "named":
                hold += Encoding.BYTE_TO_ENTITY.get(ord(d), f"&#{ord(d)};")
            elif format == "hex":
                hold += f"&#x{d.encode().hex()};"
            elif format == "numeric":
                hold += f"&#{ord(d)};"
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def from_html_entity(self) -> DataFormatT:
        """Decode html entities

        Decode special html characters like & > < etc

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("https://google.com&amp;a=&quot;lol&quot;").from_html_entity().o
            'https://google.com&a="lol"'
        """
        self.state = html.unescape(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def to_punycode(self) -> DataFormatT:
        """Encode to punycode

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("münchen").to_punycode().o
            b"mnchen-3ya"
        """
        self.state = self._convert_to_str().encode("punycode")
        return self

    @ChepyDecorators.call_stack
    def from_punycode(self) -> DataFormatT:
        """Decode to punycode

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy(b"mnchen-3ya").from_punycode().o
            "münchen"
        """
        self.state = self._convert_to_bytes().decode("punycode")
        return self

    @ChepyDecorators.call_stack
    def encode_bruteforce(self) -> DataFormatT:
        """Bruteforce the various encoding for a string

        Enumerates all supported text encodings for the input,
        allowing you to quickly spot the correct one.
        `Reference <https://docs.python.org/2.4/lib/standard-encodings.html>`__

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("münchen한").encode_bruteforce()
            {
                'ascii': b'm\\xfcnchen\\ud55c',
                'base64_codec': b'bcO8bmNoZW7tlZw=\\n',
                'big5': b'm\\xfcnchen\\ud55c',
                'big5hkscs': b'm\\x88\\xa2nchen\\ud55c',
                ...
            }
        """
        data = self._convert_to_str()
        final = dict()
        for enc in Encoding.py_encodings:
            final[enc] = data.encode(enc, errors="backslashreplace")

        for text_enc in Encoding.py_text_encodings:
            try:
                final[text_enc] = codecs.encode(data, text_enc)
            except TypeError:
                final[text_enc] = codecs.encode(data.encode(), text_enc)
            except UnicodeEncodeError:
                try:
                    final[text_enc] = codecs.encode(
                        data, text_enc, errors="backslashreplace"
                    )
                except TypeError:  # pragma: no cover
                    final[text_enc] = codecs.encode(
                        data.encode(), text_enc, errors="backslashreplace"
                    )
        self.state = final
        return self

    @ChepyDecorators.call_stack
    def decode_bruteforce(self) -> DataFormatT:
        """Bruteforce the various decoding for a string

        Enumerates all supported text encodings for the input,
        allowing you to quickly spot the correct one.
        `Reference <https://docs.python.org/2.4/lib/standard-encodings.html>`__

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("m\\xfcnchen\\ud55c").decode_bruteforce()
            {
                ...
                'unicode_escape': 'münchen한',
                'utf_16': '屭晸湣档湥畜㕤挵',
                'utf_16_be': '浜硦据捨敮屵搵㕣',
                ...
            }
        """
        data = self._convert_to_bytes()
        final = dict()
        for enc in Encoding.py_encodings:
            final[enc] = data.decode(enc, errors="backslashreplace")

        for text_enc in Encoding.py_text_encodings:
            try:
                final[text_enc] = codecs.decode(
                    data, text_enc, errors="backslashreplace"
                )
            except UnicodeDecodeError:  # pragma: no cover
                final[text_enc] = codecs.decode(
                    data.decode(), text_enc, errors="backslashreplace"
                )
            except AssertionError:
                final[text_enc] = ""
                continue
            except UnicodeError:
                final[text_enc] = ""
                continue
            except TypeError:
                final[text_enc] = ""
                continue
        self.state = final
        return self

    @ChepyDecorators.call_stack
    def to_braille(self) -> DataFormatT:
        """Convert text to six-dot braille symbols

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("secret message").to_braille().o
            "⠎⠑⠉⠗⠑⠞⠀⠍⠑⠎⠎⠁⠛⠑"
        """
        chars = dict(zip(Encoding.asciichars, Encoding.brailles))
        self.state = "".join(list(chars.get(c.lower()) for c in self.state))
        return self

    @ChepyDecorators.call_stack
    def from_braille(self) -> DataFormatT:
        """Convert text to six-dot braille symbols

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("⠎⠑⠉⠗⠑⠞⠀⠍⠑⠎⠎⠁⠛⠑").from_braille().o
            "secret message"
        """
        chars = dict(zip(Encoding.brailles, Encoding.asciichars))
        self.state = "".join(list(chars.get(c.lower()) for c in self.state))
        return self

    @ChepyDecorators.call_stack
    def trim(self) -> DataFormatT:
        """Trim string. Removes whitespaces

        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_str().strip()
        return self

    @ChepyDecorators.call_stack
    def to_nato(self, join_by: str = " ") -> DataFormatT:
        """Convert string to NATO phonetic format.

        Example: abc = Alpha Bravo Charlie

        Args:
            join_by (str, optional): [description]. Defaults to " ".

        Returns:
            Chepy: The Chepy object
        """
        nato_chars = Encoding.NATO_CONSTANTS_DICT
        hold = []
        data: str = self._convert_to_str()
        for d in data:
            if d.isalpha():
                hold.append(nato_chars.get(d.upper(), d.upper()))
            else:
                hold.append(d)
        self.state = join_by.join(hold)
        return self

    @ChepyDecorators.call_stack
    def from_nato(
        self, delimiter: Union[str, None] = None, join_by: str = ""
    ) -> DataFormatT:
        """Translate NATO phoentic to words

        Args:
            delimiter (str, optional): Delimiter to split on. Defaults to ' '.
            join_by (str, optional): Join result by. Defaults to ''.

        Returns:
            Chepy: The Chepy object
        """
        data = self._convert_to_str()
        if delimiter is None:
            delimiter = detect_delimiter(data)
        data = data.split(delimiter)
        d = {v: k for k, v in Encoding.NATO_CONSTANTS_DICT.items()}
        self.state = join_by.join([d.get(p, p) for p in data])
        return self

    @ChepyDecorators.call_stack
    def swap_strings(self, by: int) -> DataFormatT:
        """Swap characters in string

        Args:
            by (int): Number of bytes to swap

        Returns:
            Chepy: The Chepy object
        """
        t = list(self.state)
        t[::by], t[1::by] = t[1::by], t[::by]
        self.state = "".join(t)
        return self

    @ChepyDecorators.call_stack
    def to_string(self) -> DataFormatT:
        """Convert to string

        Returns:
            Chepy: The Chepy object
        """
        self.state = self._convert_to_str()
        return self

    @ChepyDecorators.call_stack
    def stringify(self, compact: bool = True) -> DataFormatT:
        """Stringify the state. This uses json.dumps unlike to_string

        Args:
            compact (bool, optional): If the output should be compact. Defaults to True.

        Returns:
            Chepy: The Chepy object.
        """
        sep = None
        if compact:
            sep = (",", ":")
        self.state = json.dumps(self.state, separators=sep)
        return self

    @ChepyDecorators.call_stack
    def select(self, start: int, end: int = None) -> DataFormatT:
        """Get an item by specifying an index

        Args:
            start (int): Starting index number to get
            end (int, optional): Ending index number to get. If none specified, will be end of item. Defaults to None.

        Returns:
            Chepy: The Chepy object.
        """
        if end is None:
            self.state = self.state[start:]
        else:
            self.state = self.state[start:end]
        return self

    @ChepyDecorators.call_stack
    def length(self) -> DataFormatT:
        """Get the length of the current state as string

        Returns:
            Chepy: The Chepy object.
        """
        self.state = len(self.state)
        return self

    @ChepyDecorators.call_stack
    def to_leetcode(self, replace_space: str = "") -> DataFormatT:
        """Convert to leetcode. Reference
        Reference github.com/ss8651twtw/CTF-flag-generator

        Args:
            replace_space (str, optional): Replace spaces with specified char. Defaults to ''.

        Returns:
            Chepy: The Chepy object.
        """

        def change(c):
            if replace_space and c == " ":
                return replace_space
            if c.isalpha():
                c = c.upper()
                char_set = Encoding.LEETCODE[ord(c) - ord("A")]
                new_c = char_set[randint(0, len(char_set) - 1)]
                return new_c
            else:
                return c

        hold = ""
        string = self._convert_to_str()
        for s in string:
            hold += change(s)
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def substitute(self, x: str, y: str) -> DataFormatT:
        """Replace a subset of specified characters in the state.

        Args:
            x (str): Chars to replace
            y (str): Chars to replace with

        Returns:
            Chepy: The Chepy object.
        """
        assert len(x) == len(y), "x and y chars are not of equal length"
        s = self._convert_to_str()
        o = s.maketrans(x, y)
        self.state = s.translate(o)
        return self

    @ChepyDecorators.call_stack
    def remove_nonprintable(self, replace_with: Union[str, bytes] = b"") -> DataFormatT:
        """Remove non-printable characters from string.

        Args:
            replace_with (bytes, optional): Replace non-printable characters with this. Defaults to ''.

        Returns:
            Chepy: The Chepy object.
        """
        replace_with = self._str_to_bytes(replace_with)
        data = self._convert_to_bytes()
        self.state = re.sub(b"[^[:print:]]", replace_with, data)
        return self

    @ChepyDecorators.call_stack
    def swap_endianness(self, word_length: int = 4) -> DataFormatT:
        """Swap endianness.

        Args:
            word_length (int, optional): Word length. Use 8 for big endian. Defaults to 4.

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_bytes()
        num_bytes = len(data)
        padding_length = (word_length - num_bytes) % word_length
        padded_data = data + b"\x00" * padding_length

        swapped_data = b""
        for i in range(0, len(padded_data), word_length):
            word = padded_data[i : i + word_length]
            swapped_word = struct.unpack("<" + "B" * word_length, word)[::-1]
            swapped_data += struct.pack("B" * word_length, *swapped_word)

        self.state = swapped_data
        return self

    @ChepyDecorators.call_stack
    def bruteforce_from_base_xx(self) -> DataFormatT:
        """Bruteforce various base encodings. Current supports base85, base16, base32, base64, base85, base58

        Returns:
            Chepy: The Chepy object.
        """
        hold = {}
        ops = {
            "base85": base64.a85decode,
            "base16": base64.b16decode,
            "base32": base64.b32decode,
            "base64": base64.b64decode,
            "base58": base58.b58decode,
        }
        data = self._convert_to_bytes()
        for do in ops.items():
            try:
                hold[do[0]] = do[1](data)
            except:
                hold[do[0]] = None
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def long_to_bytes(self) -> DataFormatT:
        """Long numbers to bytes

        Returns:
            Chepy: The Chepy object.
        """
        d = self._convert_to_int()
        self.state = crypto_number.long_to_bytes(d)
        return self

    @ChepyDecorators.call_stack
    def bytes_to_long(self) -> DataFormatT:
        """Bytes to long

        Returns:
            Chepy: The Chepy object.
        """
        d = self._convert_to_bytes()
        self.state = crypto_number.bytes_to_long(d)
        return self

    @ChepyDecorators.call_stack
    def concat(self, data: Union[str, bytes]) -> DataFormatT:
        """Concat bytes to the current state

        Args:
            data (Union[str, bytes]): Data to add

        Returns:
            Chepy: The Chepy object. s
        """
        data = self._str_to_bytes(data)
        self.state = self._convert_to_bytes() + data
        return self

    @ChepyDecorators.call_stack
    def to_wingdings(self) -> DataFormatT:
        """Encode to windings

        Returns:
            Chepy: The Chepy object.
        """
        hold = ""
        for c in list(self._convert_to_str()):
            hold += chr(Encoding.wingdings.get(c, ord(c)))
        self.state = hold.encode()
        return self

    @ChepyDecorators.call_stack
    def from_wingdings(self) -> DataFormatT:
        """Decode from windings

        Returns:
            Chepy: The Chepy object.
        """
        conv = {v: k for k, v in Encoding.wingdings.items()}
        hold = ""
        for i in list(self._convert_to_str()):
            hold += conv.get(ord(i), i)
        self.state = hold.encode()
        return self

    @ChepyDecorators.call_stack
    def from_twin_hex(self) -> DataFormatT:
        """Decode twin hex

        Returns:
            Chepy: The Chepy object.
        """
        spaceChar = " "
        cypherBase = []
        for x in range(32, 128):
            for y in range(32, 128):
                thisPair = chr(x) + chr(y)
                cypherBase.append(thisPair)

        def tripleSplit(strInput):
            outArray = []
            thisTriple = ""
            i = 0
            while i < len(strInput):
                thisTriple = strInput[i]
                i += 1
                if i < len(strInput):
                    thisTriple += strInput[i]
                else:  # pragma: no cover
                    thisTriple += spaceChar
                i += 1
                if i < len(strInput):
                    thisTriple += strInput[i]
                else:  # pragma: no cover
                    thisTriple += spaceChar
                outArray.append(thisTriple)
                i += 1
            return outArray

        def base36_encode(string):
            return int(string, 36)

        inputArray = tripleSplit(self._convert_to_str())
        strOutput = ""
        thisPair = ""
        for code in inputArray:
            if code and len(code):
                thisCode = base36_encode(code)
                thisPair = cypherBase[thisCode]
                strOutput += thisPair
        self.state = strOutput.encode()
        return self

    @ChepyDecorators.call_stack
    def to_twin_hex(self) -> DataFormatT:
        """Encode to twin hex encoding

        Returns:
            Chepy: The Chepy object.
        """

        def base36_decode(number):
            alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
            if number == 0:  # pragma: no cover
                return "0"
            base36 = ""
            while number != 0:
                number, i = divmod(number, 36)
                base36 = alphabet[i] + base36
            return base36

        def dHex(thisPair):
            intCode = cypherBase.index(thisPair)
            strOutput = base36_decode(intCode)
            if len(strOutput) == 2:  # pragma: no cover
                return strOutput + spaceChar
            else:
                return strOutput

        spaceChar = " "
        cypherBase = []
        for x in range(32, 128):
            for y in range(32, 128):
                thisPair = chr(x) + chr(y)
                cypherBase.append(thisPair)

        strInput = self._convert_to_str()
        strOutput = ""
        thisPair = ""
        i = 0
        while i < len(strInput):
            thisPair = strInput[i]
            i += 1
            if i < len(strInput):
                thisPair += strInput[i]
            else:  # pragma: no cover
                thisPair += spaceChar
            strOutput += dHex(thisPair)
            i += 1
        self.state = strOutput.encode()
        return self

    @ChepyDecorators.call_stack
    def from_base36(
        self, delimiter: Union[str, bytes] = " ", join_by: Union[str, bytes] = " "
    ) -> DataFormatT:
        """Decode Base36 data

        Args:
            delimiter (Union[str, bytes], optional): Delimiter to split groups of ints by. Defaults to ' '.
            join_by (Union[str, bytes], optional): Join final output by. Defaults to ' '.

        Returns:
            Chepy: The Chepy object.
        """
        delimiter = self._bytes_to_str(delimiter)
        join_by = self._bytes_to_str(join_by)
        data = self._convert_to_str().split(delimiter)
        hold = []

        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
        for number in data:
            number = int(number)
            if number == 0:
                return "0"  # pragma: no cover
            base36 = ""
            while number != 0:
                number, i = divmod(number, 36)
                base36 = alphabet[i] + base36
            hold.append(base36)
        self.state = join_by.join(hold)
        return self

    @ChepyDecorators.call_stack
    def to_base36(self, join_by: Union[str, bytes] = b" ") -> DataFormatT:
        """Encode to Base 36

        Args:
            join_by (Union[str, bytes], optional): Join final output by. Defaults to b' '.

        Returns:
            Chepy: The Chepy object.
        """
        join_by = self._str_to_bytes(join_by)
        data = self._convert_to_str()
        data = re.compile(r"[^a-zA-Z0-9]").sub(" ", data).split()
        hold = []
        for d in data:
            hold.append(str(int(d.strip(), 36)).encode())
        self.state = join_by.join(hold)
        return self

    @ChepyDecorators.call_stack
    def to_pickle(self) -> DataFormatT:
        """Pickle serialize state

        Returns:
            Chepy: The Chepy object.
        """
        self.state = pickle.dumps(self.state)
        return self

    @ChepyDecorators.call_stack
    def from_pickle(self, trust: bool = False) -> DataFormatT:
        """Deserialize pickle data

        Args:
            trust (bool, optional): As this can lead to code execution, this is a safety net and needs to be set to True. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        if not trust:
            return self
        self.state = pickle.loads(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def to_bacon(
        self,
        A: Literal["A", "0"] = "A",
        B: Literal["B", "1"] = "B",
        complete: bool = True,
        join_by: Union[str, bytes] = b" ",
        invert: bool = False,
    ) -> DataFormatT:
        """Bacon encode

        Args:
            A (Literal['A', '0'], optional): The A character. Defaults to 'A'.
            B (Literal['B', '1'], optional): The B character. Defaults to 'B'.
            complete (bool, optional): Use unique mapping for all characters. Defaults to True.
            join_by (Union[str,bytes], optional): Join output by. Defaults to b' '.
            invert (bool, optional): Invert encoding. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        join_by = self._str_to_bytes(join_by)
        hold = []
        for s in self._convert_to_str():
            if s in string.ascii_letters:
                if complete:
                    hold.append(Encoding.BACON_26.get(s.upper()))
                else:  # pragma: no cover
                    hold.append(Encoding.BACON_24.get(s.upper()))
        updated = []
        for h in hold:
            if invert:  # pragma: no cover
                updated.append(h.replace("a", B).replace("b", A).encode())
            else:
                updated.append(h.replace("a", A).replace("b", B).encode())
        self.state = join_by.join(updated)
        return self

    @ChepyDecorators.call_stack
    def from_bacon(
        self,
        A: Literal["A", "0"] = "A",
        B: Literal["B", "1"] = "B",
        complete: bool = True,
        split_by: Union[str, bytes] = b" ",
        invert: bool = False,
    ) -> DataFormatT:
        """From Bacon

        Args:
            A (Literal['A','0'], optional): A character. Defaults to 'A'.
            B (str, optional): B character. Defaults to 'B'.
            complete (bool, optional): Use unique mapping for all characters. Defaults to True.
            split_by (Union[str,bytes], optional): Split by. Defaults to b' '.
            invert (bool, optional): Invert decoding. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        split_by = self._bytes_to_str(split_by)
        if complete:
            mapping = {v: k for k, v in Encoding.BACON_26.items()}
        else:
            mapping = {v: k for k, v in Encoding.BACON_26.items()}  # pragma: no cover
        data = self.state
        if not isinstance(self.state, list):  # pragma: no cover
            data = self._convert_to_str().split(split_by)
        out = ""
        for d in data:
            if invert:  # pragma: no cover
                d = d.replace(A, "b").replace(B, "a")
            else:
                d = d.replace(A, "a").replace(B, "b")
            out += mapping.get(d, "")
        self.state = out.encode()
        return self

    @ChepyDecorators.call_stack
    def to_upside_down(self, reverse: bool = False):
        """To upside down

        Args:
            reverse (bool, optional): Reverse order. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        hold = ""
        for s in self._convert_to_str():
            hold += Encoding.UPSIDE_DOWN.get(s, s)
        if reverse:
            self.state = hold[::-1]
        else:
            self.state = hold
        return self

    @ChepyDecorators.call_stack
    def from_upside_down(self, reverse: bool = False):
        """From upside down

        Args:
            reverse (bool, optional): Reverse order. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        encoding = {v: k for k, v in Encoding.UPSIDE_DOWN.items()}
        hold = ""
        for s in self._convert_to_str():
            hold += encoding.get(s, s)
        if reverse:
            self.state = hold[::-1]
        else:
            self.state = hold
        return self

    @ChepyDecorators.call_stack
    def to_messagepack(self) -> DataFormatT:
        """To MessagePack

        Returns:
            Chepy: The Chepy object.
        """
        self.state = msgpack.packb(self.state)
        return self

    @ChepyDecorators.call_stack
    def from_messagepack(self) -> DataFormatT:
        """From MessagePack

        Returns:
            Chepy: The Chepy object.
        """
        self.state = msgpack.unpackb(self.state, raw=False)
        return self

    @ChepyDecorators.call_stack
    def unicode_escape(
        self, padding: int = 0, uppercase_hex: bool = False
    ) -> DataFormatT:
        """Unicode escape

        Args:
            padding (int, optional): Optional padding. Defaults to 0.
            uppercase_hex (bool, optional): Uppercase hex chars. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """

        def unicode_replacer(match):
            code_point = ord(match.group(0))
            padding_format = "{:04x}".format(code_point)
            if uppercase_hex:
                padding_format = padding_format.upper()
            return r"\u" + "0" * padding + padding_format

        escaped_string = re.sub(
            r"[^\x00-\x7F]", unicode_replacer, self._convert_to_str()
        )
        self.state = escaped_string
        return self

    @ChepyDecorators.call_stack
    def to_base(self, radix: int = 36) -> DataFormatT:
        """Convert int to base

        Args:
            radix (int, optional): Radix. Defaults to 36.

        Returns:
            Chepy: The Chepy object.
        """
        num = self._convert_to_int()
        if num == 0:
            self.state = "0"
            return self

        chars = string.digits + string.ascii_lowercase
        result = ""

        while num > 0:
            remainder = num % radix
            result = chars[remainder] + result
            num //= radix

        self.state = result
        return self

    @ChepyDecorators.call_stack
    def from_base(self, radix: int = 36) -> DataFormatT:
        """Convert string to int base

        Args:
            radix (int, optional): Radix. Defaults to 36.

        Returns:
            Chepy: The Chepy object.
        """
        chars = string.digits + string.ascii_lowercase
        result = 0

        string_num = self._convert_to_str()
        for char in string_num:
            result = result * radix + chars.index(char)

        self.state = result
        return self

    @ChepyDecorators.call_stack
    def rotate_right(self, radix: int = 1, carry: bool = False) -> DataFormatT:
        """Rotate right

        Args:
            radix (int, optional): Radix. Defaults to 1.
            carry (bool, optional): Carry. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        r = Rotate(self._convert_to_bytes(), radix)
        if carry:
            self.state = r.rot_right_carry()
        else:
            self.state = r.rot(Rotate.rotate_right)
        return self

    @ChepyDecorators.call_stack
    def rotate_left(self, radix: int = 1, carry: bool = False) -> DataFormatT:
        """Rotate left

        Args:
            radix (int, optional): Radix. Defaults to 1.
            carry (bool, optional): Carry. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        r = Rotate(self._convert_to_bytes(), radix)
        if carry:
            self.state = r.rotate_left_carry()
        else:
            self.state = r.rot(Rotate.rotate_left)
        return self

    @ChepyDecorators.call_stack
    def to_base62(
        self,
        alphabet: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    ) -> DataFormatT:
        """Encode to base62

        Args:
            alphabet (str, optional): Alphabet. Defaults to "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".

        Returns:
            Chepy: The Chepy object
        """
        base62 = []
        num = int.from_bytes(self._convert_to_bytes(), byteorder="big")

        while num > 0:
            num, remainder = divmod(num, 62)
            base62.insert(0, alphabet[remainder])

        self.state = "".join(base62)
        return self

    @ChepyDecorators.call_stack
    def from_base62(
        self,
        alphabet: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    ) -> DataFormatT:
        """Decode from base62

        Args:
            alphabet (str, optional): Alphabet. Defaults to "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".

        Returns:
            Chepy: The Chepy object.
        """
        base62_dict = {char: index for index, char in enumerate(alphabet)}
        num = 0
        for char in self._convert_to_str():
            num = num * 62 + base62_dict[char]
        decoded_data = num.to_bytes((num.bit_length() + 7) // 8, byteorder="big")

        self.state = decoded_data
        return self

    @ChepyDecorators.call_stack
    def cut(self, start: int, end: int) -> DataFormatT:
        """Convert the state to bytes and cut x:y data from it

        Args:
            start (int): Starting position
            end (int): End position

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_bytes()
        self.state = data[start:end]
        return self

    @ChepyDecorators.call_stack
    def flatten(self) -> DataFormatT:
        """Flatten a list of lists into a single list

        Returns:
            Chepy: The Chepy object.
        """
        try:
            self.state = list(itertools.chain(*self.state))
            return self
        except:
            return self

    @ChepyDecorators.call_stack
    def to_utf21(self) -> DataFormatT:
        """Convert to UTF-21

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_bytes()
        bits = Uint1Array(len(data) * 21)

        bit_index = 0
        for codepoint in data:
            for i in range(20, -1, -1):
                bits.set(bit_index, (codepoint & (1 << i)) >> i)
                bit_index += 1

        self.state = bytes(bits.buffer)
        return self

    @ChepyDecorators.call_stack
    def from_utf21(self) -> DataFormatT:
        """Convert from UTF-21

        Returns:
            Chepy: The Chepy object.
        """
        buffer = self._convert_to_bytes()
        bits = Uint1Array(buffer)
        codepoint_length = (len(buffer) * 8) // 21
        codepoints = []

        for codepoint_index in range(codepoint_length):
            start_bit_index = codepoint_index * 21
            codepoint = 0

            for i in range(21):
                bit = bits.get(start_bit_index + i)
                codepoint += bit << (20 - i)

            codepoints.append(codepoint)

        self.state = bytes(codepoints)
        return self

    @ChepyDecorators.call_stack
    def to_uuencode(self, header: str = "-") -> DataFormatT:
        """To UUEncode

        Args:
            header (str): header

        Returns:
            Chepy: The Chepy object.
        """
        self.state = UUEncoderDecoder(self._convert_to_bytes(), header).uuencode()
        return self

    @ChepyDecorators.call_stack
    def from_uuencode(self: DataFormatT, header: str = "-") -> DataFormatT:
        """From UUEncode

        Args:
            header (str): header

        Returns:
            Chepy: The Chepy object.
        """
        self.state = UUEncoderDecoder(self._convert_to_bytes(), header).uudecode()
        return self

    @ChepyDecorators.call_stack
    def from_quoted_printable(self) -> DataFormatT:
        """From quoted printable

        Returns:
            Chepy: The Chepy object.
        """
        self.state = quopri.decodestring(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def to_quoted_printable(self) -> DataFormatT:
        """To quoted printable

        Returns:
            Chepy: The Chepy object.
        """
        self.state = quopri.encodestring(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def from_rison(self) -> DataFormatT:
        """Encode to RISON

        Returns:
            Chepy: The Chepy object.
        """
        self.state = rison.loads(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def to_rison(self) -> DataFormatT:
        """Decode from RISON

        Returns:
            Chepy: The Chepy object.
        """
        self.state = rison.dumps(self.state)
        # if option is None:
        # elif option == 'array':
        #     self.state = rison.encode_array(self.state)
        # elif option == 'object':
        #     self.state = rison.encode_object(self.state)
        # elif option == 'uri':
        #     self.state = rison.encode_uri(self.state)
        # else:
        #     self._log.error('Invalid data type')
        return self

    @ChepyDecorators.call_stack
    def increment_bytes(self, n: int) -> DataFormatT:
        """Loop through each byte and increment

        Args:
            n (int): increment by.

        Returns:
            Chepy: The Chepy object.
        """
        count = int(n)
        hold = bytearray()
        data = self._convert_to_bytes()
        for d in data:
            hold.append(d + count)
        self.state = bytes(hold)
        return self

    @ChepyDecorators.call_stack
    def decrement_bytes(self, n: int) -> DataFormatT:
        """Loop through each byte and decrement

        Args:
            n (int): decrement by.

        Returns:
            Chepy: The Chepy object.
        """
        count = int(n)
        hold = bytearray()
        data = self._convert_to_bytes()
        for d in data:
            hold.append(d - count)
        self.state = bytes(hold)
        return self

    @ChepyDecorators.call_stack
    def parse_csv(self) -> DataFormatT:
        """Parse a csv file. Returns a list of dict objects.

        Returns:
            Chepy: The Chepy object.
        """
        data = io.StringIO(self._convert_to_str())
        rows = csv.DictReader(data)
        self.state = [x for x in rows]
        return self

    @ChepyDecorators.call_stack
    def parse_sqlite(self, query: str) -> DataFormatT:
        """Parse sqlite db and run queries against it. Returns an array of dict objects with column as key and value

        Args:
            query (str): SQL Query

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_bytes()
        query = self._bytes_to_str(query)
        conn = sqlite3.connect(":memory:")
        conn.deserialize(data)
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()
        hold = []
        columns = [col[0] for col in cursor.description]

        for r in rows:
            hold.append(dict(collections.OrderedDict(zip(columns, r))))

        self.state = hold
        return self
