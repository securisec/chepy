from ..core import ChepyCore
from typing import Any, Literal, TypeVar, Union, List

yaml: Any
DataFormatT = TypeVar('DataFormatT', bound='DataFormat')

class DataFormat(ChepyCore):
    def __init__(self, *data: Any) -> None: ...
    state: Any = ...
    def eval_state(self: DataFormatT) -> DataFormatT: ...
    def list_to_bytes(self: DataFormatT, ascii: bool=False) -> DataFormatT: ...
    def list_to_str(self: DataFormatT, join_by: Union[str, bytes]=...) -> DataFormatT: ...
    def str_list_to_list(self: DataFormatT) -> DataFormatT: ...
    def join(self: DataFormatT, join_by: Union[str, bytes]=...) -> DataFormatT: ...
    def json_to_dict(self: DataFormatT) -> DataFormatT: ...
    def dict_to_json(self: DataFormatT) -> DataFormatT: ...
    def dict_get_items(self: DataFormatT, *keys: str) -> DataFormatT: ...
    def yaml_to_json(self: DataFormatT) -> DataFormatT: ...
    def json_to_yaml(self: DataFormatT) -> DataFormatT: ...
    def to_base58(self: DataFormatT) -> DataFormatT: ...
    def from_base58(self: DataFormatT) -> DataFormatT: ...
    def to_base85(self: DataFormatT) -> DataFormatT: ...
    def from_base85(self: DataFormatT) -> DataFormatT: ...
    def to_base16(self: DataFormatT) -> DataFormatT: ...
    def from_base16(self: DataFormatT) -> DataFormatT: ...
    def to_base32(self: DataFormatT) -> DataFormatT: ...
    def from_base32(self: DataFormatT, remove_whitespace: bool=True) -> DataFormatT: ...
    def to_int(self: DataFormatT, byteorder: Literal['big', 'little']='big', base: int=10) -> DataFormatT: ...
    def to_bytes(self: DataFormatT) -> DataFormatT: ...
    def from_bytes(self: DataFormatT) -> DataFormatT: ...
    def to_base64(self: DataFormatT, alphabet: Literal[str, 'standard', 'url_safe', 'filename_safe', 'itoa64', 'xml', 'z64', 'radix_64', 'xxencoding', 'rot13', 'unix_crypt']='standard') -> DataFormatT: ...
    def from_base64(self: DataFormatT, alphabet: Literal[str, 'standard', 'url_safe', 'filename_safe', 'itoa64', 'xml', 'z64', 'radix_64', 'xxencoding', 'rot13', 'unix_crypt']='standard', remove_non_alpha: bool=True) -> DataFormatT: ...
    def decode_bytes(self: DataFormatT, errors: Literal['ignore', 'backslashreplace', 'replace']=...) -> DataFormatT: ...
    def to_hex(self: DataFormatT, delimiter: str=..., join_by: str=...) -> DataFormatT: ...
    def from_hex(self: DataFormatT, delimiter: Union[str, None]=None, join_by: str='', replace: Union[bytes, None]=b'%|0x') -> DataFormatT: ...
    def hex_to_int(self: DataFormatT) -> DataFormatT: ...
    def hex_to_bytes(self: DataFormatT) -> DataFormatT: ...
    def hex_to_str(self: DataFormatT, ignore: bool=...) -> DataFormatT: ...
    def str_to_hex(self: DataFormatT, delimiter: Union[str, bytes]=b'') -> DataFormatT: ...
    def int_to_hex(self: DataFormatT, unsigned_int: bool=True, bit_size: int=64) -> DataFormatT: ...
    def int_to_str(self: DataFormatT) -> DataFormatT: ...
    def binary_to_hex(self: DataFormatT) -> DataFormatT: ...
    def normalize_hex(self: DataFormatT, is_bytearray: Any=...) -> DataFormatT: ...
    def str_from_hexdump(self: DataFormatT) -> DataFormatT: ...
    def to_hexdump(self: DataFormatT) -> DataFormatT: ...
    def from_hexdump(self: DataFormatT) -> DataFormatT: ...
    def from_url_encoding(self: DataFormatT) -> DataFormatT: ...
    def to_url_encoding(self: DataFormatT, safe: str=..., all_chars: bool=...) -> DataFormatT: ...
    def bytearray_to_str(self: DataFormatT, encoding: str=..., errors: str=...) -> DataFormatT: ...
    def to_list(self: DataFormatT) -> DataFormatT: ...
    def str_to_dict(self: DataFormatT) -> DataFormatT: ...
    def to_charcode(self: DataFormatT, join_by: str=..., base: int=...) -> DataFormatT: ...
    def from_charcode(self: DataFormatT, delimiter: Union[str, None]=None, join_by: str=' ', base: int=10) -> DataFormatT: ...
    def to_decimal(self: DataFormatT) -> DataFormatT: ...
    def from_decimal(self: DataFormatT, delimiter: Union[str, None]=None, join_by: str=...) -> DataFormatT: ...
    def to_binary(self: DataFormatT, join_by: Union[bytes, str]=..., byte_length: int=...) -> DataFormatT: ...
    def from_binary(self: DataFormatT, delimiter: Union[str, None]=None, byte_length: int=...) -> DataFormatT: ...
    def to_octal(self: DataFormatT, join_by: str=...) -> DataFormatT: ...
    def from_octal(self: DataFormatT, delimiter: str=..., join_by: str=...) -> DataFormatT: ...
    def to_html_entity(self: DataFormatT, format:Literal['named', 'numeric', 'hex']='named', all_chars:bool=False) -> DataFormatT: ...
    def from_html_entity(self: DataFormatT) -> DataFormatT: ...
    def to_punycode(self: DataFormatT) -> DataFormatT: ...
    def from_punycode(self: DataFormatT) -> DataFormatT: ...
    def encode_bruteforce(self: DataFormatT) -> DataFormatT: ...
    def decode_bruteforce(self: DataFormatT) -> DataFormatT: ...
    def to_braille(self: DataFormatT) -> DataFormatT: ...
    def from_braille(self: DataFormatT) -> DataFormatT: ...
    def trim(self: DataFormatT) -> DataFormatT: ...
    def to_nato(self: DataFormatT, join_by:str=...) -> DataFormatT: ...
    def from_nato(self: DataFormatT, delimiter: Union[str, None]=None, join_by: str=...) -> DataFormatT: ...
    def swap_values(self: DataFormatT, indices1: Union[str, List[int]], indices2: Union[str, List[int]]) -> DataFormatT: ...
    def swap_strings(self: DataFormatT, by:int) -> DataFormatT: ...
    def to_string(self: DataFormatT) -> DataFormatT: ...
    def stringify(self: DataFormatT, compact:bool=...) -> DataFormatT: ...
    def select(self: DataFormatT, start: Union[int, str, bytes], end: Union[None, int]=None) -> DataFormatT: ...
    def length(self: DataFormatT) -> DataFormatT: ...
    def to_leetcode(self: DataFormatT, replace_space: str=...) -> DataFormatT: ...
    def substitute(self: DataFormatT, x: str=..., y: str=...) -> DataFormatT: ...
    def remove(self: DataFormatT, pattern: Union[str, bytes] = ...): ...
    def remove_nonprintable(self: DataFormatT, replace_with: Union[str, bytes] = ...): ...
    def to_base92(self: DataFormatT) -> DataFormatT: ...
    def from_base92(self: DataFormatT) -> DataFormatT: ...
    def to_base45(self: DataFormatT) -> DataFormatT: ...
    def from_base45(self: DataFormatT) -> DataFormatT: ...
    def to_base91(self: DataFormatT) -> DataFormatT: ...
    def from_base91(self: DataFormatT) -> DataFormatT: ...
    def swap_endianness(self: DataFormatT, word_length: int=4, pad_incomplete: bool=True) -> DataFormatT: ...
    def bruteforce_from_base_xx(self: DataFormatT) -> DataFormatT: ...
    def long_to_bytes(self: DataFormatT) -> DataFormatT: ...
    def bytes_to_long(self: DataFormatT) -> DataFormatT: ...
    def concat(self: DataFormatT, data: Union[str, bytes]) -> DataFormatT: ...
    def to_wingdings(self: DataFormatT) -> DataFormatT: ...
    def from_wingdings(self: DataFormatT) -> DataFormatT: ...
    def to_twin_hex(self: DataFormatT) -> DataFormatT: ...
    def from_twin_hex(self: DataFormatT) -> DataFormatT: ...
    def to_base36(self: DataFormatT, join_by: Union[str, bytes]=...) -> DataFormatT: ...
    def from_base36(self: DataFormatT, delimiter: Union[str, bytes]=..., join_by: Union[str, bytes]=...) -> DataFormatT: ...
    def to_pickle(self: DataFormatT) -> DataFormatT: ...
    def from_pickle(self: DataFormatT, trust: bool=...) -> DataFormatT: ...
    def to_bacon(self: DataFormatT, A: Literal['A', '0']=..., B: Literal['B', '1']=..., complete: bool=..., join_by: bytes=..., invert: bool=...) -> DataFormatT: ...
    def from_bacon(self: DataFormatT, A: Literal['A', '0']=..., B: Literal['B', '1']=..., complete: bool=..., split_by: bytes=..., invert: bool=...) -> DataFormatT: ...
    def to_upside_down(self: DataFormatT, reverse: bool=False) -> DataFormatT: ...
    def from_upside_down(self: DataFormatT, reverse: bool=False) -> DataFormatT: ...
    def to_messagepack(self: DataFormatT) -> DataFormatT: ...
    def from_messagepack(self: DataFormatT) -> DataFormatT: ...
    def unicode_escape(self: DataFormatT, padding: int = 0, uppercase_hex:bool=False) -> DataFormatT: ...
    def to_base(self: DataFormatT, radix: int=16) -> DataFormatT: ...
    def from_base(self: DataFormatT, radix: int=16) -> DataFormatT: ...
    def rotate_right(self: DataFormatT, radix: int=1, carry: bool=False) -> DataFormatT: ...
    def rotate_left(self: DataFormatT, radix: int=1, carry: bool=False) -> DataFormatT: ...
    def to_base62(self: DataFormatT, alphabet: str="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") -> DataFormatT: ...
    def from_base62(self: DataFormatT, alphabet: str="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") -> DataFormatT: ...
    def cut(self: DataFormatT, start: int, end: int) -> DataFormatT: ...
    def flatten(self: DataFormatT) -> DataFormatT: ...
    def to_utf21(self: DataFormatT) -> DataFormatT: ...
    def from_utf21(self: DataFormatT) -> DataFormatT: ...
    def to_uuencode(self: DataFormatT, header: str='-') -> DataFormatT: ...
    def from_uuencode(self: DataFormatT, header: str='-') -> DataFormatT: ...
    def from_quoted_printable(self: DataFormatT) -> DataFormatT: ...
    def to_quoted_printable(self: DataFormatT) -> DataFormatT: ...
    def from_rison(self: DataFormatT) -> DataFormatT: ...
    def to_rison(self: DataFormatT) -> DataFormatT: ...
    def increment_bytes(self: DataFormatT, n: int) -> DataFormatT: ...
    def decrement_bytes(self: DataFormatT, n: int) -> DataFormatT: ...
    def parse_csv(self: DataFormatT) -> DataFormatT: ...
    def parse_sqlite(self: DataFormatT, query: str) -> DataFormatT: ...
    def to_italics(self: DataFormatT) -> DataFormatT: ...
    def from_italics(self: DataFormatT) -> DataFormatT: ...
