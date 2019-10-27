import binascii
import codecs
import string
import base64
import re
import pathlib


class Chepy(object):
    def __init__(self, string: str, is_file: bool = False):
        self.output = string
        self.is_binary = is_file

        if is_file:
            path = pathlib.Path(self.output).expanduser().absolute()
            try:
                with open(path, "r") as f:
                    self.output = f.read()
            except UnicodeDecodeError:
                with open(path, "rb") as f:
                    self.output = f.read()

    def __is_bytes(self):
        return isinstance(self.output, bytes)

    def __is_str(self):
        return isinstance(self.output, str)

    def __convert_to_bytes(self):
        if isinstance(self.output, bytes):
            return self.output
        elif isinstance(self.output, str):
            return self.output.encode()
        else:
            # todo check more types here
            raise NotImplementedError

    @property
    def reverse(self) -> "Chepy":
        # todo by line
        self.output = self.output[::-1]
        return self

    def rotate(self, rotate_by: int) -> "Chepy":
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        lookup = str.maketrans(
            lc + uc, lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by]
        )
        self.output = self.output.translate(lookup)
        return self

    @property
    def rot_13(self) -> "Chepy":
        self.output = codecs.encode(self.output, "rot_13")
        return self

    @property
    def rot_47(self) -> "Chepy":
        x = []
        for i in range(len(self.output)):
            j = ord(self.output[i])
            if j >= 33 and j <= 126:
                x.append(chr(33 + ((j + 14) % 94)))
            else:
                x.append(self.output[i])
        self.output = "".join(x)
        return self

    @property
    def base_32_encode(self) -> "Chepy":
        self.output = base64.b32encode(self.__convert_to_bytes())
        return self

    @property
    def base_64_encode(self) -> "Chepy":
        self.output = base64.b64encode(self.__convert_to_bytes())
        return self

    @property
    def base_32_decode(self) -> "Chepy":
        self.output = base64.b32decode(self.output)
        return self

    @property
    def base_64_decode(self) -> "Chepy":
        self.output = base64.b64decode(self.output)
        return self

    @property
    def string_from_hexdump(self) -> "Chepy":
        if self.__is_bytes():
            data = self.output.decode()
        else:
            data = self.output
        self.output = "".join(re.findall(r"\|(.+)\|", data))
        return self
