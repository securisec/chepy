import emoji
from typing import List
import regex as re

from ..core import Core


class Language(Core):
    def unicode_languages(self, lang: str) -> List[str]:
        """Detect characters from varios Unicode code point ids. Example 
        of languages are Common, Arabic, Armenian, Bengali, Bopomofo, Braille, 
        Buhid, Canadian_Aboriginal, Cherokee, Cyrillic, Devanagari, Ethiopic, 
        Georgian, Greek, Gujarati, Gurmukhi, Han, Hangul, Hanunoo, Hebrew, 
        Hiragana, Inherited, Kannada, Katakana, Khmer, Lao, Latin, Limbu, 
        Malayalam, Mongolian, Myanmar, Ogham, Oriya, Runic, Sinhala, Syriac, 
        Tagalog, Tagbanwa, TaiLe, Tamil, Telugu, Thaana, Thai, Tibetan, Yi, 
        but other code points should work also.
        
        Parameters
        ----------
        lang : str
            A string value identifying the language. 
        
        Returns
        -------
        List[str]
            An array of string matches
        """
        return re.findall(r"\p{" + lang + "}", self._convert_to_str())

    def find_emojis(self) -> List[str]:
        """Find emojis, symbols, pictographs, map symbols and flags
        
        Returns
        -------
        List[str]
            An array of matches
        """
        return emoji.get_emoji_regexp().findall(self._convert_to_str())

    def encode_utf_16_le(self, decode: bool=False) -> "Baked":
        """Encode string as UTF16LE (1200). 
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_str().encode('utf_16_le')
        return self

    def decode_utf_16_le(self, decode: bool=False):
        """Decode string as UTF16LE (1200). 
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_bytes().decode('utf_16_le')
        return self

    def encode_utf_16_be(self, decode: bool=False):
        """Encode string as UTF16BE (1201). 
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_str().encode('utf_16_be')
        return self

    def decode_utf_16_be(self, decode: bool=False):
        """Decode string as UTF16BE (1201). 
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_bytes().decode('utf_16_be')
        return self

    def encode_utf_7(self, decode: bool=False):
        """Encode string as UTF7. 
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_str().encode('utf_7')
        return self

    def decode_utf_7(self, decode: bool=False):
        """Decode string as UTF7. 
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_bytes().decode('utf_7')
        return self

    def encode_cp500(self, decode: bool=False):
        """Encode string as EBCDIC-CP-BE, EBCDIC-CP-CH, IBM500 or CP500. 
        Western European languages. 
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_str().encode('cp500')
        return self

    def decode_cp500(self, decode: bool=False):
        """Decode string as EBCDIC-CP-BE, EBCDIC-CP-CH, IBM500 or CP500. 
        Western European languages.
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_bytes().decode('cp500')
        return self

    def encode_cp037(self, decode: bool=False):
        """Encode IBM037, IBM039. English languages.
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_str().encode('cp037')
        return self

    def decode_cp037(self, decode: bool=False):
        """Decode IBM037, IBM039. English languages
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._convert_to_bytes().decode('cp037')
        return self
