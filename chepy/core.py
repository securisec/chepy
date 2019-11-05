import base64
import binascii
import pathlib
import webbrowser
import json as pyjson
import pyperclip
import requests
import regex as re
from typing import Any


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
        
        Returns:
            Any: Final output
        """
        return self._holder

    @property
    def output(self):
        """Get the final output
        
        Returns:
            Any: Final output
        """
        return self._holder

    def out(self) -> Any:
        """Get the final output
        
        Returns:
            Any: Final output
        """
        return self._holder

    def state(self) -> Any:
        """Get the current state. 
        
        Similar to `out()`, `output()` and `o`. Calling state and other complimentary 
        
        Returns:
            Any: Current output.
        """
        return self._holder

    def out_as_str(self) -> str:
        """Get current value as str
        
        Returns:
            str: Current value as a string
        """
        return self._convert_to_str()

    def out_as_bytes(self) -> bytes:
        """Get current value as bytes
        
        Returns:
            bytes: Current value as bytes
        """
        return self._convert_to_bytes()

    def copy_to_clipboard(self) -> None:
        """Copy to clipboard
        
        Copy the final output to the clipboard. If an 
        error is raised, refer to the documentation on the error.
        
        Returns:
            None: Copies final output to the clipboard
        """
        pyperclip.copy(self._convert_to_str())
        return None

    def copy(self) -> None:  # placeholder for documentation
        """Copy to clipboard
        
        Copy the final output to the clipboard. If an 
        error is raised, refer to the documentation on the error.
        
        Returns:
            None: Copies final output to the clipboard
        """
        self.copy_to_clipboard()
        return None

    def get_type(self) -> str:
        """Get the type of the data in state
        
        Returns:
            str: Type of the data in the state
        """
        return type(self._holder).__name__

    def web(self) -> None:  # place holder for documentation
        """Opens the current string in CyberChef on the browser as hex
        
        Returns:
            None: Opens the current data in CyberChef
        """
        data = re.sub(
            b"=", "", base64.b64encode(binascii.hexlify(self._convert_to_bytes()))
        )
        url = "https://gchq.github.io/CyberChef/#recipe=From_Hex('None')&input={}".format(
            data.decode()
        )
        webbrowser.open_new_tab(url)
        exit(0)
        return None

    def http_request(
        self,
        method: str = "GET",
        params: dict = {},
        json: dict = {},
        headers: dict = {},
        cookies: dict = {},
    ):
        """Get data from http request

        Make a HTTP/S request and work with the data in Chepy. All request 
        methods are supported; but some methods may not provide a response body. 
        
        Args:
            method (str, optional): Request method. Defaults to 'GET'.
            params (dict, optional): Query parameters. Defaults to {}.
            json (dict, optional): JSON request payload. Defaults to {}.
            headers (dict, optional): Headers for request. Defaults to {}.
            cookies (dict, optional): Cookies for request. Defaults to {}.
        
        Raises:
            NotImplementedError: If state is not a string or dictionary
            requests.RequestException: If response status code is not 200
        
        Returns:
            Chepy: The Chepy object.
        """

        def json2str(obj):
            if isinstance(obj, dict):
                return obj
            elif isinstance(obj, str):
                return pyjson.loads(obj)
            else:
                raise NotImplementedError

        params = json2str(params)
        json = json2str(json)
        headers = json2str(headers)
        cookies = json2str(cookies)
        res = requests.request(
            method=method,
            url=self._holder,
            params=params,
            json=json,
            headers=headers,
            cookies=cookies,
        )
        if res.status_code != 200:
            raise requests.RequestException(
                "Not a 200 status code {}".format(res.status_code)
            )
        else:
            self._holder = res.text
        return self

    # def write_to_file(self, file_path: str, as_binary: bool = False) -> None:
    #     # todo
    #     raise NotImplementedError
