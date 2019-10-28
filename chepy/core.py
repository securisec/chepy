import re
import pathlib
from typing import Any
import pyperclip


class Core(object):
    def __init__(self, string: str, is_file: bool = False):
        self._holder = string
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
        else:
            # todo check more types here
            raise NotImplementedError

    def _remove_spaces(self):
        return re.sub(r"\s", "", self._holder)

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
