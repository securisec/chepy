import base64
import binascii
import inspect
import io
import itertools
import logging
from pathlib import Path
import subprocess
import sys
import struct
import webbrowser
from configparser import ConfigParser
from importlib.machinery import SourceFileLoader
from pprint import pformat
from typing import Any, Dict, List, Mapping, Tuple, Union, Callable
from urllib.parse import urljoin

import lazy_import
import pyperclip
import json
import jmespath

jsonpickle = lazy_import.lazy_module("jsonpickle")
import regex as re
from decorator import decorator

from .modules.internal.colors import blue, cyan, green, magenta, red, yellow


class ChepyDecorators(object):
    """A class to house all the decorators for Chepy"""

    @staticmethod
    @decorator
    def call_stack(func, *args, **kwargs):
        """This decorator is used to get the method name and
        arguments and save it to self.stack. The data from
        self.stack is predominantly used to save recepies.
        """
        func_sig = dict()
        func_self = args[0]
        func_sig["function"] = func.__name__

        bound_args = inspect.signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()

        func_arguments = dict(bound_args.arguments)
        del func_arguments["self"]
        func_sig["args"] = func_arguments
        func_self._stack.append(func_sig)

        return func(*args, **kwargs)  # lgtm [py/call-to-non-callable]

    @staticmethod
    @decorator
    def is_stdout(func, *args, **kwargs):  # pragma: no cover
        """Detect if method is being called from the cli"""
        if sys.stdout.isatty():
            logging.warning(f"{func.__name__} may not work as expected on the cli")
        return func(*args, **kwargs)


