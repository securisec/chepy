import regex as re
import pydash

from ..core import Core


class Utils(Core):
    def reverse(self, count: int = 1):
        """Reverses the string.

        Parameters:
            count (int): Reverse by the number of characters indicated in count

        Returns:
            Chepy: The Chepy object. 
        """
        if count == 1:
            self._holder = self._holder[::-1]
            return self
        else:
            self._holder = "".join(
                [
                    self._holder[x : x + count]
                    for x in range(0, len(self._holder), count)
                ][::-1]
            )
            return self

    def count_occurances(self, regex: str, case_sensitive: bool = False):
        """Counts the number of times the provided string occurs.

        Parameters:
            regex (str): Regex string to search for
            case_sensitive (bool, optional): If search should be case insensitive, by default False

        Returns:
            Chepy: The Chepy object. 
        """
        if case_sensitive:
            r = re.compile(regex)
        else:
            r = re.compile(regex, re.IGNORECASE)
        self._holder = len(r.findall(self._convert_to_str()))
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
            self._holder = self._convert_to_str().upper()
        elif by == "word":
            self._holder = self._convert_to_str().title()
        elif by == "sentence":
            self._holder = self._convert_to_str().capitalize()
        return self

    def to_snake_case(self):
        """Convert string to snake case
        
        Returns:
            Chepy: The Chepy object.
        """
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", self._convert_to_str())
        self._holder = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
        return self

    def to_camel_case(self, ignore_space: bool = False):
        """Convert string to camel case
        
        Args:
            ignore_space (bool, optional): Ignore space boundaries. Defaults to False.
        
        Returns:
            Chepy: The Chepy object.
        """
        if ignore_space:
            r = re.compile(r"_.|\-.")
        else:
            r = re.compile(r"_.|\-.|\s.")
        self._holder = r.sub(lambda x: x.group()[1].upper(), self._convert_to_str())
        return self

    def to_kebab_case(self):
        """Convert string to kebab case
        
        Returns:
            Chepy: The Chepy object.
        """
        self._holder = pydash.kebab_case(self._convert_to_str())
        return self
