import logging
from typing import Any, List, Mapping, Tuple, Union, TypeVar, Literal, Callable, Dict

jsonpickle: Any

ChepyCoreT = TypeVar('ChepyCoreT', bound='ChepyCore')

class ChepyDecorators:
    @staticmethod
    def call_stack(func: Any, *args: Any, **kwargs: Any): ...
    @staticmethod
    def is_stdout(func: Any, *args: Any, **kwargs: Any): ...

class ChepyCore:
    states: Any = ...
    buffers: Any = ...
    write: Any = ...
    bake: Any = ...
    cyberchef: Any = ...
    read_file: Any = ...
    log_level: Any = ...
    log_format: str = ...
    _registers: Dict[str, Union[str, bytes]] = ...
    _log: logging.Logger = ...
    def __init__(self, *data: Any) -> None: ...
    def _convert_to_bytes(self) -> bytes: ...
    def _to_bytes(self, data: Any) -> bytes: ...
    def _convert_to_bytearray(self) -> bytearray: ...
    def _convert_to_str(self) -> str: ...
    def _convert_to_int(self) -> int: ...
    def _get_nested_value(self: ChepyCoreT, data: dict, key:str, split_by: str=".") -> Any: ...
    def _str_to_bytes(self, s: str) -> bytes: ...
    def _bytes_to_str(self, s: bytes) -> str: ...
    @property
    def state(self): ...
    @state.setter
    def state(self: ChepyCoreT, val: Any) -> None: ...
    def fork(self: ChepyCoreT, methods: List[Union[Tuple[Union[str, Callable], dict], Tuple[Union[str, Callable],]]]) -> ChepyCoreT: ...
    def for_each(self: ChepyCoreT, methods: List[Union[Tuple[Union[str, Callable], dict], Tuple[Union[str, Callable],]]], merge: Union[str, bytes, None]=None) -> ChepyCoreT: ...
    def set_state(self: ChepyCoreT, data: Any) -> ChepyCoreT: ...
    def create_state(self: ChepyCoreT): ...
    def copy_state(self: ChepyCoreT, index: int=...) -> ChepyCoreT: ...
    def change_state(self: ChepyCoreT, index: int) -> ChepyCoreT: ...
    def switch_state(self: ChepyCoreT, index: int) -> ChepyCoreT: ...
    def delete_state(self: ChepyCoreT, index: int) -> ChepyCoreT: ...
    def get_state(self: ChepyCoreT, index: int) -> ChepyCoreT: ...
    def save_buffer(self: ChepyCoreT, index: int=...) -> ChepyCoreT: ...
    def load_buffer(self: ChepyCoreT, index: int) -> ChepyCoreT: ...
    def delete_buffer(self: ChepyCoreT, index: int) -> ChepyCoreT: ...
    def substring(self: ChepyCoreT, pattern: str, group: int=...) -> ChepyCoreT: ...
    @property
    def o(self): ...
    @property
    def out(self: ChepyCoreT) -> ChepyCoreT: ...
    def out_as_str(self: ChepyCoreT) -> str: ...
    def get_by_index(self: ChepyCoreT, index: int) -> ChepyCoreT: ...
    def get_by_key(self: ChepyCoreT, key: str, split_key: Union[str, None] = '.') -> ChepyCoreT: ...
    def copy_to_clipboard(self: ChepyCoreT) -> None: ...
    def copy(self: ChepyCoreT) -> None: ...
    def web(self: ChepyCoreT, magic: bool=..., cyberchef_url: str=...) -> None: ...
    def http_request(self: ChepyCoreT, method: str=..., params: dict=..., json: dict=..., headers: dict=..., cookies: dict=...) -> ChepyCoreT: ...
    def load_from_url(self: ChepyCoreT, method: str=..., params: dict=..., json: dict=..., headers: dict=..., cookies: dict=...) -> ChepyCoreT: ...
    def load_dir(self: ChepyCoreT, pattern: str=...) -> ChepyCoreT: ...
    def load_file(self: ChepyCoreT, binary_mode: bool=..., encoding: Union[str, None]=...) -> ChepyCoreT: ...
    def write_to_file(self: ChepyCoreT, path: str) -> None: ...
    def write_binary(self: ChepyCoreT, path: str) -> None: ...
    @property
    def recipe(self) -> List[Dict[str, Union[str, Dict[str, Any]]]]: ...
    def run_recipe(self: ChepyCoreT, recipes: List[Mapping[str, Union[str, Mapping[str, Any]]]]) -> ChepyCoreT: ...
    def save_recipe(self: ChepyCoreT, path: str) -> ChepyCoreT: ...
    def load_recipe(self: ChepyCoreT, path: str) -> ChepyCoreT: ...
    def run_script(self: ChepyCoreT, path: str, save_state: bool=...) -> ChepyCoreT: ...
    def loop(self: ChepyCoreT, iterations: int, callback: Union[str, Callable], args: dict=...) -> ChepyCoreT: ...
    def loop_list(self: ChepyCoreT, callback: Union[str, Callable], args: dict=...) -> ChepyCoreT: ...
    def loop_dict(self: ChepyCoreT, keys: list, callback: Union[str, Callable], args: dict=...) -> ChepyCoreT: ...
    def debug(self: ChepyCoreT, verbose: bool=...) -> ChepyCoreT: ...
    def reset(self: ChepyCoreT) -> ChepyCoreT: ...
    def print(self: ChepyCoreT) -> ChepyCoreT: ...
    def load_command(self: ChepyCoreT) -> ChepyCoreT: ...
    def pretty(self: ChepyCoreT, indent: int=...) -> ChepyCoreT: ...
    def plugins(self: ChepyCoreT, enable: Literal['true', 'false']) -> None: ...
    def set_plugin_path(self: ChepyCoreT, path: str) -> None: ...
    def subsection(self: ChepyCoreT, pattern: str, methods: List[Tuple[Union[str, object], dict]], group: int=...) -> ChepyCoreT: ...
    def callback(self: ChepyCoreT, callback_function: Callable[[Any], Any]) -> ChepyCoreT: ...
    def register(self: ChepyCoreT, pattern: Union[str, bytes], ignore_case: bool=False, multiline: bool=False, dotall: bool=False, unicode: bool=False, extended: bool=False) -> ChepyCoreT: ...
    def get_register(self: ChepyCoreT, key: str) -> Union[str, bytes]: ...
    def set_register(self, key: str, val: Union[str, bytes]) -> ChepyCoreT: ...
