import codecs
import string

from ..core import Core


class EncryptionEncoding(Core):
    def rotate(self, rotate_by: int) -> "Chepy":
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        lookup = str.maketrans(
            lc + uc, lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by]
        )
        self._holder = self._holder.translate(lookup)
        return self

    @property
    def rot_13(self) -> "Chepy":
        self._holder = codecs.encode(self._convert_to_str(), "rot_13")
        return self

    @property
    def rot_47(self) -> "Chepy":
        x = []
        for i in range(len(self._holder)):
            j = ord(self._holder[i])
            if j >= 33 and j <= 126:
                x.append(chr(33 + ((j + 14) % 94)))
            else:
                x.append(self._holder[i])
        self._holder = "".join(x)
        return self
