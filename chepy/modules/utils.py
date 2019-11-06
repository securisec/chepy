import regex as re
import pydash

from ..core import Core


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

    def to_upper_case(self, by: str = "all"):
        """Convert string to uppercase
        
        Args:
            by (str, optional): Convert all, by word or by sentence. Defaults to 'all'.
        
        Returns:
            Chepy: The Chepy object.
        """
        assert by in ["all", "word", "sentence"]
        if by == "all":
            self.state = self._convert_to_str().upper()
        elif by == "word":
            self.state = self._convert_to_str().title()
        elif by == "sentence":
            self.state = self._convert_to_str().capitalize()
        return self

    def to_lower_case(self):
        """Convert string to lowercase

        Converts every character in the input to lower case.
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_str().lower()
        return self

    def to_snake_case(self):
        """Convert string to snake case

        Converts the input string to snake case. Snake case is all lower case 
        with underscores as word boundaries. e.g. this_is_snake_case.

        Returns:
            Chepy: The Chepy object.
        """
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", self._convert_to_str())
        self.state = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
        return self

    def to_camel_case(self, ignore_space: bool = False):
        """Convert string to camel case
        
        Converts the input string to camel case. Camel case is all lower case 
        except letters after word boundaries which are uppercase. e.g. thisIsCamelCase 

        Args:
            ignore_space (bool, optional): Ignore space boundaries. Defaults to False.
        
        Returns:
            Chepy: The Chepy object.
        """
        if ignore_space:
            r = re.compile(r"_.|\-.")
        else:
            r = re.compile(r"_.|\-.|\s.")
        self.state = r.sub(lambda x: x.group()[1].upper(), self._convert_to_str())
        return self

    def to_kebab_case(self):
        """Convert string to kebab case

        Converts the input string to kebab case. Kebab case is all lower case 
        with dashes as word boundaries. e.g. this-is-kebab-case.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = pydash.kebab_case(self._convert_to_str())
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

    def swap_case(self):
        """Swap case in a string
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = pydash.swap_case(self._convert_to_str())
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
