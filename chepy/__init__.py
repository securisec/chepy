from .modules.dataformat import DataFormat
from .modules.encryptionencoding import EncryptionEncoding
from .modules.utils import Utils


class Chepy(DataFormat, EncryptionEncoding, Utils):
    pass
