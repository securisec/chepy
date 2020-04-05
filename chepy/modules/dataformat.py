import binascii
import base64
import codecs
import html
import base58
import ujson
import yaml
import regex as re
import hexdump
from typing import Union
from urllib.parse import quote_plus as _urllib_quote_plus
from urllib.parse import unquote_plus as _urllib_unquote_plus

from ..core import ChepyCore, ChepyDecorators
from chepy.modules.internal.constants import Encoding


class DataFormat(ChepyCore):
    @ChepyDecorators.call_stack
    def list_to_str(self, join_by: Union[str, bytes]=" "):
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
        self.state = join_by.join(self.state)
        return self

    @ChepyDecorators.call_stack
    def str_list_to_list(self):
        """Convert a string list to a list
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("[1,2,'lol', true]").str_list_to_list().o
            [1, 2, "lol", True]
        """
        self.state = ujson.loads(re.sub(r"'", '"', self._convert_to_str()))
        return self

    @ChepyDecorators.call_stack
    def join_list(self, by: Union[str, bytes] = ""):
        """Join a list with specified character
        
        Args:
            by (Union[str, bytes], optional): What to join with. Defaults to ""
        
        Returns:
            Chepy: The Chepy object. 
        Examples:
            >>> Chepy(["a", "b", "c"]).join_list(":").o
            "a:b:c"
        """
        self.state = by.join(self.state)
        return self

    @ChepyDecorators.call_stack
    def json_to_dict(self):
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
        self.state = ujson.loads(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def dict_to_json(self):
        """Convert a dict object to a JSON string
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy({"some": "data", "a": ["list", 1, True]}).dict_to_json().o
            '{"some":"data","a":["list",1,true]}'
        """
        assert isinstance(self.state, dict), "Not a dict object"
        self.state = ujson.dumps(self.state)
        return self

    @ChepyDecorators.call_stack
    def yaml_to_json(self):
        """Convert yaml to a json string
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = ujson.dumps(yaml.safe_load(self.state))
        return self

    @ChepyDecorators.call_stack
    def json_to_yaml(self):
        """Convert a json string to yaml structure
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = yaml.dump(
            ujson.loads(self.state),
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
        return self

    @ChepyDecorators.call_stack
    def base58_encode(self):
        """Encode as Base58
        
        Base58 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property encodes raw data 
        into an ASCII Base58 string.

        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some data").base58_encode().output.decode()
            "2UDrs31qcWSPi"
        """
        self.state = base58.b58encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def base58_decode(self):
        """Decode as Base58
        
        Base58 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base58 string.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("2UDrs31qcWSPi").base58_decode().output.decode()
            "some data"
        """
        self.state = base58.b58decode(self.state)
        return self

    @ChepyDecorators.call_stack
    def base85_encode(self):
        """Encode as Base58

        Base85 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base58 string.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some data").base85_encode().output.decode()
            "F)Po,+Cno&@/"
        """
        self.state = base64.a85encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def base85_decode(self):
        """Decode as Base85

        Base85 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base58 string.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("F)Po,+Cno&@/").base85_decode().output.decode()
            "some data"
        """
        self.state = base64.a85decode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def base32_encode(self):
        """Encode as Base32
        
        Base32 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers. It uses a smaller set of characters than 
        Base64, usually the uppercase alphabet and the numbers 2 to 7.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some data").base32_encode().output.decode()
            "ONXW2ZJAMRQXIYI="
        """
        self.state = base64.b32encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def base32_decode(self):
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

    @ChepyDecorators.call_stack
    def to_int(self):
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
    def to_bytes(self):
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
    def from_bytes(self):
        """Decodes bytes to string.
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_bytes().decode()
        return self

    @ChepyDecorators.call_stack
    def base64_encode(self, custom: str = None):
        """Encode as Base64
        
        Base64 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property encodes raw data 
        into an ASCII Base64 string.

        Args:
            custom (str, optional): Provide a custom charset to base64 with
        
        Returns:
            Chepy: The Chepy object. 
        
        Examples:
            >>> # To use a custom character set, use:
            >>> custom = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
            >>> Chepy("Some data").base64_encode(custom=custom).o
            b'IqxhNG/YMLFV'
        """
        if custom is not None:
            x = base64.b64encode(self._convert_to_bytes())
            std_base64chars = (
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
            )
            self.state = bytes(
                str(x)[2:-1].translate(str(x)[2:-1].maketrans(std_base64chars, custom)),
                "utf-8",
            )
        else:
            self.state = base64.b64encode(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def base64_decode(self, custom: str = None, fix_padding: bool = True):
        """Decode as Base64

        Base64 is a notation for encoding arbitrary byte data using a 
        restricted set of symbols that can be conveniently used by humans 
        and processed by computers.This property decodes raw data 
        into an ASCII Base64 string.

        Args:
            custom (str, optional): Provide a custom charset to base64 with
            fix_padding (bool, optional): If padding error, add padding. Defaults to True
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            Base64 decode using a custom string
            >>> c = Chepy("QqxhNG/mMKtYPqoz64FVR42=")
            >>> c.base64_decode(custom="./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
            >>> c.out()
            b"some random? data"
        """
        if custom is not None:
            std_base64chars = (
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
            )
            c = self._convert_to_str().translate(str.maketrans(custom, std_base64chars))
            self.state = base64.b64decode(c.encode())
        else:
            try:
                self.state = base64.b64decode(self._convert_to_bytes())
            except binascii.Error:
                if fix_padding:
                    try:
                        self._warning_logger("Padding error. Adding =")
                        self.state = base64.b64decode(self._convert_to_bytes() + b"=")
                    except binascii.Error:  # pragma: no cover
                        self._warning_logger("Padding error. Adding ==")
                        self.state = base64.b64decode(self._convert_to_bytes() + b"==")
                else:  # pragma: no cover
                    raise
        return self

    @ChepyDecorators.call_stack
    def to_hex(self):
        """Converts a string to its hex representation
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("AAA").to_hex().out().decode()
            "414141"
        """
        self.state = binascii.hexlify(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def from_hex(self):
        """Convert a non delimited hex string to string
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("414141").from_hex().out()
            b"AAA"
        """
        self.state = binascii.unhexlify(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def hex_to_int(self):
        """Converts hex into its intiger represantation
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            Chepy works with hex characters that start with a 0x

            >>> Chepy("0x123").hex_to_int().output
            291
            
            Without 0x in the hex

            >>> Chepy("123").hex_to_int().output
            291
        """
        if self._convert_to_str().startswith("0x"):
            self.state = int(self.state, 0)
        else:
            self.state = int(self.state, 16)
        return self

    @ChepyDecorators.call_stack
    def hex_to_binary(self):
        """Hex to binary hex
        
        Converts a hex string to its binary form. Example: 
        41 becomes \\x41
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("ab00").hex_to_binary().o
            b"\\xab\\x00"
        """
        self.state = binascii.unhexlify(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def hex_to_str(self, ignore: bool = False):
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
    def str_to_hex(self):
        """Converts a string to a hex string
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = binascii.hexlify(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def int_to_hex(self):
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
    def int_to_str(self):
        """Converts an integer into a string
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str()
        return self

    @ChepyDecorators.call_stack
    def binary_to_hex(self):
        """Converts binary data into a hex string
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = binascii.hexlify(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def normalize_hex(self, is_bytearray=False):
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
    def str_from_hexdump(self):
        """Extract a string from a hexdump
        
        Returns:
            Chepy: The Chepy object.
        """
        # TODO make new line aware \n \r\n \0a etc
        self.state = "".join(re.findall(r"\|(.+)\|", self._convert_to_str()))
        return self

    @ChepyDecorators.call_stack
    def to_hexdump(self):
        """Convert the state to hexdump
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = hexdump.hexdump(self._convert_to_bytes(), result="return")
        return self

    @ChepyDecorators.call_stack
    def from_hexdump(self):
        """Convert hexdump back to str
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = hexdump.restore(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def url_encode(self, safe: str = ""):
        """URL encode
        
        Encodes problematic characters into percent-encoding, 
        a format supported by URIs/URLs.
        
        Args:
            safe (str, optional): String of characters that will not be encoded, by default ""
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            Url encode while specifying save characters

            >>> Chepy("https://google.com/?lol=some data&a=1").url_encode(safe="/:").o
            "https://google.com/%3Flol%3Dsome+data%26a%3D1"
        """
        self.state = _urllib_quote_plus(self._convert_to_str(), safe=safe)
        return self

    @ChepyDecorators.call_stack
    def url_decode(self):
        """Converts URI/URL percent-encoded characters back to their raw values.
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("https://google.com/%3Flol%3Dsome+data%26a%3D1").url_decode().o
            "https://google.com/?lol=some data&a=1"
        """
        self.state = _urllib_unquote_plus(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def bytearray_to_str(self, encoding: str = "utf8", errors: str = "replace"):
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
    def str_to_list(self):
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
    def str_to_dict(self):
        """Convert string to a dictionary
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = yaml.safe_load(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def to_charcode(self, escape_char: str = ""):
        """Convert a string to a list of unicode charcode

        Converts text to its unicode character code equivalent.
        e.g. Γειά σου becomes 0393 03b5 03b9 03ac 20 03c3 03bf 03c5

        Args:
            escape_char (str, optional): Charcater to prepend with. Example \\u, u etc. 
                @ChepyDecorators.call_stack
                Defaults to ''
        
        Returns:
            Chepy: The Chepy object. 
        
        Examples:
            >>> Chepy("aㅎ").to_charcode().o
            ["61", "314e"]
        """
        self.state = list(
            "{escape}{hex:02x}".format(escape=escape_char, hex=ord(x))
            for x in list(self._convert_to_str())
        )
        return self

    @ChepyDecorators.call_stack
    def from_charcode(self, prefix: str = ""):
        """Convert array of unicode chars to string
        
        Args:
            prefix (str, optional): Any prefix for the charcode. Ex: \\u or u. Defaults to "".
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy(["314e", "61", "20", "41"]).from_charcode().o
            ["ㅎ", "a", " ", "A"]
        """
        out = []
        for c in self.state:
            c = re.sub(prefix, "", c)
            out.append(chr(int(c, 16)))
        self.state = out
        return self

    @ChepyDecorators.call_stack
    def to_decimal(self):
        """Convert charactes to decimal
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("aㅎ").to_decimal().o
            [97, 12622]
        """
        self.state = list(ord(s) for s in list(self._convert_to_str()))
        return self

    @ChepyDecorators.call_stack
    def from_decimal(self):
        """Convert a list of decimal numbers to string
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy([12622]).from_decimal().o
            ["ㅎ"]
        """
        self.state = list(chr(int(s)) for s in self.state)
        return self

    @ChepyDecorators.call_stack
    def to_binary(self):
        """Convert string characters to binary
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("abc").to_binary().o
            ["01100001", "01100010", "01100011"]
        """
        self.state = list(format(ord(s), "08b") for s in list(self._convert_to_str()))
        return self

    @ChepyDecorators.call_stack
    def from_binary(self):
        """Convert a list of binary numbers to string
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy(["01100001", "01100010", "01100011"]).from_binary().o
            [
                "a",
                "b",
                "c",
            ]
        """
        if isinstance(self.state, list):
            self.state = list(chr(int(s, 2)) for s in self.state)
        else:
            n = int(self._convert_to_str(), 2)
            self.state = n.to_bytes((n.bit_length() + 7) // 8, "big")
        return self

    @ChepyDecorators.call_stack
    def to_octal(self):
        """Convert string characters to octal
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("abㅎ").to_octal().o
            ["141", "142", "30516"]
        """
        self.state = list(format(ord(s), "0o") for s in list(self._convert_to_str()))
        return self

    @ChepyDecorators.call_stack
    def from_octal(self):
        """Convert a list of octal numbers to string
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy(["141", "142", "30516"]).from_octal().o
            ["a", "b", "ㅎ"]
        """
        self.state = list(chr(int(str(s), 8)) for s in self.state)
        return self

    @ChepyDecorators.call_stack
    def to_html_entity(self):
        """Encode html entities

        Encode special html characters like & > < etc
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy('https://google.com&a="lol"').to_html_entity().o
            "https://google.com&amp;a=&quot;lol&quot;"
        """
        self.state = html.escape(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def from_html_entity(self):
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
    def to_punycode(self):
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
    def from_punycode(self):
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
    def encode_bruteforce(self):
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
    def decode_bruteforce(self):
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
    def to_braille(self):
        """Convery text to six-dot braille symbols
        
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
    def from_braille(self):
        """Convery text to six-dot braille symbols
        
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
    def trim(self):
        """Trim string. Removes whitespaces
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().strip()
        return self

