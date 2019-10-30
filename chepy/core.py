import pathlib
from typing import Any
import pyperclip
import regex as re


class Core(object):
    def __init__(self, input: str, is_file: bool = False):
        self._holder = input
        self.is_binary = is_file

        if is_file:
            path = pathlib.Path(self._holder).expanduser().absolute()
            try:
                with open(path, "r") as f:
                    self._holder = f.read()
            except UnicodeDecodeError:
                with open(path, "rb") as f:
                    self._holder = f.read()

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

    def int_to_hex(self):
        self._holder = format(self._convert_to_int(), "x")
        return self

    def _remove_spaces(self):
        return re.sub(r"\s", "", self._convert_to_str())

    # def __clean_hex(self):
    #     # TODO
    #     self.output = re.sub(r"\s|\\x", "", self.output)
    #     if '0x' in self._holder:
    #         return self._holder = self._holder.strip('0x')

    @property
    def output(self) -> Any:
        """Get the final output

        Returns
        -------
        Any
            Final output
        """
        return self.out()

    def out(self) -> Any:
        """Get the final output
        
        Returns
        -------
        Any
            Final output
        """
        return self._holder

    def copy_to_clipboard(self) -> None:
        """Copy the final output to the clipboard. If an 
        error is raised, refer to the documentation on the error.
        
        Returns
        -------
        None
            Copies final output to the clipboard
        """
        pyperclip.copy(self._holder)
        return None

    def write_to_file(self, file_path: str) -> None:
        # todo
        raise NotImplementedError

    def write_binary_to_file(self, file_path: str) -> None:
        # todo
        raise NotImplementedError

    def pipe(self):
        # todo
        return self._holder

    def __str__(self):
        return self._convert_to_str()
