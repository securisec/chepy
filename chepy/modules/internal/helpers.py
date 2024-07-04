from typing import List, Union
import binascii
import regex as re


class Base45:
    # reference: https://github.com/kirei/python-base45/blob/main/base45/__init__.py
    def __init__(self) -> None:
        self.BASE45_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
        self.BASE45_DICT = {v: i for i, v in enumerate(self.BASE45_CHARSET)}

    def b45encode(self, buf: bytes) -> bytes:
        """Convert bytes to base45-encoded string"""
        res = ""
        buflen = len(buf)
        for i in range(0, buflen & ~1, 2):
            x = (buf[i] << 8) + buf[i + 1]
            e, x = divmod(x, 45 * 45)
            d, c = divmod(x, 45)
            res += (
                self.BASE45_CHARSET[c] + self.BASE45_CHARSET[d] + self.BASE45_CHARSET[e]
            )
        if buflen & 1:
            d, c = divmod(buf[-1], 45)
            res += self.BASE45_CHARSET[c] + self.BASE45_CHARSET[d]
        return res.encode()

    def b45decode(self, s: Union[bytes, str]) -> bytes:
        """Decode base45-encoded string to bytes"""
        try:
            if isinstance(s, str):  # pragma: no cover
                buf = [self.BASE45_DICT[c] for c in s.rstrip("\n")]
            elif isinstance(s, bytes):
                buf = [self.BASE45_DICT[c] for c in s.decode()]
            else:  # pragma: no cover
                raise TypeError("Type must be 'str' or 'bytes'")

            buflen = len(buf)
            if buflen % 3 == 1:  # pragma: no cover
                raise ValueError("Invalid base45 string")

            res = []
            for i in range(0, buflen, 3):
                if buflen - i >= 3:
                    x = buf[i] + buf[i + 1] * 45 + buf[i + 2] * 45 * 45
                    if x > 0xFFFF:  # pragma: no cover
                        raise ValueError
                    res.extend(divmod(x, 256))
                else:
                    x = buf[i] + buf[i + 1] * 45
                    if x > 0xFF:  # pragma: no cover
                        raise ValueError
                    res.append(x)
            return bytes(res)
        except (ValueError, KeyError, AttributeError):  # pragma: no cover
            raise ValueError("Invalid base45 string")


