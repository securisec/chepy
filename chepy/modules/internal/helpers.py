from typing import List, Union


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
        " ",
        ";",
        ".",
        "-",
        "\\",
        ":",
        "/",
        ",",
        "\n",
        "\\x",
        "\\0x",
    ],
    default_delimiter: str = " ",
) -> Union[str, bytes, None]:
    """Detect delimiter

    Args:
        data (Union[str, bytes]): Data
        delimiters (List[Union[str, bytes]], optional): Array of delimiters. Defaults to [" ", ";", ".", "-", "\"].
        default_delimiter (str): The default delimiter

    Returns:
        Union[str, bytes, None]: Delimiter or None if one is not found
    """
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
