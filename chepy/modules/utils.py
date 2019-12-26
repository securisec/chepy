import difflib
import regex as re
from typing import Any
import pydash

from ..core import ChepyCore, ChepyDecorators
from .exceptions import StateNotDict, StateNotList
import chepy.modules.internal.colors as _int_colors


class Utils(ChepyCore):
    @ChepyDecorators.call_stack
    def reverse(self, count: int = 1):
        """Reverses a string
        
        Args:
            count (int, optional): Reverse by the number of characters indicated in count. Defaults to 1.
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("abcdefg").reverse().output
            "gfedcba"
        """
        if count == 1:
            self.state = self.state[::-1]
            return self
        else:
            self.state = "".join(
                [self.state[x : x + count] for x in range(0, len(self.state), count)][
                    ::-1
                ]
            )
            return self

    @ChepyDecorators.call_stack
    def count_occurances(self, regex: str, case_sensitive: bool = False):
        """Counts occurances of the regex.

        Counts the number of times the provided string occurs.

        Args:
            regex (str): Required. Regex string to search for
            case_sensitive (bool, optional): If search should be case insensitive, by default False

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("AABCDADJAKDJHKSDAJSDdaskjdhaskdjhasdkja").count_occurances("ja").output
            2
        """
        if case_sensitive:
            r = re.compile(regex)
        else:
            r = re.compile(regex, re.IGNORECASE)
        self.state = len(r.findall(self._convert_to_str()))
        return self

    @ChepyDecorators.call_stack
    def remove_whitespace(
        self,
        spaces: bool = True,
        carriage_return: bool = True,
        line_feeds: bool = True,
        tabs: bool = True,
        form_feeds: bool = True,
    ):
        """Remove whitespace from a string
        
        Args:
            spaces (bool, optional): Remove spaces. Defaults to True.
            carriage_return (bool, optional): Remove carriage return \\r. Defaults to True.
            line_feeds (bool, optional): Remove line feeds \\n. Defaults to True.
            tabs (bool, optional): Temove tabs \\t. Defaults to True.
            form_feeds (bool, optional): Remove form feeds \\f. Defaults to True.
        
        Returns:
            Chepy: The Chepy object.
        """
        remove = []
        if spaces:
            remove.append(" ")
        if carriage_return:
            remove.append("\r")
        if line_feeds:
            remove.append("\n")
        if tabs:
            remove.append("\t")
        if form_feeds:
            remove.append("\f")
        print(remove)
        self.state = re.sub("|".join(remove), "", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def remove_nullbytes(self):
        """Remove null \\x00 byes from binary data
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_bytes().replace(b"\x00", b"")
        return self

    @ChepyDecorators.call_stack
    def regex_search(
        self,
        pattern: str,
        ignore_case: bool = False,
        multiline: bool = False,
        dotall: bool = False,
        unicode: bool = False,
        extended: bool = False,
    ):
        """Regex search on current data
        
        Args:
            pattern (str): Required. The regex pattern to search by
            ignore_case (bool, optional): Set case insentive flag. Defaults to False.
            multiline (bool, optional): ^/$ match start/end. Defaults to False.
            dotall (bool, optional): `.` matches newline. Defaults to False.
            unicode (bool, optional): Match unicode characters. Defaults to False.
            extended (bool, optional): Ignore whitespace. Defaults to False.
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("loLolololoL")
            >>> c.regex_search("ol", ignore_case=True)
        """
        flags = 0
        if ignore_case:
            flags += re.IGNORECASE
        if multiline:
            flags += re.MULTILINE
        if dotall:
            flags += re.DOTALL
        if unicode:
            flags += re.UNICODE
        if extended:
            flags += re.X
        self.state = re.findall(pattern, self._convert_to_str(), flags=flags)
        return self

    @ChepyDecorators.call_stack
    def split_by(self, pattern: str = "\n", trim=True):
        """Split a string by the given pattern
        
        Args:
            pattern (str, optional): Pattern to split by. Defaults to '\\n'.
            time (bool, optional): Trim whitespace after split. Defaults to True
        
        Returns:
            Chepy: The Chepy object.
        """
        if trim:
            self.state = list(
                map(pydash.trim, re.split(pattern, self._convert_to_str()))
            )
        else:
            self.state = re.split(pattern, self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def split_by_n(self, n: int):
        """Split a string by n characters.
        
        Args:
            n (int): n from 0
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some string").split_by_n(2).o[2]
            " s"
        """
        self.state = re.findall(".{1," + str(n) + "}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def get_every_n(self, n: int):
        """Get every nth item from a list or string. 

        Index starts at 0
        
        Args:
            n (int): n from 0
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy(["a", 1, "lol", "b", True]).get_every_n(3)
            ["a", "b"]
        """
        self.state = self.state[0::n]
        return self

    @ChepyDecorators.call_stack
    def unique(self):
        """Get an array of unique list items
        
        Raises:
            TypeError: If state is not a list
        
        Returns:
            Chepy: The Chepy object.
        """
        if isinstance(self.state, list):
            self.state = pydash.uniq(self.state)
            return self
        else:  # pragma: no cover
            raise TypeError("State is not a list")

    @ChepyDecorators.call_stack
    def sorted(self, reverse: bool = False):
        """Sort a list
        
        Args:
            reverse (bool, optional): In reverse order. Defaults to False.
        
        Raises:
            TypeError: If state is not list
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy(["a", "b", "1", "2"]).sorted().o
            ["1", "2", "a", "b"]
        """
        if isinstance(self.state, (list)):
            self.state = sorted(self.state)
            return self
        else:  # pragma: no cover
            raise TypeError("State is not a list")

    @ChepyDecorators.call_stack
    def filter_list(self, by: str):
        """Filter a dict or list
        
        Args:
            by (str): Required. What to filter by. Defaults to None.
        
        Raises:
            TypeError: If state is not a list
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy('[{"a": 1}, {"b": 2}, {"a": 1, "b": 3}]').str_list_to_list().filter_list("b").o
            [{"b": 2}, {"a": 1, "b": 3}]
        """
        assert isinstance(self.state, list), StateNotList()
        self.state = pydash.filter_(self.state, by)
        return self

    @ChepyDecorators.call_stack
    def filter_dict_key(self, by: str):
        """Filter dictionary by key
        
        Args:
            by (str): Required. Key to filter by. 
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy({'some': 'dict', 'another': 'val'}).filter_dict_key('ano')
            {'another': 'val'}
        """
        assert isinstance(self.state, dict), StateNotDict()
        self.state = {
            key: val for (key, val) in self.state.items() if re.search(by, str(key))
        }
        return self

    @ChepyDecorators.call_stack
    def filter_dict_value(self, by: str):
        """Filter dictionary by value. 

        This method does descend into nested dictionary values. 
        
        Args:
            by (str): Required. Value to filter by. 
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy({'some': 'dict', 'another': 'val'}).filter_dict_value('val')
            {'another': 'val'}
        """
        assert isinstance(self.state, dict), StateNotDict()
        self.state = {
            key: val for (key, val) in self.state.items() if re.search(by, str(val))
        }
        return self

    @ChepyDecorators.call_stack
    def slice(self, start: int = 0, end: int = None):
        """Returns the specified slice
        
        Args:
            start (int, optional): Start position. Defaults to 0.
            end (int, optional): End position. Defaults to None.
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").slice(3, 6).o
            "e d"
        """
        self.state = self.state[start:end]
        return self

    @ChepyDecorators.call_stack
    def find_replace(self, pattern: str, repl: str, ignore_case=True):
        """Replace matched pattern with repln
        
        Args:
            pattern (str): Required. Pattern to search
            repl (str): Required. Pattern to match
            ignore_case (bool, optional): Case insensitive. Defaults to True.
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some some data").find_replace(r"some\s", "data").o
            "datadatadata"
        """
        flags = 0
        if ignore_case:
            flags = re.IGNORECASE
        self.state = re.sub(pattern, repl, self._convert_to_str(), flags=flags)
        return self

    @ChepyDecorators.call_stack
    def escape_string(self):
        """Escape all special characters in a string
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("\\$ome' d@ta").unescape_string().o
            "$ome' d@ta"
        """
        self.state = re.escape(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def unescape_string(self):
        """Unescape \\ from a string
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.sub(r"\\", "", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def color_hex_to_rgb(self):
        """Convert hex color to rgb
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = tuple(
            int(self._convert_to_str().strip("#")[i : i + 2], 16) for i in (0, 2, 4)
        )
        return self

    @ChepyDecorators.call_stack
    def diff(
        self,
        state: int = None,
        buffer: int = None,
        colors: bool = False,
        swap: bool = False,
    ):
        """Diff state with another state or buffer
        
        Args:
            state (int, optional): Index of state to compare against. Defaults to None.
            buffer (int, optional): Index of buffer to compare against. Defaults to None.
            colors (int, optional): Show colored diff. Defaults to False.
            swap (int, optional): Swap the diff order. Defaults to False.
        
        Raises:
            TypeError: If both state and buffer is set to True.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("first string", "First $trin")
            >>> # there are two states
            >>> c.diff(state=1) # this will diff state 0 with state 1
            {F->f}irst {-$}strin{+g}
            >>> # optionally set colors=True in the diff method to see colored output
        """
        if state is not None and buffer is None:
            data = self.states.get(state)
            if isinstance(data, bytes):  # pragma: no cover
                data = data.decode()
        elif state is None and buffer is not None:
            data = self.buffers.get(buffer)
            if isinstance(data, bytes):  # pragma: no cover
                data = data.decode()
        else:  # pragma: no cover
            raise TypeError("Only select a state or a buffer to diff against")

        if swap:  # pragma: no cover
            matcher = difflib.SequenceMatcher(None, self._convert_to_str(), data)
        else:
            matcher = difflib.SequenceMatcher(None, data, self._convert_to_str())

        def process_tag(tag, i1, i2, j1, j2):  # pragma: no cover
            if tag == "replace":
                if colors:
                    return _int_colors.blue(matcher.b[j1:j2])
                else:
                    return "{" + matcher.a[i1:i2] + "->" + matcher.b[j1:j2] + "}"
            if tag == "delete":
                if colors:
                    return _int_colors.red(matcher.a[i1:i2])
                else:
                    return "{-" + matcher.a[i1:i2] + "}"
            if tag == "equal":
                return matcher.a[i1:i2]
            if tag == "insert":
                if colors:
                    return _int_colors.green(matcher.b[j1:j2])
                else:
                    return "{+" + matcher.b[j1:j2] + "}"
            assert False, "Unknown tag %r" % tag

        self.state = "".join(process_tag(*t) for t in matcher.get_opcodes())
        return self

    @ChepyDecorators.call_stack
    def pad(self, width: int, direction: str = "left", char: str = " "):
        """Pad string with a character
        
        Args:
            width (int): Required. Total length of string. The padding is calculated from 
                the length of state minus width.
            direction (str, optional): Padding direction. left or right. Defaults to 'left'.
            char (str, optional): Char to fill with. Defaults to ' '.
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("lol").pad(5, char="a")
            lol # this is because "lol" is len 3, and padding is 5 - 2, which is 2, so no 
            padding is added
            >>> c = Chepy("lol").pad(8, char="a")
            lolaa # 8 - 3 so the output is padded for 5 chars
            >>> c = Chepy("lol").pad(8, direction="right", char="a")
            aalol
        """
        assert direction in [
            "left",
            "right",
        ], "Direction has to be either left or right"
        if direction == "left":
            self.state = self._convert_to_str().ljust(
                width - len(self._convert_to_str()), char
            )
        elif direction == "right":
            self.state = self._convert_to_str().rjust(
                width - len(self._convert_to_str()), char
            )
        return self

    @ChepyDecorators.call_stack
    def count(self):
        """Count anything
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = pydash.count_by(self.state)
        return self

    @ChepyDecorators.call_stack
    def set(self):
        """Get an array of unique values
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = list(set(self.state))
        return self

    def get_length(self):  # pragma: no cover
        """Get the length of the current state.

        This method does not change the state
        
        Returns:
            Chepy: The Chepy object. 
        """
        self._info_logger(len(self.state))
        return self

    def get_keys(self):  # pragma: no cover
        """Get the dict keys of the current state.

        This method does not change the state
        
        Returns:
            Chepy: The Chepy object. 
        """
        assert isinstance(self.state, dict), StateNotDict()
        self._info_logger(self.state.keys())
        return self

