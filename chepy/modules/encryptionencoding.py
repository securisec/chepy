import codecs
import string
import re
import itertools
import base64
import binascii

from ..core import Core


class EncryptionEncoding(Core):
    def rotate(self, rotate_by: int):
        """Rotate string by provided number
        
        Args:
            rotate_by (int): Number to rotate by
        
        Returns:
            Chepy: The Chepy object.
        """
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        lookup = str.maketrans(
            lc + uc, lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by]
        )
        self.state = self.state.translate(lookup)
        return self

    def rot_13(self):
        """ROT-13 encoding
        
        A simple caesar substitution cipher which rotates alphabet 
        characters by the specified amount (default 13).
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = codecs.encode(self._convert_to_str(), "rot_13")
        return self

    def rot_47(self):
        """ROT 47 encoding
        
        A slightly more complex variation of a caesar cipher, which includes 
        ASCII characters from 33 '!' to 126 '~'. Default rotation: 47.
        
        Returns:
            Chepy: The Chepy object. 
        """
        x = []
        for i in range(len(self.state)):
            j = ord(self.state[i])
            if j >= 33 and j <= 126:
                x.append(chr(33 + ((j + 14) % 94)))
            else:
                x.append(self.state[i])
        self.state = "".join(x)
        return self

    def xor(self, key: str, key_type: str = "hex"):
        """XOR cipher

        Simple XOR cipher is a type of additive cipher based on logical operation xor.

        Returns:
            Chepy: The Chepy object. 
        """
        assert re.search(r"[a-fA-F0-9]+", self.state), "Need a valid hex string"
        assert key_type in ["utf", "hex", "base64"], "Need a valid key type"
        if key_type == "utf":
            key = binascii.hexlify(key.encode())
        elif key_type == "base64":
            key = binascii.hexlify(base64.b64decode(key.encode()))
        key = codecs.decode(key, "hex")
        self.state = "".join(chr(ord(a) ^ b) for (a, b) in zip(self.state, itertools.cycle(key)))
        return self