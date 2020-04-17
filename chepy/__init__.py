import re

from docstring_parser import parse as _doc_parse

from .modules.aritmeticlogic import AritmeticLogic
from .modules.codetidy import CodeTidy
from .modules.compression import Compression
from .modules.dataformat import DataFormat
from .modules.datetimemodule import DateTime
from .modules.encryptionencoding import EncryptionEncoding
from .modules.extractors import Extractors
from .modules.hashing import Hashing
from .modules.language import Language
from .modules.links import Links
from .modules.multimedia import Multimedia
from .modules.networking import Networking
from .modules.other import Other
from .modules.publickey import Publickey
from .modules.search import Search
from .modules.utils import Utils
from .modules.internal.colors import cyan

from .config import ChepyConfig

_plugins = ChepyConfig().load_plugins()


class Chepy(
    AritmeticLogic,
    CodeTidy,
    Compression,
    DataFormat,
    DateTime,
    EncryptionEncoding,
    Extractors,
    Hashing,
    Language,
    Links,
    Multimedia,
    Networking,
    Other,
    Publickey,
    Search,
    Utils,
    *_plugins
):
    pass


def search_chepy_methods(search: str) -> None:  # pragma: no cover
    """Search for Chepy methods
    
    Args:
        search (str): String to search for
    """
    methods = dir(Chepy)
    for method in methods:
        if search in method and not method.startswith("_"):
            docs = _doc_parse(getattr(Chepy, method).__doc__).short_description
            print(cyan(method), docs)
