import base64
import binascii
import pathlib
import webbrowser
import pyperclip
from typing import Any
import regex as re


class Core(object):
    def __init__(self, data: str, is_file: bool = False):
        self._holder = data
        self._is_file = is_file

        if self._is_file:
            path = pathlib.Path(self._holder).expanduser().absolute()
            try:
                with open(path, "r") as f:
                    self._holder = f.read()
            except UnicodeDecodeError:
                with open(path, "rb") as f:
                    self._holder = f.read()

    def __str__(self):
        return self._convert_to_str()

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
        elif isinstance(self._holder, dict):
            return str(self._holder).encode()
        elif isinstance(self._holder, list):
            return str(self._holder).encode()
        elif isinstance(self._holder, bool):
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
        elif isinstance(self._holder, dict):
            return str(self._holder)
        elif isinstance(self._holder, list):
            return str(self._holder)
        elif isinstance(self._holder, bool):
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

    def _remove_spaces(self):
        return re.sub(r"\s", "", self._convert_to_str())

    @property
    def o(self):
        """Get the final output
        
        Returns
        -------
        Any
            Final output
        """
        return self._holder

    @property
    def output(self):
        """Get the final output
        
        Returns
        -------
        Any
            Final output
        """
        return self._holder

    def out(self) -> Any:
        """Get the final output
        
        Returns
        -------
        Any
            Final output
        """
        return self._holder

    def out_as_str(self) -> str:
        """Returns the current value as a string
        
        Returns
        -------
        str
            Current value as a string
        """
        return self._convert_to_str()

    def out_as_bytes(self) -> bytes:
        """Returns the current value as bytes
        
        Returns
        -------
        bytes
            Current value as bytes
        """
        return self._convert_to_bytes()

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

    def copy(self) -> None:  # placeholder for documentation
        """Copy the final output to the clipboard. If an 
        error is raised, refer to the documentation on the error.
        
        Returns
        -------
        None
            Copies final output to the clipboard
        """
        return None

    def web(self) -> None:  # place holder for documentation
        """Opens the current string in CyberChef on the browser as hex
        
        Returns
        -------
        None
            Opens the current data in CyberChef
        """
        return None

    def write_to_file(self, file_path: str, as_binary: bool = False) -> None:
        # todo
        raise NotImplementedError
