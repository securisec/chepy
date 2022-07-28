from ..core import ChepyCore
from typing import Any, Literal, TypeVar

LanguageT = TypeVar("LanguageT", bound="Language")

ENCODINGS = Literal[
    "utf_16_le",
    "utf_16_be",
    "utf_7",
    "utf_8",
    "cp500",
    "cp037",
    "cp874",
    "cp932",
    "gbk",
    "gb2312",
    "cp949",
    "cp950",
    "cp1250",
    "cp1251",
    "cp1252",
    "cp1253",
    "cp1254",
    "cp1255",
    "cp1256",
    "cp1257",
    "cp1258",
    "iso8859_2",
    "iso8859_3",
    "iso8859_4",
    "iso8859_5",
    "iso8859_6",
    "iso8859_7",
    "iso8859_8",
    "iso8859_9",
    "iso8859_10",
    "iso8859_11",
    "iso8859_13",
    "iso8859_14",
    "iso8859_15",
    "ascii",
    "unicode-escape",
]

class Language(ChepyCore):
    def __init__(self, *data: Any) -> None: ...
    state: Any = ...
    def search_perl_unicode_props(self: LanguageT, lang: str) -> LanguageT: ...
    def find_emojis(self: LanguageT) -> LanguageT: ...
    def encode(self: LanguageT, encoding: ENCODINGS, errors: Literal['ignore', 'replace', 'backslashreplace']=...) -> LanguageT: ...
    def decode(self: LanguageT, encoding: ENCODINGS, errors: Literal['ignore', 'replace', 'backslashreplace']=...) -> LanguageT: ...
    def remove_diacritics(self: LanguageT) -> LanguageT: ...
    def unicode_to_str(self: LanguageT) -> LanguageT: ...
