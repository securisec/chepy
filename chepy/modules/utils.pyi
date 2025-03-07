from ..core import ChepyCore
from typing import Any, Literal, TypeVar, Union

UtilsT = TypeVar('UtilsT', bound='Utils')

class Utils(ChepyCore):
    def __init__(self, *data: Any) -> None: ...
    state: Any = ...
    def reverse(self: UtilsT, count: int=...) -> UtilsT: ...
    def count_occurances(self: UtilsT, regex: str, case_sensitive: bool=...) -> UtilsT: ...
    def remove_whitespace(self: UtilsT, spaces: bool=..., carriage_return: bool=..., line_feeds: bool=..., tabs: bool=..., form_feeds: bool=...) -> UtilsT: ...
    def remove_nullbytes(self: UtilsT) -> UtilsT: ...
    def regex_search(self: UtilsT, pattern: str, is_bytes: bool=False, ignore_case: bool=False, multiline: bool=False, dotall: bool=False, unicode: bool=False, extended: bool=False) -> UtilsT: ...
    def split_by_char(self: UtilsT, delimiter: str=...) -> UtilsT: ...
    def split_by_regex(self: UtilsT, pattern: str=..., trim: Any=...) -> UtilsT: ...
    def split_by_n(self: UtilsT, n: int) -> UtilsT: ...
    def split_lines(self: UtilsT) -> UtilsT: ...
    def split_chunks(self: UtilsT, chunk_size: int) -> UtilsT: ...
    def select_every_n(self: UtilsT, n: int, start: int=...) -> UtilsT: ...
    def unique(self: UtilsT) -> UtilsT: ...
    def sort_list(self: UtilsT, reverse: bool=...) -> UtilsT: ...
    def sort_dict_key(self: UtilsT, reverse: bool=...) -> UtilsT: ...
    def sort_dict_value(self: UtilsT, reverse: Any=...) -> UtilsT: ...
    def filter_list(self: UtilsT, by: Union[str, dict], regex: bool=...) -> UtilsT: ...
    def filter_list_by_length(self: UtilsT, length: int, exact: bool=...) -> UtilsT: ...
    def filter_dict_key(self: UtilsT, by: str) -> UtilsT: ...
    def filter_dict_value(self: UtilsT, by: str) -> UtilsT: ...
    def slice(self: UtilsT, start: int=..., end: int=...) -> UtilsT: ...
    def strip_ansi(self: UtilsT) -> UtilsT: ...
    def strip(self: UtilsT, pattern: str, ignore_case: bool=...) -> UtilsT: ...
    def strip_non_printable(self: UtilsT) -> UtilsT: ...
    def find_replace(self: UtilsT, pattern: Union[bytes, str], repl: Union[bytes, str], ignore_case: bool=...) -> UtilsT: ...
    def escape_string(self: UtilsT) -> UtilsT: ...
    def unescape_string(self: UtilsT) -> UtilsT: ...
    def color_hex_to_rgb(self: UtilsT) -> UtilsT: ...
    def diff(self: UtilsT, state: int=..., buffer: int=..., colors: bool=False, swap: bool=False, only_changes: bool=False) -> UtilsT: ...
    def pad(self: UtilsT, width: int, direction: Literal['left', 'right']=..., char: str=...) -> UtilsT: ...
    def count(self: UtilsT) -> UtilsT: ...
    def set(self: UtilsT) -> UtilsT: ...
    def regex_to_str(self: UtilsT, all_combo: bool=...) -> UtilsT: ...
    def shuffle(self: UtilsT) -> UtilsT: ...
    def drop_bytes(self: UtilsT, start: int, length: int) -> UtilsT: ...
    def without(self: UtilsT, *values: Any) -> UtilsT: ...
    def pick(self: UtilsT, *values: Any) -> UtilsT: ...
    def expand_alpha_range(self: UtilsT, join_by: Union[str, None]=None) -> UtilsT: ...
    def split_and_count(self: UtilsT, pattern: Union[str, bytes], threshold: int=None) -> UtilsT: ...
