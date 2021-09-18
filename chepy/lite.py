from .modules.aritmeticlogic import AritmeticLogic
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

class ChepyLite(
    AritmeticLogic,
    Compression,
    DataFormat,
    DateTime,
    EncryptionEncoding,
    Extractors,
    Hashing,
    Language,
    Links,
    Networking,
    Other,
    Publickey,
    Search,
    Utils,
):
    """Chepy Lite class. Chepy lite is a lightweight version of Chepy which offers 
    most of the core functionalities of Chepy, but without any extensions or extra 
    modules. This is so that Chepy load time can be faster.
    """
    pass