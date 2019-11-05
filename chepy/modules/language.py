import emoji
import unicodedata
from typing import List
import regex as re

from ..core import Core


class Language(Core):
    def unicode_chrs_by_lang(self, lang: str):
        """Detect language specific characters
        
        Detect characters from varios Unicode code point ids. Example 
        of languages are Common, Arabic, Armenian, Bengali, Bopomofo, Braille, 
        Buhid, Canadian_Aboriginal, Cherokee, Cyrillic, Devanagari, Ethiopic, 
        Georgian, Greek, Gujarati, Gurmukhi, Han, Hangul, Hanunoo, Hebrew, 
        Hiragana, Inherited, Kannada, Katakana, Khmer, Lao, Latin, Limbu, 
        Malayalam, Mongolian, Myanmar, Ogham, Oriya, Runic, Sinhala, Syriac, 
        Tagalog, Tagbanwa, TaiLe, Tamil, Telugu, Thaana, Thai, Tibetan, Yi, 
        but other code points should work also.
        
        Args:
            lang (str): A string value identifying the language. 
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"\p{" + lang + "}", self._convert_to_str())
        return self

    def find_emojis(self):
        """Find emojis, symbols, pictographs, map symbols and flags
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state =  emoji.get_emoji_regexp().findall(self._convert_to_str())
        return self

    def encode_utf_16_le(self):
        """Encode string as UTF16LE (1200). 
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "utf_16_le", errors="backslashreplace"
        )
        return self

    def decode_utf_16_le(self):
        """Decode string as UTF16LE (1200). 
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("utf_16_le")
        return self

    def encode_utf_16_be(self):
        """Encode string as UTF16BE (1201). 
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "utf_16_be", errors="backslashreplace"
        )
        return self

    def decode_utf_16_be(self):
        """Decode string as UTF16BE (1201). 
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("utf_16_be")
        return self

    def encode_utf_7(self):
        """Encode string as UTF7. 
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode("utf_7", errors="backslashreplace")
        return self

    def decode_utf_7(self):
        """Decode string as UTF7. 
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("utf_7")
        return self

    def encode_cp500(self):
        """Encode string as EBCDIC-CP-BE, EBCDIC-CP-CH, IBM500 or CP500. 
        Western European languages. 
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode("cp500", errors="backslashreplace")
        return self

    def decode_cp500(self):
        """Decode string as EBCDIC-CP-BE, EBCDIC-CP-CH, IBM500 or CP500. 
        Western European languages.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp500")
        return self

    def encode_cp037(self):
        """Encode IBM037, IBM039. English languages.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode("cp037", errors="backslashreplace")
        return self

    def decode_cp037(self):
        """Decode IBM037, IBM039. English languages
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp037")
        return self

    def encode_cp874(self):
        """Encode Windows-874 Thai (874)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode("cp874", errors="backslashreplace")
        return self

    def decode_cp874(self):
        """Decode Windows-874 Thai (874)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp874")
        return self

    def encode_cp932(self):
        """Encode Japanese Shift-JIS (932), 932, ms932, mskanji, ms-kanji	
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode("cp932", errors="backslashreplace")
        return self

    def decode_cp932(self):
        """Decode Japanese Shift-JIS (932), 932, ms932, mskanji, ms-kanji	
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp932")
        return self

    def encode_gbk(self):
        """Encode Simplified Chinese GBK (936), 936, cp936, ms936
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode("gbk", errors="backslashreplace")
        return self

    def decode_gbk(self):
        """Decode Simplified Chinese GBK (936), 936, cp936, ms936
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("gbk")
        return self

    def encode_gb2312(self):
        """Encode Simplified Chinese GB2312 (20936), chinese, csiso58gb231280, 
        euc-cn, euccn, eucgb2312-cn, gb2312-1980, gb2312-80, iso-ir-58
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "gb2312", errors="backslashreplace"
        )
        return self

    def decode_gb2312(self):
        """Decode Simplified Chinese GB2312 (20936), chinese, csiso58gb231280, 
        euc-cn, euccn, eucgb2312-cn, gb2312-1980, gb2312-80, iso-ir-58
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("gb2312")
        return self

    def encode_cp949(self):
        """Encode Korean (949), 949, ms949, uhc
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode("cp949", errors="backslashreplace")
        return self

    def decode_cp949(self):
        """Decode Korean (949), 949, ms949, uhc
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp949")
        return self

    def encode_cp950(self):
        """Encode Traditional Chinese Big5 (950), 950, ms950
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode("cp950", errors="backslashreplace")
        return self

    def decode_cp950(self):
        """Decode Traditional Chinese Big5 (950), 950, ms950
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp950")
        return self

    def encode_cp1250(self):
        """Encode Windows-1250 Central / Eastern European (1250), windows-1250	
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "cp1250", errors="backslashreplace"
        )
        return self

    def decode_cp1250(self):
        """Decode Windows-1250 Central / Eastern European (1250), windows-1250	
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp1250")
        return self

    def encode_cp1251(self):
        """Encode Windows-1251 Cyrillic (1251), windows-1251
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "cp1251", errors="backslashreplace"
        )
        return self

    def decode_cp1251(self):
        """Decode Windows-1251 Cyrillic (1251), windows-1251
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp1251")
        return self

    def encode_cp1252(self):
        """Encode Windows-1252 Latin (1252)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "cp1252", errors="backslashreplace"
        )
        return self

    def decode_cp1252(self):
        """Decode Windows-1252 Latin (1252)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp1252")
        return self

    def encode_cp1253(self):
        """Encode Windows-1253 Greek (1253)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "cp1253", errors="backslashreplace"
        )
        return self

    def decode_cp1253(self):
        """Decode Windows-1253 Greek (1253)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp1253")
        return self

    def encode_cp1254(self):
        """Encode Windows-1254 Turkish (1254)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "cp1254", errors="backslashreplace"
        )
        return self

    def decode_cp1254(self):
        """Decode Windows-1254 Turkish (1254)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp1254")
        return self

    def encode_cp1255(self):
        """Encode Windows-1255 Hebrew (1255)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "cp1255", errors="backslashreplace"
        )
        return self

    def decode_cp1255(self):
        """Decode Windows-1255 Hebrew (1255)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp1255")
        return self

    def encode_cp1256(self):
        """Encode Windows-1256 Arabic (1256)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "cp1256", errors="backslashreplace"
        )
        return self

    def decode_cp1256(self):
        """Decode Windows-1256 Arabic (1256)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp1256")
        return self

    def encode_cp1257(self):
        """Encode Windows-1257 Baltic (1257)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "cp1257", errors="backslashreplace"
        )
        return self

    def decode_cp1257(self):
        """Decode Windows-1257 Baltic (1257)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp1257")
        return self

    def encode_cp1258(self):
        """Encode Windows-1258 Vietnam (1258)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "cp1258", errors="backslashreplace"
        )
        return self

    def decode_cp1258(self):
        """Decode Windows-1258 Vietnam (1258)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("cp1258")
        return self

    def encode_iso8859_2(self):
        """Encode ISO-8859-2 Latin 2 Central European (28592)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_2", errors="backslashreplace"
        )
        return self

    def decode_iso8859_2(self):
        """Decode ISO-8859-2 Latin 2 Central European (28592)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_2")
        return self

    def encode_iso8859_3(self):
        """Encode ISO-8859-3 Latin 3 South European (28593)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_3", errors="backslashreplace"
        )
        return self

    def decode_iso8859_3(self):
        """Decode ISO-8859-3 Latin 3 South European (28593)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_3")
        return self

    def encode_iso8859_4(self):
        """Encode ISO-8859-4 Latin 4 North European (28594)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_4", errors="backslashreplace"
        )
        return self

    def decode_iso8859_4(self):
        """Decode ISO-8859-4 Latin 4 North European (28594)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_4")
        return self

    def encode_iso8859_5(self):
        """Encode ISO-8859-5 Latin/Cyrillic (28595)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_5", errors="backslashreplace"
        )
        return self

    def decode_iso8859_5(self):
        """Decode ISO-8859-5 Latin/Cyrillic (28595)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_5")
        return self

    def encode_iso8859_6(self):
        """Encode ISO-8859-6 Latin/Arabic (28596)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_6", errors="backslashreplace"
        )
        return self

    def decode_iso8859_6(self):
        """Decode ISO-8859-6 Latin/Arabic (28596)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_6")
        return self

    def encode_iso8859_7(self):
        """Encode ISO-8859-7 Latin/Greek (28597)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_7", errors="backslashreplace"
        )
        return self

    def decode_iso8859_7(self):
        """Decode ISO-8859-7 Latin/Greek (28597)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_7")
        return self

    def encode_iso8859_8(self):
        """Encode ISO-8859-8 Latin/Hebrew (28598)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_8", errors="backslashreplace"
        )
        return self

    def decode_iso8859_8(self):
        """Decode ISO-8859-8 Latin/Hebrew (28598)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_8")
        return self

    def encode_iso8859_9(self):
        """Encode ISO-8859-9 Latin 5 Turkish (28599)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_9", errors="backslashreplace"
        )
        return self

    def decode_iso8859_9(self):
        """Decode ISO-8859-9 Latin 5 Turkish (28599)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_9")
        return self

    def encode_iso8859_10(self):
        """Encode ISO-8859-10 Latin 6 Nordic (28600)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_10", errors="backslashreplace"
        )
        return self

    def decode_iso8859_10(self):
        """Decode ISO-8859-10 Latin 6 Nordic (28600)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_10")
        return self

    def encode_iso8859_11(self):
        """Encode ISO-8859-11 Latin/Thai (28601)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_11", errors="backslashreplace"
        )
        return self

    def decode_iso8859_11(self):
        """Decode ISO-8859-11 Latin/Thai (28601)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_11")
        return self

    def encode_iso8859_13(self):
        """Encode ISO-8859-13 Latin 7 Baltic Rim (28603)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_13", errors="backslashreplace"
        )
        return self

    def decode_iso8859_13(self):
        """Decode ISO-8859-13 Latin 7 Baltic Rim (28603)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_13")
        return self

    def encode_iso8859_14(self):
        """Encode ISO-8859-14 Latin 8 Celtic (28604)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_14", errors="backslashreplace"
        )
        return self

    def decode_iso8859_14(self):
        """Decode ISO-8859-14 Latin 8 Celtic (28604)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_14")
        return self

    def encode_iso8859_15(self):
        """Encode ISO-8859-15 Latin 9 (28605)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_str().encode(
            "iso8859_15", errors="backslashreplace"
        )
        return self

    def decode_iso8859_15(self):
        """Decode ISO-8859-15 Latin 9 (28605)
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = self._convert_to_bytes().decode("iso8859_15")
        return self

    def remove_diacritics(self):
        """Replaces accented characters latin character equivalent.
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = unicodedata.normalize("NFKD", self._convert_to_str()).encode(
            "ascii", errors="ignore"
        )
        return self

    def unicode_to_str(self):
        """Escape any \\u characters to its proper unicode representation
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = self._convert_to_bytes().decode('unicode-escape')
        return self
