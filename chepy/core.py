import base64
import binascii
import pathlib
import webbrowser
import json as pyjson
import pyperclip
import requests
import logging
import inspect
import regex as re
from typing import Any, Tuple, List, Union

from .modules.exceptions import PrintException


class Core(object):
    def __init__(self, *data):
        self.states = dict(list(enumerate(data)))
        self._current_index = 0
        self.buffers = dict()

    @property
    def state(self):
        return self.states[self._current_index]

    @state.setter
    def state(self, val):
        self.states[self._current_index] = val

    def __str__(self):
        try:
            if isinstance(self.state, bytearray):
                return "bytearray in state"
            else:
                return self._convert_to_str()
        except:
            logging.exception(
                "\n\nCannot print current state. Either chain with "
                "another method, or use one of the output methods "
                "Example: .o, .output, .state or .out()\n\n"
            )
            return ""

    def fork(self, methods: List[Tuple[Union[str, object], dict]]):
        """Run multiple methods on all available states
        
        Args:
            methods (List[Tuple[Union[str, object], dict]]): Method names in a list
                of tuples.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            This method takes an array of method names and their args as an list of 
            tuples; the first value of the tuple is the method name as either a string, 
            or as an object, and the second value is a ditionary of arguments. 

            >>> from chepy import Chepy
            >>> c = Chepy("some", "data")
            >>> c.fork([("to_hex",), ("hmac_hash", {"secret_key": "key"})])
            >>> # this is how to use fork methods with a string
            >>> c.fork([(c.to_hex,), (c.hmac_hash, {"secret_key": "key"})])
            >>> # This is how to use fork using methods
            >>> print(c.states)
            {0: 'e46dfcf050c0a0d135b73856ab8e3298f9cc4105', 1: '1863d1542629590e3838543cbe3bf6a4f7c706ff'}
        """
        for i in self.states:
            self.change_state(i)
            for method in methods:
                if type(method[0]).__name__ == "method":
                    method_name = method[0].__name__
                elif isinstance(method[0], str):
                    method_name = method[0]
                if len(method) > 1:
                    self.states[i] = getattr(self, method_name)(**method[1]).o
                else:
                    self.states[i] = getattr(self, method_name)().o
        return self

    def create_state(self):
        """Create a new empty state
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.states[len(self.states)] = {}
        return self

    def copy_state(self, index: int):
        """Copy the current state to a new state
        
        Args:
            index (int): Index of new state
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.states[index] = self.states.get(self._current_index)
        return self

    def change_state(self, index: int):
        """Change current state by index
        
        Args:
            index (int): Index of new state
        
        Raises:
            TypeError: If specified index does not exist
        
        Returns:
            Chepy: The Chepy object.
        """
        if index > len(self.states):
            raise TypeError("Specified index does not exist")
        self._current_index = index
        return self

    def save_buffer(self, index: int = None):
        """Save current state in a buffer 

        Buffers are temporary holding areas for anything that is in the state. 
        The state can change, but the buffer does not. Can be chained with other 
        methods. Use in conjunction with `load_buffer` to load buffer back into 
        the state. 
        
        Args:
            index (int, optional): The index to save the state in, defaults to next index if None
        
        Returns:
            Chepy: The Chepy object. 
        """
        if index is not None:
            self.buffers[index] = self.state
        else:
            self.buffers[len(self.buffers)] = self.state
        return self

    def load_buffer(self, index: int):
        """Load the specified buffer into state
        
        Args:
            index (int): Index key of an existing buffer
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self.buffers[index]
        return self

    def subsection(self, pattern: str, group: int = 0):
        """Choose a subsection from current state as string 

        The preceeding methods will only run on the subsection and 
        not the original state. Group capture is supported. 
        
        Args:
            pattern (str): Pattern to match.
            group (int, optional): Group to match. Defaults to 0.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = re.search(pattern, self._convert_to_str()).group(group)
        return self

    def get_state(self, index: int) -> Any:
        """Returns the value of the specified state. 

        This method does not chain with other methods of Chepy
        
        Args:
            index (int): The index of the state
        
        Returns:
            Any: Any value that is in the specified state
        """
        return self.states.get(index)

    # def fork_state(self):
    #     # todo run methods on all states
    #     pass

    def _convert_to_bytes(self):
        if isinstance(self.state, bytes):
            return self.state
        elif isinstance(self.state, str):
            return self.state.encode()
        elif isinstance(self.state, int):
            return str(self.state).encode()
        elif isinstance(self.state, dict):
            return str(self.state).encode()
        elif isinstance(self.state, list):
            return str(self.state).encode()
        elif isinstance(self.state, bool):
            return str(self.state).encode()
        elif isinstance(self.state, bytearray):
            return bytes(self.state)
        else:
            # todo check more types here
            raise NotImplementedError

    def _convert_to_bytearray(self):
        return bytearray(self._convert_to_bytes())

    def _convert_to_str(self):
        if isinstance(self.state, bytes):
            return self.state.decode()
        elif isinstance(self.state, str):
            return self.state
        elif isinstance(self.state, int):
            return str(self.state)
        elif isinstance(self.state, dict):
            return str(self.state)
        elif isinstance(self.state, list):
            return str(self.state)
        elif isinstance(self.state, bool):
            return str(self.state)
        elif isinstance(self.state, bytearray):
            return bytearray(self.state).decode()
        else:
            # todo check more types here
            raise NotImplementedError

    def _convert_to_int(self):
        if isinstance(self.state, int):
            return self.state
        elif isinstance(self.state, str) or isinstance(self.state, bytes):
            return int(self.state)
        else:
            raise NotImplementedError

    @property
    def o(self):
        """Get the final output
        
        Returns:
            Any: Final output
        """
        return self.state

    @property
    def output(self):
        """Get the final output
        
        Returns:
            Any: Final output
        """
        return self.state

    def out(self) -> Any:
        """Get the final output
        
        Returns:
            Any: Final output
        """
        return self.state

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

    def get_by_index(self, index: int):
        """Get an item by specifying an index
        
        Args:
            index (int): Index number to get
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = self.state[index]
        return self

    def get_by_key(self, key: str):
        """Get an object from a dict by key
        
        Args:
            key (str): A valid key
        
        Returns:
            Chepy: The Chepy object.
        """
        if isinstance(self.state, dict):
            self.state = self.state.get(key)
            return self
        else:
            raise TypeError("State is not a dictionary")

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
        return type(self.state).__name__

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
        return None

    def http_request(
        self,
        method: str = "GET",
        params: dict = {},
        json: dict = None,
        headers: dict = {},
        cookies: dict = {},
    ):
        """Get data from http request

        Make a HTTP/S request and work with the data in Chepy. All request 
        methods are supported; but some methods may not provide a response body. 
        
        Args:
            method (str, optional): Request method. Defaults to 'GET'.
            params (dict, optional): Query Args. Defaults to {}.
            json (dict, optional): Request payload. Defaults to None.
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
        headers = json2str(headers)
        cookies = json2str(cookies)
        res = requests.request(
            method=method,
            url=self.state,
            params=params,
            json=json,
            headers=headers,
            cookies=cookies,
        )
        self.state = {
            "body": res.text,
            "status": res.status_code,
            "headers": res.headers,
        }
        return self

    def load_file(self):
        """If a path is provided, read the file
        
        Returns:
            Chepy: The Chepy object. 
        """
        path = pathlib.Path(self.state).expanduser().absolute()
        try:
            with open(path, "r") as f:
                self.states[self._current_index] = f.read()
        except UnicodeDecodeError:
            with open(path, "rb") as f:
                self.states[self._current_index] = bytearray(f.read())
        return self

    def write_to_file(self, file_path: str, as_binary: bool = False) -> None:
        """Save the state to disk
        
        Args:
            file_path (str): The file path to save in
            as_binary (bool, optional): If file should be saved as a binary file. Defaults to False.
        
        Returns:
            None: Returns None
        """
        path = pathlib.Path(file_path).expanduser().absolute()
        if as_binary:
            mode = "wb+"
        else:
            mode = "w+"
        with open(str(path), mode) as f:
            f.write(self.state)
        return None
