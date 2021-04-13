from typing import Any

class StateNotList(Exception):
    def __init__(self, msg: str = ..., *args: Any, **kwargs: Any) -> None: ...

class StateNotDict(Exception):
    def __init__(self, msg: str = ..., *args: Any, **kwargs: Any) -> None: ...
