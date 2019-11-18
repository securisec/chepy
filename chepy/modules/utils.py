import difflib
import regex as re
from typing import Any
import pydash

from ..core import Core
import chepy.modules.internal.colors as _int_colors


class Utils(Core):
    def reverse(self, count: int = 1):
        """Reverses a string
        
        Args:
            count (int, optional): Reverse by the number of characters indicated in count. Defaults to 1.
        
        Returns:
            Chepy: The Chepy object.
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

    def count_occurances(self, regex: str, case_sensitive: bool = False):
        """Counts occurances of the regex.

        Counts the number of times the provided string occurs.

        Args:
            regex (str): Regex string to search for
            case_sensitive (bool, optional): If search should be case insensitive, by default False

        Returns:
            Chepy: The Chepy object. 
        """
        if case_sensitive:
            r = re.compile(regex)
        else:
            r = re.compile(regex, re.IGNORECASE)
        self.state = len(r.findall(self._convert_to_str()))
        return self

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

    def remove_nullbytes(self):
        """Remove null \\x00 byes from binary data
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_bytes().replace(b"\x00", b"")
        return self

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
            pattern (str): The regex pattern to search by
            ignore_case (bool, optional): Set case insentive flag. Defaults to False.
            multiline (bool, optional): ^/$ match start/end. Defaults to False.
            dotall (bool, optional): `.` matches newline. Defaults to False.
            unicode (bool, optional): Match unicode characters. Defaults to False.
            extended (bool, optional): Ignore whitespace. Defaults to False.
        
        Returns:
            Chepy: The Chepy object.
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

    def split_by(self, pattern: str = "\n"):
        """Split a string by the given pattern
        
        Args:
            pattern (str, optional): Pattern to split by. Defaults to '\\n'.
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.split(pattern, self._convert_to_str())
        return self

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

    def sorted(self, reverse: bool = False):
        """Sort a list
        
        Args:
            reverse (bool, optional): In reverse order. Defaults to False.
        
        Raises:
            TypeError: If state is not list
        
        Returns:
            Chepy: The Chepy object.
        """
        if isinstance(self.state, (list)):
            self.state = sorted(self.state)
            return self
        else:  # pragma: no cover
            raise TypeError("State is not a list")

    def filter_by(self, predicate: Any = None):
        """Filter a dict or list
        
        Args:
            predicate (Any, optional): What to filter by. Defaults to None.
        
        Raises:
            TypeError: If state is not a list or dict
        
        Returns:
            Chepy: The Chepy object.
        """
        if isinstance(self.state, (list, dict)):
            self.state = pydash.filter_(self.state, predicate)
            return self
        else:  # pragma: no cover
            raise TypeError("State is not a list")

    def slice(self, start: int = 0, end: int = None):
        """Returns the specified slice
        
        Args:
            start (int, optional): Start position. Defaults to 0.
            end (int, optional): End position. Defaults to None.
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = self.state[start:end]
        return self

    def find_replace(self, pattern: str, repl: str, ignore_case=True):
        """Replace matched pattern with repln
        
        Args:
            pattern (str): Pattern to search
            repl (str): Pattern to match
            ignore_case (bool, optional): Case insensitive. Defaults to True.
        
        Returns:
            Chepy: The Chepy object.
        """
        flags = 0
        if ignore_case:
            flags = re.IGNORECASE
        self.state = re.sub(pattern, repl, self._convert_to_str(), flags=flags)
        return self

    def escape_string(self):
        """Escape all special characters in a string
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = re.escape(self._convert_to_str())
        return self

    def unescape_string(self):
        """Unescape \\ from a string
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = re.sub(r"\\", "", self._convert_to_str())
        return self

    def color_hex_to_rgb(self):
        """Convert hex color to rgb
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = tuple(
            int(self._convert_to_str().strip("#")[i : i + 2], 16) for i in (0, 2, 4)
        )
        return self

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
                    return _int_colors.BLUE(matcher.b[j1:j2])
                else:
                    return "{" + matcher.a[i1:i2] + "->" + matcher.b[j1:j2] + "}"
            if tag == "delete":
                if colors:
                    return _int_colors.RED(matcher.a[i1:i2])
                else:
                    return "{-" + matcher.a[i1:i2] + "}"
            if tag == "equal":
                return matcher.a[i1:i2]
            if tag == "insert":
                if colors:
                    return _int_colors.GREEN(matcher.b[j1:j2])
                else:
                    return "{+" + matcher.b[j1:j2] + "}"
                return "{+" + matcher.b[j1:j2] + "}"
            assert False, "Unknown tag %r" % tag

        self.state = "".join(process_tag(*t) for t in matcher.get_opcodes())
        return self
