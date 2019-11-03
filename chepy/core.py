import base64
import binascii
import pathlib
import webbrowser
import pyperclip
from typing import Any
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
        elif isinstance(self.holder, dict):
            return str(self.holder)
        elif isinstance(self.holder, list):
            return str(self.holder)
        elif isinstance(self.holder, bool):
            return str(self.holder)
        else:
            # todo check more types here
            raise NotImplementedError

    def out_as_bytes(self):
        if isinstance(self.holder, bytes):
            return self.holder
        elif isinstance(self.holder, str):
            return self.holder.encode()
        elif isinstance(self.holder, int):
            return str(self.holder).encode()
        elif isinstance(self.holder, dict):
            return str(self.holder).encode()
        elif isinstance(self.holder, list):
            return str(self.holder).encode()
        elif isinstance(self.holder, bool):
            return str(self.holder).encode()
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

    def copy(self) -> None: # placeholder for documentation
        """Copy the final output to the clipboard. If an 
        error is raised, refer to the documentation on the error.
        
        Returns
        -------
        None
            Copies final output to the clipboard
        """
        return None

    def web(self) -> None: # place holder for documentation
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
        elif isinstance(self.holder, dict):
            return str(self._holder).encode()
        elif isinstance(self.holder, list):
            return str(self._holder).encode()
        elif isinstance(self.holder, bool):
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
        elif isinstance(self.holder, dict):
            return str(self._holder)
        elif isinstance(self.holder, list):
            return str(self._holder)
        elif isinstance(self.holder, bool):
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

    def copy(self) -> None:
        # DONT document
        pyperclip.copy(self._holder)
        return None

    def web(self) -> None:
        # DONT document
        data = re.sub(b"=", "", base64.b64encode(binascii.hexlify(self._convert_to_bytes())))
        print(data)
        url = "https://gchq.github.io/CyberChef/#recipe=From_Hex('None')&input={}".format(
            data.decode()
        )
        print(url)
        webbrowser.open_new_tab(url)
        return None

    def __str__(self):
        return self._convert_to_str()
