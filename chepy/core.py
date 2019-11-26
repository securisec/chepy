import base64
import binascii
import pathlib
import webbrowser
import pyperclip
import requests
import logging
import inspect
import jsonpickle
import ujson
import io
import regex as re
from typing import Any, Tuple, List, Union

from .modules.exceptions import PrintException

logging.getLogger().setLevel(logging.INFO)


class ChepyCore(object):
    """The `ChepyCore` class for Chepy is primarily used as an interface 
    for all the current modules/classes in Chepy, or for plugin development. 
    The `ChepyCore` class is what provides the various attributes like **states**, 
    **buffers**, etc and is required to use and extend Chepy.
    
    Args:
        \*data (tuple): The core class takes arbitrary number of arguments as \*args.

    Attributes:
        states (dict): Contains all the current states. Each arg passed to 
            the ChepyCore class will be considered a state.
        buffers (dict): Contains all the current buffers if a buffer is saved. 
        state (Any): The data in the current state. The state changes each time a 
            Chepy method is called. 
    
    Returns:
        Chepy: The Chepy object. 
    """

    def __init__(self, *data):
        self.states = dict(list(enumerate(data)))
        self._current_index = 0
        self.buffers = dict()
        #: Alias for `write_to_file`
        self.write = self.write_to_file
        #: Alias for `out`
        self.bake = self.out
        #: Alias for `web`
        self.cyberchef = self.web

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
        except UnicodeDecodeError:  # pragma: no cover
            return "Could not convert to str, but the data exists in the states. Use o, output or out() to access the values"
        except:  # pragma: no cover
            logging.exception(
                "\n\nCannot print current state. Either chain with "
                "another method, or use one of the output methods "
                "Example: .o, .output, .state or .out()\n\n"
            )
            return ""

    def _pickle_class(self, obj: Any) -> Any:
        """This method takes another object as an argument and 
        pickels that into a json object using jsonpickel. The 
        return value is a dictionary
        
        Args:
            obj (Any): Any object
        
        Returns:
            Any: unpickeled JSON as a python object. 
        """
        return ujson.loads(jsonpickle.encode(obj, unpicklable=True))

    def _load_as_file(self) -> object:
        """This method is used when a function or a method expects 
        a file path to load a file. Instead of passing a file path, 
        this method allows passing an io.BytesIO object instead.
        
        Returns:
            object: io.BytesIO object
        """
        return io.BytesIO(self._convert_to_bytes())

    def _abs_path(self, path: str) -> str:
        """Returns the absolute path by expanding home dir
        
        Args:
            path (str): Path to expand
        
        Returns:
            str: Expanded absolute path
        """
        return str(pathlib.Path(path).expanduser().absolute())

    def _info_logger(self, data: str) -> None:
        """Just a binding for logger.info
        
        Args:
            data (str): Message to log
        
        Returns:
            Chepy: The Chepy object. 
        """
        logging.info(data)
        return None

    def fork(self, methods: List[Tuple[Union[str, object], dict]]):
        """Run multiple methods on all available states
        
        Method names in a list of tuples. If using in the cli, 
        this should not contain any spaces.

        Args:
            methods (List[Tuple[Union[str, object], dict]]): Required. 
                List of tuples
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            This method takes an array of method names and their args as an list of 
            tuples; the first value of the tuple is the method name as either a string, 
            or as an object, and the second value is a ditionary of arguments. The keys of 
            in the dictionary are method argument names, while the values are argument 
            values.

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

    def set_state(self, data: Any):
        """Set any arbitrary values in the current state

        This method is simply changing the value of the instantiated 
        state with an arbitrary value. 
        
        Args:
            data (Any): Any data type
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("some data")
            >>> print(c.state)
            some data
            >>> c.set_state("New data")
            >>> print(c.state)
            New data
        """
        self.state = data
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

        Same behaviour as switch_state
        
        Args:
            index (int): Index of new state
        
        Raises:
            TypeError: If specified index does not exist
        
        Returns:
            Chepy: The Chepy object.
        """
        if index > len(self.states):  # pragma: no cover
            raise TypeError("Specified index does not exist")
        self._current_index = index
        return self

    def switch_state(self, index: int):  # pragma: no cover
        """Switch current state by index

        Same behaviour as change_state
        
        Args:
            index (int): Index of new state
        
        Raises:
            TypeError: If specified index does not exist
        
        Returns:
            Chepy: The Chepy object.
        """
        if index > len(self.states):  # pragma: no cover
            raise TypeError("Specified index does not exist")
        self._current_index = index
        return self

    def delete_state(self, index: int):
        """Delete a state specified by the index
        
        Args:
            index (int): Index of state
        
        Returns:
            Chepy: The Chepy object. 
        """
        try:
            del self.states[index]
        except KeyError:  # pragma: no cover
            logging.warning("{} does not exist".format(index))
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

        Examples:
            >>> c = Chepy("A").save_buffer()
            >>> # this saves the current value of state to a new buffer
            >>> c.to_hex()
            >>> # operate on a state, in this case, convert to hex.
            >>> c.state
            "41"
            >>> c.buffers
            {0: "A"}
            >>> c.load_buffer(0)
            >>> # loads the content of the buffer back into the current state. 
            >>> c.state
            "A"
        """
        self.state = self.buffers[index]
        return self

    def delete_buffer(self, index: int):
        """Delete a buffer item
        
        Args:
            index (int): Key of buffer item
        
        Returns:
            Chepy: The Chepy object. 
        """
        try:
            del self.buffers[index]
        except KeyError:  # pragma: no cover
            logging.warning("{} does not exist".format(index))
        return self

    def substring(self, pattern: str, group: int = 0):
        """Choose a substring from current state as string 

        The preceeding methods will only run on the substring and 
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

    def _convert_to_bytes(self) -> None:
        """This method is used to coerce the curret object in 
        the state variable into a string. The method should be 
        called inside any method that operates on a string object 
        instead of calling `self.state` directly to avoid errors. 
        
        Raises:
            NotImplementedError: If type coercian isnt available 
                for the current state type.
        """
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
        elif isinstance(self.state, bool):  # pragma: no cover
            return str(self.state).encode()
        elif isinstance(self.state, bytearray):
            return bytes(self.state)
        else:  # pragma: no cover
            # todo check more types here
            raise NotImplementedError

    def _convert_to_bytearray(self):
        """Attempts to coerce the current state into a 
        `bytesarray` object
        """
        return bytearray(self._convert_to_bytes())

    def _convert_to_str(self):
        """This method is used to coerce the curret object in 
        the state variable into bytes. The method should be 
        called inside any method that operates on a bytes object 
        instead of calling `self.state` directly to avoid errors. 
        
        Raises:
            NotImplementedError: If type coercian isnt available 
                for the current state type.
        """
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
        elif isinstance(self.state, bool):  # pragma: no cover
            return str(self.state)
        elif isinstance(self.state, bytearray):
            return bytearray(self.state).decode()
        else:  # pragma: no cover
            # todo check more types here
            raise NotImplementedError

    def _convert_to_int(self):
        """This method is used to coerce the curret object in 
        the state variable into an int. The method should be 
        called inside any method that operates on a int types 
        instead of calling `self.state` directly to avoid errors. 
        
        Raises:
            NotImplementedError: If type coercian isnt available 
                for the current state type.
        """
        if isinstance(self.state, int):
            return self.state
        elif isinstance(self.state, str) or isinstance(self.state, bytes):
            return int(self.state)
        else:  # pragma: no cover
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
        else:  # pragma: no cover
            raise TypeError("State is not a dictionary")

    def copy_to_clipboard(self) -> None:  # pragma: no cover
        """Copy to clipboard
        
        Copy the final output to the clipboard. If an 
        error is raised, refer to the documentation on the error.
        
        Returns:
            None: Copies final output to the clipboard
        """
        pyperclip.copy(self._convert_to_str())
        return None

    def copy(self) -> None:  # pragma: no cover
        """Copy to clipboard
        
        Copy the final output to the clipboard. If an 
        error is raised, refer to the documentation on the error.
        
        Returns:
            None: Copies final output to the clipboard
        """
        self.copy_to_clipboard()
        return None

    def web(self, magic: bool = False) -> None:  # pragma: no cover
        """Opens the current string in CyberChef on the browser as hex

        Args:
            magic (bool, optional): Start with the magic method in CyberChef
        
        Returns:
            None: Opens the current data in CyberChef
        """
        data = re.sub(
            b"=", "", base64.b64encode(binascii.hexlify(self._convert_to_bytes()))
        )
        if magic:
            url = "https://gchq.github.io/CyberChef/#recipe=From_Hex('None')Magic(3,false,false,'')&input={}".format(
                data.decode()
            )
        else:
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

        Make a HTTP/S request and work with the data in Chepy. Most common http 
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
            Chepy: A dictionary containing body, status and headers. The Chepy object.

        Examples:
            By default, this methed with make a GET request, But supports most 
            common methods. 
            
                >>> c = Chepy("http://example.com").http_request()
                >>> c.get_by_key("headers")

            This method can also be used to make more complex requests by specifying 
            headers, cookies, body data etc.

                >>> c = Chepy("https://en4qpftrmznwq.x.pipedream.net")
                >>> c.http_request(
                >>>    method="POST", 
                >>>    headers={"My-header": "some header"}, 
                >>>    json={"some": "data"}
                >>> )
                >>> print(c.get_by_key("body"))
                {"success": true}
        """

        def json2str(obj):  # pragma: no cover
            if isinstance(obj, dict):
                return obj
            elif isinstance(obj, str):
                return json.loads(obj)
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

    def load_dir(self, pattern: str = "*"):
        """Load all file paths in a directory
        
        Args:
            pattern (str, optional): File pattern to match. Defaults to "*".
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.states = {
            x[0]: str(x[1])
            for x in enumerate(pathlib.Path(self.state).glob(pattern))
            if x[1].is_file()
        }
        return self

    def load_file(self):
        """If a path is provided, read the file
        
        Returns:
            Chepy: The Chepy object. 
        
        Examples:
            >>> c = Chepy("/path/to/file")
            >>> # at the moment, the state only contains the string "/path/to/file"
            >>> c.load_file() # this will load the file content into the state
        """
        path = pathlib.Path(self.state).expanduser().absolute()
        try:
            with open(path, "r") as f:
                self.states[self._current_index] = f.read()
        except UnicodeDecodeError:
            with open(path, "rb") as f:
                self.states[self._current_index] = bytearray(f.read())
        return self

    def read_file(self):
        """If a path is provided, read the file 

        Alias of `load_file`.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.load_file()
        return self

    def write_to_file(self, file_path: str, as_binary: bool = False) -> None:
        """Save the state to disk. Return None.
        
        Args:
            file_path (str): The file path to save in.
            as_binary (bool, optional): If file should be saved as a binary file. Defaults to False.
        
        Returns:
            None: Returns None

        Examples:
            >>> c = Chepy("some data").write_to_file('/some/path/file', as_binary=True)
            >>> # use the alias
            >>> c = Chepy("some data").write('/some/path/file', as_binary=True)
        """
        if as_binary:
            mode = "wb+"
        else:
            mode = "w+"
        with open(str(self._abs_path(file_path)), mode) as f:
            f.write(self.state)
        self._info_logger("File written to {}".format(self._abs_path(file_path)))
        return None

    def write_binary(self, file_path: str) -> None:  # pragma: no cover
        """Save the state to disk. Return None.
        
        Args:
            file_path (str): The file path to save in.
        
        Returns:
            None: Returns None

        Examples:
            >>> c = Chepy("some data").write_binary('/some/path/file')
        """
        with open(str(self._abs_path(file_path)), "wb+") as f:
            f.write(self.state)
        self._info_logger("File written to {}".format(self._abs_path(file_path)))
        return None