class ChepyCore(object):
    """The ChepyCore class for Chepy is primarily used as an interface
    for all the current modules/classes in Chepy, or for plugin development.
    The `ChepyCore` class is what provides the various attributes like **states**,
    **buffers**, etc and is required to use and extend Chepy.

    Args:
        *data (tuple): The core class takes arbitrary number of arguments as *args.

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
        #: Holder for the initial state
        self._initial_states = dict(list(enumerate(data)))
        #: Value of the initial state
        self._current_index = 0
        self.buffers = dict()
        #: Alias for `write_to_file`
        self.write = self.write_to_file
        #: Alias for `out`
        self.bake = self.out
        #: Alias for `web`
        self.cyberchef = self.web
        #: Alias for `load_file`
        self.read_file = self.load_file
        #: Holds all the methods that are called/chained and their args
        self._stack = list()
        #: Holds register values
        self._registers = dict()

        #: Log level
        self.log_level = logging.INFO
        #: Log format message
        self.log_format = "%(levelname)-2s - %(message)s"
        logging.getLogger().setLevel(self.log_level)
        logging.basicConfig(format=self.log_format)
        # logger
        self._log = logging

    @property
    def recipe(self) -> List[Dict[str, Union[str, Dict[str, Any]]]]:
        """Returns the current recipe. This is a list of dictionaries
        that contains the method name and the arguments.

        Returns:
            List[Dict[str, Union[str, Dict[str, Any]]]]: The recipe.
        """
        return self._stack

    @property
    def state(self):
        return self.states[self._current_index]

    @state.setter
    def state(self, val):
        self.states[self._current_index] = val

    def __str__(self):
        try:
            if isinstance(self.state, bytearray):
                return re.sub(rb"[^\x00-\x7f]", b".", self.state).decode()
            else:
                return self._convert_to_str()
        except UnicodeDecodeError:  # pragma: no cover
            return "Could not convert to str, but the data exists in the states. Use o, output or out() to access the values"
        except:  # pragma: no cover
            logging.exception(
                "\n\nCannot print current state. Either chain with "
                "another method, or use one of the output methods "
                "Example: .o, .out, .state or .out\n\n"
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
        return json.loads(jsonpickle.encode(obj, unpicklable=True))

    def _load_as_file(self) -> object:
        """This method is used when a function or a method expects
        a file path to load a file. Instead of passing a file path,
        this method allows passing an io.BytesIO object instead.

        Returns:
            object: io.BytesIO object
        """
        return io.BytesIO(self._convert_to_bytes())

    def _abs_path(self, path: str):
        """Returns the absolute path by expanding home dir

        Args:
            path (str): Path to expand

        Returns:
            object: Path object
        """
        return Path(path).expanduser().absolute()

    def _info_logger(self, data: str) -> None:
        """Just a binding for logger.info

        Args:
            data (str): Message to log

        Returns:
            Chepy: The Chepy object.
        """
        logging.info(blue(data))
        return None

    def _warning_logger(self, data: str) -> None:  # pragma: no cover
        """Just a binding for logger.warning

        Args:
            data (str): Message to log

        Returns:
            Chepy: The Chepy object.
        """
        logging.warning(yellow(data))
        return None

    def _error_logger(self, data: str) -> None:  # pragma: no cover
        """Just a binding for logger.error

        Args:
            data (str): Message to log

        Returns:
            Chepy: The Chepy object.
        """
        logging.error(red(data))
        return None

    def subsection(
        self,
        pattern: Union[str, bytes],
        methods: List[Tuple[Union[str, object], dict]],
        group: int = 0,
    ):
        """Run specified methods over a subsection of the state. This method will always treat the state
        as bytes.

        Args:
            pattern (Union[str, bytes]): Regex pattern to match against.
            methods (List[Tuple[Union[str, object], dict]]): Required. List of tuples. The first value of the
                tuple is the method name, the second value is a dictionary of arguments.
            group (int, optional): Matching group. Defaults to 0.

        Returns:
            _type_: _description_
        """
        if isinstance(pattern, str):
            pattern = pattern.encode()

        old_state = self._convert_to_bytes()
        new_state = b""
        start = 0
        for matched in re.compile(pattern).finditer(old_state):
            end, newstart = matched.span()
            self.state = matched.group(group)
            new_state += old_state[start:end]
            for method in methods:
                if type(method[0]).__name__ == "method":
                    method_name = method[0].__name__  # type: ignore
                elif isinstance(method[0], str):
                    method_name = method[0]
                if len(method) > 1:
                    getattr(self, method_name)(**method[1]).o
                else:
                    getattr(self, method_name)().o
            start = newstart
            new_state += self._convert_to_bytes()

        new_state += old_state[start:]

        self.state = new_state
        return self

    def fork(self, methods: List[Tuple[Union[str, object], dict]]):
        """Run multiple methods on all available states

        Method names in a list of tuples. If using in the cli,
        this should not contain any spaces.

        Args:
            methods (List[Tuple[Union[str, object], dict]]): Required. List of tuples

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
                    method_name = method[0].__name__  # type: ignore
                elif isinstance(method[0], str):
                    method_name = method[0]
                if len(method) > 1:
                    self.states[i] = getattr(self, method_name)(**method[1]).o
                else:
                    self.states[i] = getattr(self, method_name)().o
        return self

    def for_each(
        self,
        methods: List[Tuple[Union[str, object], dict]],
        merge: Union[str, bytes, None] = None,
    ):
        """Run multiple methods on current state if it is a list

        Method names in a list of tuples. If using in the cli,
        this should not contain any spaces.

        Args:
            methods (List[Tuple[Union[str, object], dict]]): Required.
                List of tuples
            merge (Union[str, bytes, None]): Merge data with. Defaults to None

        Returns:
            Chepy: The Chepy object.

        Examples:
            This method takes an array of method names and their args as an list of
            tuples; the first value of the tuple is the method name as either a string,
            or as an object, and the second value is a ditionary of arguments. The keys of
            in the dictionary are method argument names, while the values are argument
            values.

            >>> from chepy import Chepy
            >>> c = Chepy(['41', '42'])
            >>> c.for_each([("from_hex",), ("to_hex",)])
            >>> # this is how to use fork methods with a string
            >>> c.for_each([(c.from_hex,), (c.to_hex,)])
            >>> # This is how to use fork using methods
            >>> print(c)
            ['41', '42']
        """
        assert isinstance(self.state, list), "Current state is not a list"
        hold = self.state
        for i, val in enumerate(hold):
            self.state = val
            for method in methods:
                if type(method[0]).__name__ == "method":
                    method_name = method[0].__name__  # pragma: no cover
                elif isinstance(method[0], str):
                    method_name = method[0]
                if len(method) > 1:
                    hold[i] = getattr(self, method_name)(
                        **method[1]
                    ).o  # pragma: no cover
                else:
                    hold[i] = getattr(self, method_name)().o
        if merge is not None:
            if len(hold) > 0:
                merge = self._to_bytes(merge)
                if isinstance(hold[0], str):  # pragma: no cover
                    self.state = merge.decode().join(hold)
                elif isinstance(hold[0], bytes):
                    self.state = merge.join(hold)
                else:  # pragma: no cover
                    self.state = hold
        else:
            self.state = hold
        return self

    @ChepyDecorators.call_stack
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

    @ChepyDecorators.call_stack
    def create_state(self):
        """Create a new empty state

        Returns:
            Chepy: The Chepy object.
        """
        self.states[len(self.states)] = {}
        return self

    @ChepyDecorators.call_stack
    def copy_state(self, index: int = None):
        """Copy the current state to a new state

        Args:
            index (int): Index of new state. Defaults to next available.

        Returns:
            Chepy: The Chepy object.
        """
        if not index:
            index = len(self.states)
        self.states[index] = self.states.get(self._current_index)
        return self

    @ChepyDecorators.call_stack
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

    @ChepyDecorators.call_stack
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

    @ChepyDecorators.call_stack
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

    @ChepyDecorators.call_stack
    def get_state(self, index: int) -> Any:
        """Returns the value of the specified state.

        This method does not chain with other methods of Chepy

        Args:
            index (int): The index of the state

        Returns:
            Any: Any value that is in the specified state
        """
        return self.states.get(index)

    @ChepyDecorators.call_stack
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

    @ChepyDecorators.call_stack
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

    @ChepyDecorators.call_stack
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

    @ChepyDecorators.call_stack
    def substring(self, pattern: str, group: int = 0):
        """Choose a substring from current state as string

        The preceding methods will only run on the substring and
        not the original state. Group capture is supported.

        Args:
            pattern (str): Pattern to match.
            group (int, optional): Group to match. Defaults to 0.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.search(pattern, self._convert_to_str()).group(group)
        return self

    def _convert_to_bytes(self) -> bytes:
        """This method is used to coerce the current object in
        the state variable into a bytes. The method should be
        called inside any method that operates on a string object
        instead of calling `self.state` directly to avoid errors.

        Raises:
            NotImplementedError: If type coercian isn't available
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
        elif isinstance(self.state, float):
            return bytearray(struct.pack("f", self.state))
        else:  # pragma: no cover
            # todo check more types here
            raise NotImplementedError

    def _to_bytes(self, data: Any) -> bytes:  # pragma: no cover
        """This method is used to coerce data to bytes. The method should be
        called inside any method that operates on a string object
        instead of calling `self.state` directly to avoid errors.

        Raises:
            NotImplementedError: If type coercian isn't available
                for the current state type.
        """
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.encode()
        elif isinstance(data, int):
            return str(data).encode()
        elif isinstance(data, dict):
            return str(data).encode()
        elif isinstance(data, list):
            return str(data).encode()
        elif isinstance(data, bool):
            return str(data).encode()
        elif isinstance(data, bytearray):
            return bytes(data)
        elif isinstance(data, float):
            return bytearray(struct.pack("f", data))
        else:  # pragma: no cover
            # todo check more types here
            raise NotImplementedError

    def _convert_to_bytearray(self) -> bytearray:
        """Attempts to coerce the current state into a
        `bytesarray` object
        """
        return bytearray(self._convert_to_bytes())

    def _convert_to_str(self) -> str:
        """This method is used to coerce the current object in
        the state variable into bytes. The method should be
        called inside any method that operates on a bytes object
        instead of calling `self.state` directly to avoid errors.

        Raises:
            NotImplementedError: If type coercian isn't available
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
        elif isinstance(self.state, float):  # pragma: no cover
            return format(self.state, "f")
        else:  # pragma: no cover
            # todo check more types here
            raise NotImplementedError

    def _str_to_bytes(self, s: str) -> bytes:  # pragma: no cover
        """Converts a str to bytes

        Args:
            s (str): String

        Returns:
            bytes: Bytes
        """
        if s is None:
            return s
        if isinstance(s, bytes):
            return s
        return s.encode()

    def _bytes_to_str(self, s: bytes) -> str:  # pragma: no cover
        """Converts a bytes to str

        Args:
            s (str): String

        Returns:
            str: String
        """
        if s is None:
            return s
        if isinstance(s, bytes):
            return s.decode()
        return s

    def _convert_to_int(self) -> int:
        """This method is used to coerce the current object in
        the state variable into an int. The method should be
        called inside any method that operates on a int types
        instead of calling `self.state` directly to avoid errors.

        Raises:
            NotImplementedError: If type coercian isn't available
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
        if isinstance(self.state, str):
            return self.state.encode()
        return self.state

    @property
    def out(self) -> Any:
        """Get the final output

        Returns:
            Any: Final output
        """
        if isinstance(self.state, str):
            return self.state.encode()
        return self.state

    @ChepyDecorators.call_stack
    def get_by_index(self, *indexes: int):
        """Get an item by specifying an index. If only one index is specified, the obj is return else a new list is returned

        Args:
            *indexes (int): Index numbers to get.

        Returns:
            Chepy: The Chepy object.
        """
        if len(indexes) == 1:
            self.state = self.state[int(indexes[0])]
        else:
            self.state = [self.state[int(index)] for index in indexes]
        return self

    def _get_nested_value(self, data, key, split_by="."):
        """Get a dict value based on a string key with dot notation. Supports array indexing.
        If split_by is None or "", returns only the first key
        Args:
            data (dict): Data
            key (str): Dict key in a dot notation and array
            split_by (str, optional): Chars to split key by. Defaults to ".".
        """
        if not split_by:
            return data[key]
        try:
            keys = key.split(split_by)
            for key in keys:
                if "[" in key:
                    # Extract the key and index
                    key, index_str = key.split("[")
                    index_str = index_str.rstrip("]").strip()
                    if index_str == "*":
                        data = [data[key][i] for i in range(len(data[key]))]
                    else:
                        index = int(index_str)
                        data = data[key][index]
                else:
                    if isinstance(data, list):
                        data = [
                            data[i][key] for i in range(len(data)) if key in data[i]
                        ]
                    else:
                        data = data[key] if key in data else data
            return data
        except Exception as e:  # pragma: no cover
            self._error_logger(e)
            return data

    @ChepyDecorators.call_stack
    def get_by_key(self, *keys: str, py_style: bool = False, split_key: str = "."):
        """This method support json keys support.

        Args:
            keys (Tuple[Union[Hashable, None]]): Keys to extract.
            split_key (str, optional): Split nested keys. Defaults to "."
            nested (bool, optional): If the specified keys are nested. Supports array indexing. Defaults to True

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy({"a":{"b": "c"}}).get_by_key('a.b')
            >>> 'c'
        """
        assert isinstance(
            self.state,
            (
                dict,
                list,
            ),
        ), "State does not contain valid data"

        if py_style:
            if len(keys) == 1:
                self.state = self._get_nested_value(
                    self.state, keys[0], split_by=split_key
                )
            else:
                self.state = [
                    self._get_nested_value(self.state, key, split_by=split_key)
                    for key in keys
                ]
        else:
            o = jmespath.search(keys[0], self.state)
            if o is None:  # pragma: no cover
                raise ValueError("Query did not match any data")
            self.state = o
        return self

    @ChepyDecorators.call_stack
    def copy_to_clipboard(self) -> None:  # pragma: no cover
        """Copy to clipboard

        Copy the final output to the clipboard. If an
        error is raised, refer to the documentation on the error.

        Returns:
            None: Copies final output to the clipboard
        """
        pyperclip.copy(self._convert_to_str())
        return None

    @ChepyDecorators.call_stack
    def copy(self) -> None:  # pragma: no cover
        """Copy to clipboard

        Copy the final output to the clipboard. If an
        error is raised, refer to the documentation on the error.

        Returns:
            None: Copies final output to the clipboard
        """
        self.copy_to_clipboard()
        return None

    @ChepyDecorators.call_stack
    def web(
        self,
        magic: bool = False,
        cyberchef_url: str = "https://gchq.github.io/CyberChef/",
    ) -> None:  # pragma: no cover
        """Opens the current string in CyberChef on the browser as hex

        Args:
            magic (bool, optional): Start with the magic method in CyberChef
            cyberchef_url (string, optional): Base url for Cyberchef

        Returns:
            None: Opens the current data in CyberChef
        """
        data = re.sub(
            b"=+$", "", base64.b64encode(binascii.hexlify(self._convert_to_bytes()))
        )
        if magic:
            url = urljoin(
                cyberchef_url,
                "#recipe=From_Hex('None')Magic(3,false,false,'')&input={}".format(
                    data.decode()
                ),
            )
        else:
            url = urljoin(
                cyberchef_url,
                "#recipe=From_Hex('None')&input={}".format(data.decode()),
            )
        webbrowser.open_new_tab(url)
        return None

    @ChepyDecorators.call_stack
    def http_request(
        self,
        method: str = "GET",
        params: dict = {},
        json: dict = None,
        headers: dict = {},
        cookies: dict = {},
    ):  # pragma: no cover
        """Make a http/s request

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

        try:
            from requests import request
        except ImportError:  # pragma: no cover
            self._error_logger("Could not import requests. pip install requests")
            return self

        params = json2str(params)
        headers = json2str(headers)
        cookies = json2str(cookies)
        res = request(
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
            "headers": dict(res.headers),
        }
        return self

    @ChepyDecorators.call_stack
    def load_from_url(
        self,
        method: str = "GET",
        params: dict = {},
        json: dict = None,
        headers: dict = {},
        cookies: dict = {},
    ):  # pragma: no cover
        """Load binary content from a url

        Most common http methods are supported; but some methods may not provide a response body.

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
            Chepy: A bytearray of the response content. The Chepy object.

        Examples:
            By default, this methed with make a GET request, But supports most
            common methods.

                >>> c = Chepy("http://example.com/file.png").load_from_url()
                >>> b'\\x89PNG...'
        """

        def json2str(obj):  # pragma: no cover
            if isinstance(obj, dict):
                return obj
            elif isinstance(obj, str):
                return json.loads(obj)
            else:
                raise NotImplementedError

        try:
            from requests import request
        except ImportError:  # pragma: no cover
            self._error_logger("Could not import requests. pip install requests")
            return self

        params = json2str(params)
        headers = json2str(headers)
        cookies = json2str(cookies)
        res = request(
            method=method,
            url=self.state,
            params=params,
            json=json,
            headers=headers,
            cookies=cookies,
        )
        self.state = io.BytesIO(res.content).read()
        return self

    @ChepyDecorators.call_stack
    def load_dir(self, pattern: str = "*"):
        """Load all file paths in a directory

        Args:
            pattern (str, optional): File pattern to match. Defaults to "*".

        Returns:
            Chepy: The Chepy object.
        """
        files = [x for x in Path(self.state).glob(pattern) if x.is_file()]
        self.states = {x[0]: str(x[1]) for x in enumerate(files) if x[1].is_file()}
        return self

    @ChepyDecorators.call_stack
    def load_file(self, binary_mode: bool = False, encoding: Union[str, None] = None):
        """If a path is provided, load the file

        Args:
            binary_mode (bool, optional): Force load in binary mode.
            encoding (Union[str, None], optional): Encoding for string.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("/path/to/file")
            >>> # at the moment, the state only contains the string "/path/to/file"
            >>> c.load_file() # this will load the file content into the state
        """
        path = Path(str(self.state)).expanduser().absolute()
        if binary_mode:
            with open(path, "rb") as f:
                self.states[self._current_index] = bytearray(f.read())
        else:
            try:
                with open(path, "r", encoding=encoding) as f:  # type: ignore
                    self.states[self._current_index] = f.read()
            except UnicodeDecodeError:
                with open(path, "rb") as f:
                    self.states[self._current_index] = bytearray(f.read())
        return self

    def write_to_file(self, path: str) -> None:
        """Save the state to disk. Return None.

        Args:
            path (str): The file path to save in.

        Returns:
            None: Returns None

        Examples:
            >>> c = Chepy("some data").write_to_file('/some/path/file', as_binary=True)
        """
        if isinstance(path, bytes):  # pragma: no cover
            path = path.decode()
        with open(str(self._abs_path(path)), "w+") as f:
            f.write(self._convert_to_str())
        self._info_logger("File written to {}".format(self._abs_path(path)))
        return None

    def write_binary(self, path: str) -> None:  # pragma: no cover
        """Save the state to disk. Return None.

        Args:
            path (str): The file path to save in.

        Returns:
            None: Returns None

        Examples:
            >>> c = Chepy("some data").write_binary('/some/path/file')
        """
        if isinstance(path, bytes):  # pragma: no cover
            path = path.decode()
        with open(str(self._abs_path(path)), "wb+") as f:
            f.write(self.state)
        self._info_logger("File written to {}".format(self._abs_path(path)))
        return None

    def run_recipe(self, recipes: List[Mapping[str, Union[str, Mapping[str, Any]]]]):
        """Run a recipe on the state. All arguments including optional needs to
        be specified for a recipe.

        Args:
            recipes (List[Mapping[str, Union[str, Mapping[str, Any]]]]): An array of recipes.
                Recipes are in the format {'function': 'function_name', 'args': {'arg_name': 'arg_val'}}

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy('bG9sCg==').run_recipe([{"function":"base64_decode","args":{"custom":None}}]])
            >>> lol
            In this example, we are calling the base64 decode method on the state.
        """
        for recipe in recipes:
            function = recipe["function"]
            args = recipe["args"]
            if len(args) > 0:
                getattr(self, function)(**args)
            else:
                getattr(self, function)()
        return self

    def save_recipe(self, path: str):
        """Save the current recipe

        A recipe will be all the previous methods called on the
        chepy instance along with their args

        Args:
            path (str): The path to save the recipe

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("some data").to_hex().base64_encode()
            >>> c.save_recipe("/path/to/recipe)
            >>> c.out
            NzM2ZjZkNjUyMDY0NjE3NDYx
        """
        with self._abs_path(path) as f:
            f.write_text(json.dumps(self._stack))
        self._info_logger("Saved recipe to {}".format(str(path)))
        return self

    def load_recipe(self, path: str):
        """Load and run a recipe

        Args:
            path (str): Path to recipe file

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("some data").load_recipe("/path/to/recipe").out
            NzM2ZjZkNjUyMDY0NjE3NDYx
        """
        with self._abs_path(path) as f:
            recipes = json.loads(f.read_text())
            for recipe in recipes:
                function = recipe["function"]
                args = recipe["args"]
                if len(args) > 0:
                    getattr(self, function)(**args)
                else:
                    getattr(self, function)()
        return self

    # @ChepyDecorators.call_stack
    def run_script(self, path: str, save_state: bool = False):
        """Inject and run a custom script on the state.
        The custom script must have a function called **cpy_script** which
        must take one argument. The state is passed as the argument.

        Args:
            path (str): Path to custom script
            save_state (bool, optional): Save script output to the state. Defaults to False.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("A").to_hex().run_script('tests/files/script.py', True)
            b'4141'
        """
        script_path = str(self._abs_path(path))
        loader = SourceFileLoader("cpy_s", script_path)
        handle = loader.load_module("cpy_s")
        if save_state:
            self.state = handle.cpy_script(self.state)
        else:
            print(cyan("Script Output: {}".format(script_path)))
            print(handle.cpy_script(self.state))
        return self

    @ChepyDecorators.call_stack
    def loop(self, iterations: int, callback: str, args: dict = {}):
        """Loop and apply callback n times

        Args:
            iterations (int): Number of iterations to loop
            callback (str): The Chepy method to loop over
            args (dict, optional): Optional arguments for the callback. Defaults to {}.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("VmpGb2QxTXhXWGxTYmxKV1lrZDRWVmx0ZEV0alZsSllaVWRHYWxWVU1Eaz0=")
            >>> c.loop(iterations=6, callback='hmac_hash', args={'key': 'secret'})
            securisec
        """
        if type(callback).__name__ == "method":
            # this allows for both method and string passing
            callback = callback.__name__
        assert isinstance(callback, str), "Callback must be a string"
        assert isinstance(iterations, int), "Iterations must be an integer"
        assert isinstance(args, dict), "Args must be a dick"

        stack_loop_index = next(
            itertools.dropwhile(
                lambda x: self._stack[x]["function"] != "loop",
                reversed(range(len(self._stack))),
            )
        )

        for _ in range(int(iterations)):
            getattr(self, callback)(**args)

        self._stack = self._stack[: stack_loop_index + 1]
        return self

    @ChepyDecorators.call_stack
    def loop_list(self, callback: str, args: dict = {}):
        """Loop over an array and run a Chepy method on it

        Args:
            callback (str): Chepy method as string
            args (dict, optional): Dictionary of args. If in cli, dont use spaces. Defaults to {}.

        Returns:
            Chepy: The Chepy object

        Examples:
            This method is capable of running a callable from either
            a string, or a chepy method.

            >>> c = Chepy(["an", "array"])
            >>> c.loop_list('to_hex').loop_list('hmac_hash', {'key': 'secret'})
            ['5cbe6ca2a66b380aec1449d4ebb0d40ac5e1b92e', '30d75bf34740e8781cd4ec7b122e3efd8448e270']
        """
        if type(callback).__name__ == "method":
            # this allows for both method and string passing
            callback = callback.__name__

        assert isinstance(self.state, list), "State is not a list"
        assert isinstance(callback, str), "Callback must be a string"
        hold = []
        current_state = self.state
        # find the last index that this method was run
        stack_loop_index = next(
            itertools.dropwhile(
                lambda x: self._stack[x]["function"] != "loop_list",
                reversed(range(len(self._stack))),
            )
        )
        if isinstance(args, str):  # pragma: no cover
            args = json.loads(args)
        try:
            for index, data in enumerate(current_state):
                self.state = current_state[index]
                if args:
                    hold.append(getattr(self, callback)(**args).o)
                else:
                    hold.append(getattr(self, callback)().o)
            self._stack = self._stack[: stack_loop_index + 1]
            self.state = hold
            return self
        except:  # pragma: no cover
            self.state = current_state
            raise

    @ChepyDecorators.call_stack
    def loop_dict(self, keys: list, callback: str, args: dict = {}):
        """
        Loop over a dictionary and apply the callback to the value

        Args:
            keys (list): List of keys to match. If in cli, dont use spaces.
            callback (str): Chepy method as string
            args (dict, optional): Dictionary of args. If in cli, dont use spaces. Defaults to {}.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy({'some': 'hahahaha', 'lol': 'aahahah'})
            >>> c.loop_dict(['some'], 'hmac_hash', {'key': 'secret'}).o
            {'some': '99f77ec06a3c69a4a95371a7888245ba57f47f55', 'lol': 'aahahah'}

            We can combine `loop_list` and `loop_dict` to loop over a list of dictionaries.

            >>> data = [{"some": "val"}, {"some": "another"}, {"lol": "lol"}, {"another": "aaaa"}]
            >>> c = Chepy(data)
            >>> c.loop_list("loop_dict", {"keys": ["some", "lol"], "callback": "to_upper_case"})
            [
                {"some": "VAL"},
                {"some": "ANOTHER"},
                {"lol": "LOL"},
                {"another": "aaaa"},
            ]
        """
        if type(callback).__name__ == "method":
            # this allows for both method and string passing
            callback = callback.__name__
        assert isinstance(callback, str), "Callback must be a string"

        hold = {}
        current_state = self.state
        # find the last index that this method was run
        stack_loop_index = next(
            itertools.dropwhile(
                lambda x: self._stack[x]["function"] != "loop_dict",
                reversed(range(len(self._stack))),
            )
        )

        if isinstance(keys, str):  # pragma: no cover
            keys = json.loads(keys)

        if isinstance(args, str):  # pragma: no cover
            args = json.loads(args)
        try:
            dict_keys = current_state.keys()
            for key in keys:
                if current_state.get(key) is not None:
                    self.state = current_state.get(key)
                    if args:
                        hold[key] = getattr(self, callback)(**args).o
                    else:
                        hold[key] = getattr(self, callback)().o
            for unmatched_key in list(set(dict_keys) - set(keys)):
                hold[unmatched_key] = current_state[unmatched_key]
            self._stack = self._stack[: stack_loop_index + 1]
            self.state = hold
            return self
        except:  # pragma: no cover
            self.state = current_state
            raise

    @ChepyDecorators.call_stack
    def debug(self, verbose: bool = False):
        """Debug the current instance of Chepy

        This method does not change the state.

        Args:
            verbose (bool, optional): Show verbose info. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        print(cyan("Current state:"), yellow(str(self._current_index)))
        print(cyan("Current states:"), yellow(str(len(self.states))))
        print(
            cyan("Current state types:"),
            yellow(str({k: type(v).__name__ for k, v in self.states.items()})),
        )
        print(cyan("Current buffers:"), yellow(str(len(self.buffers))))
        print(
            cyan("Current buffer types:"),
            yellow(str({k: type(v).__name__ for k, v in self.buffers.items()})),
        )
        if verbose:
            print(magenta("States:"), self.states)
            print(magenta("Buffers:"), self.buffers)
        return self

    @ChepyDecorators.call_stack
    def print(self, *args):  # pragma: no cover
        """Print the state

        Returns:
            Chepy: The Chepy object.
        """
        print(*args, self.state)
        return self

    @ChepyDecorators.call_stack
    def reset(self):
        """Reset states back to their initial values

        Returns:
            Chepy: The Chepy object.
        """
        self.states = self._initial_states
        return self

    @ChepyDecorators.call_stack
    def load_command(self):  # pragma: no cover
        """Run the command in state and get the output

        Returns:
            Chepy: The Chepy object.

        Examples:
            This method can be used to interface with the shell and Chepy
            directly by ingesting a commands output in Chepy.

            >>> c = Chepy("ls -l").shell_output().o
            test.html
            ...
            test.py
        """
        self.state = subprocess.getoutput(self.state)
        return self

    @ChepyDecorators.call_stack
    def pretty(self, indent: int = 2):  # pragma: no cover
        """Prettify the state.

        Args:
            indent (int, optional): Indent level. Defaults to 2.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = pformat(self.state, indent=int(indent))
        return self

    def plugins(self, enable: str) -> None:  # pragma: no cover
        """Use this method to enable or disable Chepy plugins.

        Valid options are `true` or `false`. Once this method completes,
        it does call sys.exit().

        Args:
            enable (str): Set to `true` or `false`

        Returns:
            None
        """
        assert enable in ["true", "false"], "Valid values are true and false"
        conf_path = Path().home() / ".chepy" / "chepy.conf"
        c = ConfigParser()
        c.read(conf_path)
        c.set("Plugins", "enableplugins", enable)
        with open(conf_path, "w") as f:
            c.write(f)
        if enable:
            self._info_logger(
                green(
                    "Plugins have been enabled. Restart Chepy for effects to take place."
                )
            )
        else:
            self._info_logger(
                green(
                    "Plugins have been disabled. Restart Chepy for effects to take place."
                )
            )
        sys.exit()
        return None

    def set_plugin_path(self, path: str) -> None:  # pragma: no cover
        """Use this method to set the path for Chepy plugins.

        Args:
            path (str): Path to plugins directory

        Returns:
            None
        """
        expand_path = self._abs_path(path)
        if expand_path.exists():
            conf_path = Path().home() / ".chepy" / "chepy.conf"
            c = ConfigParser()
            c.read(conf_path)
            c.set("Plugins", "pluginpath", str(expand_path))
            with open(conf_path, "w") as f:
                c.write(f)
            self._info_logger(green("Plugin path has been set. Restart for changes."))
            sys.exit()
            return None
        else:
            raise AttributeError("The path does not exist")

    def callback(self, callback_function: Callable[[Any], Any]):
        """Run any user defined python function against the state.
        This method is not recorded in the recipes

        Args:
            callback_function (Callable[[Any], Any]): The function to run. The function should take one argument (the state is passed to it). It can return Any

        Examples:
            from chepy import Chepy

            def cb(data):
                return data * 2

            c = Chepy('abc').callback(cb)
            # state is now abcabc

        Returns:
            Chepy: The Chepy object.
        """
        # dont run if from cli
        if sys.stdout.isatty():  # pragma: no cover
            logging.warning("callback cannot be used via the cli")
            return self
        self.state = callback_function(self.state)
        return self

    @ChepyDecorators.call_stack
    def register(
        self,
        pattern: Union[str, bytes],
        ignore_case: bool = False,
        multiline: bool = False,
        dotall: bool = False,
        unicode: bool = False,
        extended: bool = False,
    ):
        """Extract data from the input and store it in registers. Regular expression capture groups are used to select the data to extract.

        Args:
            pattern (Union[str, bytes]): Required. The regex pattern to search by
            ignore_case (bool, optional): Set case insensitive flag. Defaults to False.
            multiline (bool, optional): ^/$ match start/end. Defaults to False.
            dotall (bool, optional): `.` matches newline. Defaults to False.
            unicode (bool, optional): Match unicode characters. Defaults to False.
            extended (bool, optional): Ignore whitespace. Defaults to False.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("hello world")
            >>> c.register("(hello)\\s(world)")
            >>> c._registers
            {'$R0': 'hello', '$R1': 'world'}
        """
        # regex flags
        flags = 0
        if ignore_case:
            flags += re.IGNORECASE
        if multiline:
            flags += re.MULTILINE
        if dotall:
            flags += re.DOTALL
        if unicode:
            flags += re.UNICODE
        if extended:  # pragma: no cover
            flags += re.X

        r = re.compile(pattern, flags=flags)
        old_state = self.state

        if isinstance(pattern, bytes):
            matches = r.findall(self._convert_to_bytes())
        else:
            matches = r.findall(self._convert_to_str())

        # there are matches which is a list of tuples
        if len(matches) > 0:
            # if there is only one match, it will be a list. else, it is a list with a tuple
            if isinstance(matches[0], tuple):  # pragma: no cover
                matches = matches[0]
            for i in range(len(matches)):
                # only add non empty
                if matches[i]:
                    self._registers[f"$R{i}"] = matches[i]

        self.state = old_state
        return self

    @ChepyDecorators.call_stack
    def prefix(self, data: bytes):
        """Add a prefix to the data in state. The state is converted to bytes

        Args:
            data (bytes): Data to add

        Returns:
            Chepy: The Chepy object.
        """
        data = self._str_to_bytes(data)
        self.state = data + self._convert_to_bytes()
        return self

    @ChepyDecorators.call_stack
    def suffix(self, data: bytes):
        """Add a suffix to the data in state. The state is converted to bytes

        Args:
            data (bytes): Data to add

        Returns:
            Chepy: The Chepy object.
        """
        data = self._str_to_bytes(data)
        self.state = self._convert_to_bytes() + data
        return self

    def get_register(self, key: str) -> Union[str, bytes]:
        """Get a value from registers by key

        Args:
            key (str): Key

        Raises:
            ValueError: If key does not exist

        Returns:
            Union[str, bytes]: Value of register
        """
        v = self._registers.get(key)
        if v is None:  # pragma: no cover
            raise ValueError("Key not found in registers")
        return v

    def set_register(self, key: str, val: Union[str, bytes]):
        """Set the value of a register

        Args:
            key (str): Key
            val (Union[str, bytes]): Value

        Returns:
            Chepy: The Chepy object.
        """
        self._registers[key] = val
        return self

    @ChepyDecorators.call_stack
    def dump_json(self):
        """Json serialize the state

        Returns:
            Chepy: The Chepy object.
        """

        # Function to recursively convert bytes to UTF-8 strings or Base64-encoded strings
        def encode_bytes(obj):
            if isinstance(obj, bytes):
                try:
                    # Try to decode as UTF-8
                    return obj.decode("utf-8")
                except UnicodeDecodeError:  # pragma: no cover
                    # If decoding fails, encode as Base64
                    return base64.b64encode(obj).decode("utf-8")
            elif isinstance(obj, dict):
                return {
                    encode_bytes(k) if isinstance(k, bytes) else k: encode_bytes(v)
                    for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [encode_bytes(item) for item in obj]
            else:
                return obj

        self.state = json.dumps(encode_bytes(self.state))
        return self
