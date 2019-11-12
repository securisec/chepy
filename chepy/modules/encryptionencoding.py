import codecs
import string
import itertools
import base64
import binascii
import jwt
import pathlib
import json
import regex as re

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

    def xor(self, key: str, key_type: str = "hex", ascii: bool = False):
        """XOR state with a key

        Valid key formats are utf, hex and base64. Simple XOR cipher is a type 
        of additive cipher based on logical operation xor, which operates according 
        to the following principles.

        (A * B) + (!A * !B)

        A  B  A XOR B
        0  0     0
        1  0     1
        0  1     1
        1  1     0

        The main advantage of xor chipher is that the encyption is reversible with t
        he same logical operation.
        
        Args:
            key (str): The key to xor by
            key_type (str, optional): The key type. Valid values are hex, utf and base64. Defaults to "hex".
            ascii (bool, optional): If the input is in ascii format
        
        Returns:
            Chepy: The Chepy object. 
        """
        assert key_type in [
            "utf",
            "hex",
            "base64",
        ], "Valid key types are hex, utf and base64"

        if key_type == "utf":
            key = binascii.hexlify(key.encode())
        elif key_type == "base64":
            key = binascii.hexlify(base64.b64decode(key.encode()))
        if isinstance(key, int):
            key = str(key)
        key = codecs.decode(key, "hex")
        xor = bytearray(b"")
        if ascii:
            for char, key_val in zip(self._convert_to_str(), itertools.cycle(key)):
                xor.append(ord(char) ^ key_val)
        else:
            for char, key_val in zip(self._convert_to_bytes(), itertools.cycle(key)):
                xor.append(char ^ key_val)

        self.state = xor
        return self

    def jwt_decode(self):
        """Decode a JWT token. Does not verify
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = {
            "payload": jwt.decode(self._convert_to_str(), verify=False),
            "header": jwt.get_unverified_header(self._convert_to_str()),
        }
        return self

    def jwt_verify(self, secret: str, algorithm: list = ["HS256"]):
        """Verify JWT token
        
        Args:
            secret (str): Secret key for token
            algorithm (list, optional): Array of valid algorithms. Defaults to ["HS256"]
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = jwt.decode(
            self._convert_to_str(), key=secret, algorithms=algorithm
        )
        return self

    def jwt_sign(self, secret: str, algorithms: str = "HS256"):
        """Sign a json/dict object in JWT
        
        Args:
            secret (str): Secret to sign with
            algorithms (str, optional): Signing algorithm. Defaults to "HS256".
        
        Returns:
            Chepy: The Chepy object. 
        """
        if isinstance(self.state, dict):
            data = self.state
        elif isinstance(self.state, str):
            data = json.loads(self.state)
        self.state = jwt.encode(data, key=secret, algorithm=algorithms)
        return self

    def jwt_bruteforce(
        self, wordlist: str, b64_encode: bool = False, algorithm: list = ["HS256"]
    ):
        """Brute force JWT token secret

        This method will use the provided wordlist to try and bruteforce the 
        verification.
        
        Args:
            wordlist (str): Path to a wordlist
            b64_encode (bool, optional): Encoded the words in base64. Defaults to False.
            algorithm (list, optional): Array of valid algorithms. Defaults to ["HS256"].
        
        Returns:
            Chepy: The Chepy object. 
        """
        with open(pathlib.Path(wordlist).expanduser().absolute()) as words:
            for word in words:
                try:
                    word = word.strip()
                    if b64_encode:
                        word = base64.b64encode(word)
                    j = jwt.decode(self._convert_to_str(), word, algorithms=algorithm)
                    self.state = {
                        "paylod": j,
                        "header": jwt.get_unverified_header(self._convert_to_str()),
                        "secret": word,
                    }
                    return self
                except jwt.InvalidSignatureError:
                    continue
            else:
                return self
