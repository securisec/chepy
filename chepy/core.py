import base64
import binascii
import pathlib
from typing import Any
import pyperclip
import regex as re


class Baked(object):
    def __init__(self, data):
        self.holder = data

    @property
    def o(self):
        """Get the final output
        
        Returns
        -------
        Any
            Final output
        """
        return self.holder

    @property
    def output(self):
        """Get the final output
        
        Returns
        -------
        Any
            Final output
        """
        return self.holder

    def out(self) -> Any:
        """Get the final output
        
        Returns
        -------
        Any
            Final output
        """
        return self.holder

    def out_as_str(self) -> str:
        if isinstance(self.holder, bytes):
            return self.holder.decode()
        elif isinstance(self.holder, str):
            return self.holder
        elif isinstance(self.holder, int):
            return str(self.holder)
        else:
            # todo check more types here
            raise NotImplementedError

    def copy_to_clipboard(self) -> None:
        """Copy the final output to the clipboard. If an 
        error is raised, refer to the documentation on the error.
        
        Returns
        -------
        None
            Copies final output to the clipboard
        """
        pyperclip.copy(self.holder)
        return None

    def copy(self):
        """Copy the final output to the clipboard. If an 
        error is raised, refer to the documentation on the error.
        
        Returns
        -------
        None
            Copies final output to the clipboard
        """
        pyperclip.copy(self.holder)
        return None

    def write_to_file(self, file_path: str, as_binary: bool = False) -> None:
        # todo
        raise NotImplementedError


class Core(object):
    def __init__(self, data: str, is_file: bool = False):
        self._holder = data
        self.is_file = is_file
        # self.baked = Baked(self._holder)

        if self.is_file:
            path = pathlib.Path(self._holder).expanduser().absolute()
            try:
                with open(path, "r") as f:
                    self._holder = f.read()
            except UnicodeDecodeError:
                with open(path, "rb") as f:
                    self._holder = f.read()

    def __getattr__(self, i):
        return getattr(Baked(self._holder), i)

    def _is_bytes(self):
        return isinstance(self._holder, bytes)

    def _is_str(self):
        return isinstance(self._holder, str)

    def _convert_to_bytes(self):
        if isinstance(self._holder, bytes):
            return self._holder
        elif isinstance(self._holder, str):
            return self._holder.encode()
        elif isinstance(self._holder, int):
            return str(self._holder).encode()
        else:
            # todo check more types here
            raise NotImplementedError

    def _convert_to_bytearray(self):
        return bytearray(self._convert_to_bytes())

    def _convert_to_str(self):
        if isinstance(self._holder, bytes):
            return self._holder.decode()
        elif isinstance(self._holder, str):
            return self._holder
        elif isinstance(self._holder, int):
            return str(self._holder)
        else:
            # todo check more types here
            raise NotImplementedError

    def _convert_to_int(self):
        if isinstance(self._holder, int):
            return self._holder
        elif isinstance(self._holder, str) or isinstance(self._holder, bytes):
            return int(self._holder)
        else:
            raise NotImplementedError

    def to_int(self):
        self._holder = int(self._holder)
        return self

    def _remove_spaces(self):
        return re.sub(r"\s", "", self._convert_to_str())

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

    def str_to_hex(self) -> "Baked":
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    def int_to_hex(self):
        self._holder = format(self._convert_to_int(), "x")
        return self

    def binary_to_hex(self):
        self._holder = binascii.hexlify(self._convert_to_bytes())
        return self

    def hex_to_binary(self):
        self._holder = binascii.unhexlify(self._convert_to_bytes())
        return self

    def normalize_hex(self):
        assert r"\x" not in self._holder, "Cannot normalize binary data"
        delimiters = [" ", "0x", "%", ",", ";", ":", r"\\n", "\\r\\n"]
        string = re.sub("|".join(delimiters), "", self._holder)
        assert re.search(r"^[a-fA-F0-9]+$", string) is not None, "Invalid hex"
        self._holder = string
        return self

    def __str__(self):
        return self._convert_to_str()
