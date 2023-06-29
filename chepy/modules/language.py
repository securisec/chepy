import unicodedata
from typing import TypeVar

import emoji
import regex as re

from ..core import ChepyCore, ChepyDecorators

LanguageT = TypeVar("LanguageT", bound="Language")


class Language(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    @ChepyDecorators.call_stack
    def search_perl_unicode_props(self, lang: str) -> LanguageT:
        """Search using perl unicode properties.
        https://perldoc.perl.org/perluniprops#(%5Cd+)-in-the-info-column-gives-the-number-of-Unicode-code-points-matched-by-this-property.

        Args:
            lang (str): Required. A string value identifying the language.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"\p{" + lang + "}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def find_emojis(self) -> LanguageT:
        """Find emojis, symbols, pictographs, map symbols and flags

        Returns:
            Chepy: The Chepy object.
        """
        self.state = [e.get("emoji") for e in emoji.emoji_list(self._convert_to_str())]
        return self

    @ChepyDecorators.call_stack
    def encode(self, encoding: str, errors: str = "backslashreplace") -> LanguageT:
        """Encode the string using the given encoding.

        Args:
            encoding (str): Encoding to use.
            errors (str, optional): How to handle errors when encoding. Defaults to 'backslashreplace'.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_str().encode(encoding, errors=errors)
        return self

    @ChepyDecorators.call_stack
    def encode_us_ascii_7_bit(self) -> LanguageT:
        """Encode state using US ascii 7 bit

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_str()
        self.state = "".join(chr(ord(c) & 127) for c in data)
        return self

    @ChepyDecorators.call_stack
    def decode(self, encoding: str, errors: str = "backslashreplace") -> LanguageT:
        """Decode the string using the given encoding.

        Args:
            encoding (str): Encoding to use.
            errors (str, optional): How to handle errors when decoding. Defaults to 'backslashreplace'.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_bytes().decode(encoding, errors=errors)
        return self

    @ChepyDecorators.call_stack
    def remove_diacritics(self) -> LanguageT:
        """Replaces accented characters latin character equivalent.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = unicodedata.normalize("NFKD", self._convert_to_str()).encode(
            "ascii", errors="ignore"
        )
        return self

    @ChepyDecorators.call_stack
    def unicode_to_str(self) -> LanguageT:
        """Escape any \\u characters to its proper unicode representation

        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_bytes().decode(
            "unicode-escape", errors="backslashreplace"
        )
        return self

    @ChepyDecorators.call_stack
    def str_to_unicode(self) -> LanguageT:
        """Convert unicode to str

        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_str().encode("unicode_escape")
        return self