class Base92(object):
    """
    Reference: https://github.com/Gu-f/py3base92/tree/master
    """

    CHARACTER_SET = r"!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}"

    @classmethod
    def base92_chr(cls, val):
        if val < 0 or val >= 91:  # pragma: no cover
            raise ValueError("val must be in [0, 91)")
        if val == 0:
            return "!"  # pragma: no cover
        elif val <= 61:
            return chr(ord("#") + val - 1)
        else:
            return chr(ord("a") + val - 62)

    @classmethod
    def base92_ord(cls, val):
        num = ord(val)
        if val == "!":
            return 0  # pragma: no cover
        elif ord("#") <= num and num <= ord("_"):
            return num - ord("#") + 1
        elif ord("a") <= num and num <= ord("}"):
            return num - ord("a") + 62
        else:  # pragma: no cover
            raise ValueError("val is not a base92 character")

    @classmethod
    def b92encode(cls, byt: bytes) -> str:
        if not isinstance(byt, bytes):  # pragma: no cover
            raise TypeError(f"a bytes-like object is required, not '{type(byt)}'")
        if not byt:
            return "~"
        if not isinstance(byt, str):
            byt = "".join([chr(b) for b in byt])
        bitstr = ""
        while len(bitstr) < 13 and byt:
            bitstr += "{:08b}".format(ord(byt[0]))
            byt = byt[1:]
        resstr = ""
        while len(bitstr) > 13 or byt:
            i = int(bitstr[:13], 2)
            resstr += cls.base92_chr(i // 91)
            resstr += cls.base92_chr(i % 91)
            bitstr = bitstr[13:]
            while len(bitstr) < 13 and byt:
                bitstr += "{:08b}".format(ord(byt[0]))
                byt = byt[1:]

        if bitstr:
            if len(bitstr) < 7:
                bitstr += "0" * (6 - len(bitstr))
                resstr += cls.base92_chr(int(bitstr, 2))
            else:  # pragma: no cover
                bitstr += "0" * (13 - len(bitstr))
                i = int(bitstr, 2)
                resstr += cls.base92_chr(i // 91)
                resstr += cls.base92_chr(i % 91)
        return resstr

    @classmethod
    def b92decode(cls, bstr: str) -> bytes:
        if not isinstance(bstr, str):  # pragma: no cover
            raise TypeError(f"a str object is required, not '{type(bstr)}'")
        bitstr = ""
        resstr = ""
        if bstr == "~":
            return "".encode(encoding="latin-1")

        for i in range(len(bstr) // 2):
            x = cls.base92_ord(bstr[2 * i]) * 91 + cls.base92_ord(bstr[2 * i + 1])
            bitstr += "{:013b}".format(x)
            while 8 <= len(bitstr):
                resstr += chr(int(bitstr[0:8], 2))
                bitstr = bitstr[8:]
        if len(bstr) % 2 == 1:
            x = cls.base92_ord(bstr[-1])
            bitstr += "{:06b}".format(x)
            while 8 <= len(bitstr):
                resstr += chr(int(bitstr[0:8], 2))
                bitstr = bitstr[8:]
        return resstr.encode(encoding="latin-1")


class LZ77Compressor:
    """
    Class containing compress and decompress methods using LZ77 compression algorithm.
    Reference: https://the-algorithms.com/algorithm/lz-77?lang=python
    """

    def __init__(self, window_size: int = 13, lookahead_buffer_size: int = 6) -> None:
        self.window_size = window_size
        self.lookahead_buffer_size = lookahead_buffer_size
        self.search_buffer_size = self.window_size - self.lookahead_buffer_size

    def compress(self, text: str) -> list:
        output = []
        search_buffer = ""

        while text:
            token = self._find_encoding_token(text, search_buffer)

            search_buffer += text[: token[1] + 1]
            if len(search_buffer) > self.search_buffer_size:
                search_buffer = search_buffer[-self.search_buffer_size :]

            text = text[token[1] + 1 :]

            output.append(token)

        return output

    def decompress(self, tokens: list) -> str:
        output = ""

        for token in tokens:
            for _ in range(token[1]):
                output += output[-token[0]]
            output += token[2]

        return output

    def _find_encoding_token(self, text: str, search_buffer: str):
        if not text:
            raise ValueError("We need some text to work with.")  # pragma: no cover

        length, offset = 0, 0

        if not search_buffer:
            return [offset, length, text[length]]

        for i, character in enumerate(search_buffer):  # pragma: no cover
            found_offset = len(search_buffer) - i
            if character == text[0]:
                found_length = self._match_length_from_index(text, search_buffer, 0, i)
                if found_length >= length:
                    offset, length = found_offset, found_length

        return [offset, length, text[length]]  # pragma: no cover

    def _match_length_from_index(
        self, text: str, window: str, text_index: int, window_index: int
    ) -> int:
        if not text or text[text_index] != window[window_index]:  # pragma: no cover
            return 0
        return 1 + self._match_length_from_index(
            text, window + text[text_index], text_index + 1, window_index + 1
        )  # pragma: no cover


class UUEncoderDecoder:
    def __init__(self, data: bytes, header: str = "-"):
        self.data = data
        self.header = header

    def split_data(self, data, chunk_size=45):
        for i in range(0, len(data), chunk_size):
            yield self.data[i : i + chunk_size]

    def uuencode(self):
        encoded_chunks = []
        for chunk in self.split_data(self.data):
            encoded_data = binascii.b2a_uu(chunk)
            encoded_chunks.append(encoded_data.decode("utf-8"))

        # UUencode header and footer
        header = f"begin 644 {self.header}\n"
        footer = " \nend\n"

        return header + "\n".join(encoded_chunks) + footer

    def uudecode(self):
        lines = self.data.strip().split(b"\n")
        if len(lines) < 3 or b"begin 644" not in lines[0].lower():  # pragma: no cover
            raise ValueError("Invalid UUencode format. Missing header")

        data_lines = lines[1:-1]  # Remove header and footer

        decoded_data = []
        for line in data_lines:
            decoded_chunk = binascii.a2b_uu(line)
            decoded_data.append(decoded_chunk)

        return b"".join(decoded_data)


class Uint1Array:
    # reference https://git.sr.ht/~evanhahn/UTF-21.js
    def __init__(self, bit_length_or_buffer):
        if isinstance(bit_length_or_buffer, int):
            bit_length = bit_length_or_buffer
            self.bit_length = bit_length
            self.bytes = bytearray((bit_length + 7) // 8)
        else:
            buffer = bit_length_or_buffer
            self.bit_length = len(buffer) * 8
            self.bytes = bytearray(buffer)

    @property
    def buffer(self):
        return bytes(self.bytes)

    def get(self, index):
        byte_index = index // 8
        bit_index = index % 8
        byte = self.bytes[byte_index]
        return (byte >> (7 - bit_index)) & 1

    def set(self, index, value):
        byte_index = index // 8
        bit_index = index % 8
        old_byte = self.bytes[byte_index]
        new_byte = old_byte | (value << (7 - bit_index))
        self.bytes[byte_index] = new_byte


def detect_delimiter(
    data: Union[str, bytes],
    delimiters: List[Union[str, bytes]] = [
        "; ",
        ";",
        ". ",
        ".",
        "- ",
        "-",
        "\\",
        ": ",
        ":",
        "/",
        ", ",
        ",",
        " ",
        "\n",
        "\\x",
        "\\0x",
    ],
    default_delimiter: str = "",
) -> Union[str, bytes, None]:
    """Detect delimiter

    Args:
        data (Union[str, bytes]): Data
        delimiters (List[Union[str, bytes]], optional): Array of delimiters. Defaults to [" ", ";", ".", "-", "\"].
        default_delimiter (str): The default delimiter

    Returns:
        Union[str, bytes, None]: Delimiter or None if one is not found
    """
    if default_delimiter:
        return default_delimiter

    is_bytes = False
    if isinstance(data, bytes):  # pragma: no cover
        delimiters = [d.encode() for d in delimiters]
        is_bytes = True

    for delimiter in delimiters:
        parts = data.split(delimiter)
        if len(parts) > 1 and all(part.strip() for part in parts):
            return delimiter

    if default_delimiter:  # pragma: no cover
        return default_delimiter.encode() if is_bytes else default_delimiter
    else:
        return None


class Rotate:
    def __init__(self, data: bytes, radix: int):
        self.data = data
        self.radix = radix

    def rot(self, algo):
        result = []
        for byte in self.data:
            b = byte
            for _ in range(self.radix):
                b = algo(b)
            result.append(b)
        return b"".join([chr(x).encode() for x in result])

    def rot_right_carry(self):
        result = []
        carryBits = 0

        amount = self.radix % 8
        for i in range(len(self.data)):
            oldByte = self.data[i] & 0xFF  # Ensure it's treated as an unsigned byte
            newByte = (oldByte >> amount) | carryBits
            carryBits = (oldByte & ((1 << amount) - 1)) << (8 - amount)
            result.append(newByte)

        result[0] |= carryBits
        return b"".join([chr(x).encode() for x in result])

    @staticmethod
    def rotate_right(b):
        bit = (b & 1) << 7
        return (b >> 1) | bit

    @staticmethod
    def rotate_left(b):
        bit = (b >> 7) & 1
        return ((b << 1) | bit) & 0xFF

    def rotate_left_carry(self):
        result = bytearray(len(self.data))
        carryBits = 0

        amount = self.radix % 8
        for i in range(len(self.data) - 1, -1, -1):
            oldByte = self.data[i]
            newByte = ((oldByte << amount) | carryBits) & 0xFF
            carryBits = (oldByte >> (8 - amount)) & ((1 << amount) - 1)
            result[i] = newByte

        result[-1] |= carryBits

        return b"".join([chr(x).encode() for x in result])


class _Base64:
    base_64_chars = {
        "standard": "A-Za-z0-9+/=",
        "url_safe": "A-Za-z0-9-_",
        "filename_safe": "A-Za-z0-9+\\-=",
        "itoa64": "./0-9A-Za-z=",
        "xml": "A-Za-z0-9_.",
        # "y64": "A-Za-z0-9._-",
        "z64": "0-9a-zA-Z+/=",
        "radix_64": "0-9A-Za-z+/=",
        # "uuencoding": " -_",
        "xxencoding": "+\\-0-9A-Za-z",
        # "binHex": "!-,-0-689@A-NP-VX-Z[`a-fh-mp-r",
        "rot13": "N-ZA-Mn-za-m0-9+/=",
        "unix_crypt": "./0-9A-Za-z",
        # "atom128": "/128GhIoPQROSTeUbADfgHijKLM+n0pFWXY456xyzB7=39VaqrstJklmNuZvwcdEC",
        # "megan35": "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5",
        # "zong22": "ZKj9n+yf0wDVX1s/5YbdxSo=ILaUpPBCHg8uvNO4klm6iJGhQ7eFrWczAMEq3RTt2",
        # "hazz15": "HNO4klm6ij9n+J2hyf0gzA8uvwDEq3X1Q7ZKeFrWcVTts/MRGYbdxSo=ILaUpPBC5",
    }

    @staticmethod
    def decode_base64(data, alphabet):
        output = []
        i = 0

        # Calculate the necessary padding
        padding_required = (4 - len(data) % 4) % 4
        data += padding_required * "="

        while i < len(data):
            enc1 = alphabet.index(data[i]) if i < len(data) and data[i] != "=" else 0
            i += 1
            enc2 = alphabet.index(data[i]) if i < len(data) and data[i] != "=" else 0
            i += 1
            enc3 = alphabet.index(data[i]) if i < len(data) and data[i] != "=" else 0
            i += 1
            enc4 = alphabet.index(data[i]) if i < len(data) and data[i] != "=" else 0
            i += 1

            chr1 = (enc1 << 2) | (enc2 >> 4)
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2)
            chr3 = ((enc3 & 3) << 6) | enc4

            if 0 <= chr1 < 256:
                output.append(chr1)
            if 0 <= chr2 < 256 and data[i - 2] != "=":
                output.append(chr2)
            if 0 <= chr3 < 256 and data[i - 1] != "=":
                output.append(chr3)

        return bytes(output)

    @staticmethod
    def encode_base64(data: bytes, alphabet: str):
        output = ""
        i = 0
        padding_char = (
            "=" if alphabet[-1] == "=" else None
        )  # Check if '=' is in the alphabet, otherwise use None

        while i < len(data):
            chr1 = data[i] if i < len(data) else 0
            i += 1
            chr2 = data[i] if i < len(data) else 0
            i += 1
            chr3 = data[i] if i < len(data) else 0
            i += 1

            enc1 = chr1 >> 2
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
            enc4 = chr3 & 63

            if i > len(data) + 1:
                enc3 = 64
                enc4 = 64
            elif i > len(data):
                enc4 = 64

            output += alphabet[enc1]
            output += alphabet[enc2]
            output += (
                alphabet[enc3]
                if enc3 < 64
                else (padding_char if padding_char is not None else "")
            )
            output += (
                alphabet[enc4]
                if enc4 < 64
                else (padding_char if padding_char is not None else "")
            )

        # Remove padding characters if they are not part of the alphabet
        if padding_char is None:
            output = output.rstrip(
                alphabet[-1]
            )  # Strip the last character of the alphabet if it's not '='

        return output


def expand_alpha_range(alph_str: str, join_by: Union[str, None] = None):
    def expand_range(start, end):
        return [str(x) for x in range(int(start), int(end) + 1)]

    def expand_char_range(start, end):
        return [chr(x) for x in range(ord(start), ord(end) + 1)]

    hold = []
    i = 0
    length = len(alph_str)

    while i < length:
        # Check for numeric ranges
        if (
            i < length - 2
            and alph_str[i].isdigit()
            and alph_str[i + 1] == "-"
            and alph_str[i + 2].isdigit()
        ):
            start = ""
            while i < length and alph_str[i].isdigit():
                start += alph_str[i]
                i += 1
            i += 1  # Skip the '-'
            end = ""
            while i < length and alph_str[i].isdigit():
                end += alph_str[i]
                i += 1
            hold.extend(expand_range(start, end))
        elif (
            i < length - 2
            and alph_str[i].isalpha()
            and alph_str[i + 1] == "-"
            and alph_str[i + 2].isalpha()
        ):
            start = alph_str[i]
            end = alph_str[i + 2]
            hold.extend(expand_char_range(start, end))
            i += 3
        elif (
            i < length - 2 and alph_str[i] == "\\" and alph_str[i + 1] == "-"
        ):  # pragma: no cover
            hold.append("-")
            i += 2
        else:
            hold.append(alph_str[i])
            i += 1

    if join_by is not None:
        return join_by.join(hold)
    return hold
