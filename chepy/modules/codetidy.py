from typing import TypeVar

import json
import random

import pydash
import regex as re
from ..core import ChepyCore, ChepyDecorators

CodeTidyT = TypeVar("CodeTidyT", bound="CodeTidy")


class CodeTidy(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    @ChepyDecorators.call_stack
    def minify_json(self) -> CodeTidyT:
        """Minify JSON string

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("/path/to/file.json").load_file()
            >>> print(c.minify_json())
        """
        self.state = json.dumps(
            json.loads(self._convert_to_str()), separators=(",", ":")
        )
        return self

    @ChepyDecorators.call_stack
    def beautify_json(self, indent: int = 2) -> CodeTidyT:
        """Beautify minified JSON

        Args:
            indent (int, optional): Indent level. Defaults to 2.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("/path/to/file.json").load_file()
            >>> print(c.beautify_json(indent=4))
        """
        self.state = json.dumps(json.loads(self._convert_to_str()), indent=indent)
        return self

    @ChepyDecorators.call_stack
    def to_upper_case(self, by: str = "all") -> CodeTidyT:
        """Convert string to uppercase

        Args:
            by (str, optional): Convert all, by word or by sentence. Defaults to 'all'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            Uppercase by word

            >>> Chepy("some String").to_upper_case(by="word").o
            "Some String"

            Uppercase by sentence

            >>> Chepy("some String").to_upper_case(by="sentence").o
            "Some string"

            Uppercase all

            >>> Chepy("some String").to_upper_case(by="all").o
            "SOME STRING"
        """
        assert by in [
            "all",
            "word",
            "sentence",
        ], "Valid options are all, word and sentence"
        if by == "all":
            self.state = self._convert_to_str().upper()
        elif by == "word":
            self.state = self._convert_to_str().title()
        elif by == "sentence":
            self.state = self._convert_to_str().capitalize()
        return self

    @ChepyDecorators.call_stack
    def to_lower_case(self) -> CodeTidyT:
        """Convert string to lowercase

        Converts every character in the input to lower case.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("HelLo WorLd").to_lower_case().o
            "hello world"
        """
        self.state = self._convert_to_str().lower()
        return self

    @ChepyDecorators.call_stack
    def to_snake_case(self) -> CodeTidyT:
        """Convert string to snake case

        Converts the input string to snake case. Snake case is all lower case
        with underscores as word boundaries. e.g. this_is_snake_case.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("helloWorld").to_snake_case().o
            "hello_world"
        """
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", self._convert_to_str())
        self.state = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
        return self

    @ChepyDecorators.call_stack
    def to_camel_case(self, ignore_space: bool = False) -> CodeTidyT:
        """Convert string to camel case

        Converts the input string to camel case. Camel case is all lower case
        except letters after word boundaries which are uppercase. e.g. thisIsCamelCase

        Args:
            ignore_space (bool, optional): Ignore space boundaries. Defaults to False.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some Data_test").to_camel_case().o
            "someDataTest"

            To ignore space, we can set the `ignore_space` to True
            >>> Chepy("some Data_test").to_camel_case(ignore_space=True).o
            "some DataTest"
        """
        if ignore_space:
            r = re.compile(r"_.|\-.")
        else:
            r = re.compile(r"_.|\-.|\s.")
        self.state = r.sub(lambda x: x.group()[1].upper(), self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def to_kebab_case(self) -> CodeTidyT:
        """Convert string to kebab case

        Converts the input string to kebab case. Kebab case is all lower case
        with dashes as word boundaries. e.g. this-is-kebab-case.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("Some data_test").to_kebab_case().o
            "some-data-test"
        """
        self.state = pydash.kebab_case(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def swap_case(self) -> CodeTidyT:
        """Swap case in a string

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("SoMe TeXt").swap_case().o
            "sOmE tExT"
        """
        self.state = pydash.swap_case(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def to_leetspeak(self, special_chars: bool = True) -> CodeTidyT:
        """Convert string to l33t speak

        Args:
            special_chars (bool, optional): Use special chars in conversion. Defaults to True.

        Returns:
            Chepy: The Chepy object

        Examples:
            >>> Chepy("somexValue").to_leetspeak().o
            "50m3%V@1u3"
        """
        chars = {"B": "8", "E": "3", "L": "1", "O": "0", "S": "5", "T": "7", "Z": "2"}
        special = {"A": "@", "C": "(", "I": "!", "X": "%"}
        if special_chars:
            chars = {**chars, **special}
        hold = ""
        for char in list(self._convert_to_str()):
            upper = char.upper()
            if chars.get(upper):
                hold += chars.get(upper)
            else:
                hold += char
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def random_case(self) -> CodeTidyT:
        """Randomly change the case

        Returns:
            Chepy: The Chepy object.
        """
        string = self._convert_to_str()
        string_length = len(string)

        random_indices = random.sample(range(string_length), string_length)
        random_chars = []
        for i in random_indices:
            if random.choice([True, False]):
                random_chars.append(string[i].upper())
            else:
                random_chars.append(string[i].lower())

        string_list = list(string)
        for index, char in zip(random_indices, random_chars):
            if 0 <= index < len(string_list):
                string_list[index] = char
        self.state = "".join(string_list)
        return self
