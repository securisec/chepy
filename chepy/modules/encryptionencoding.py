import codecs
import string
import itertools
import base64
import binascii
import jwt
import pathlib
import ujson
import pycipher
import regex as re

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import ARC4
from Crypto.Cipher import DES, DES3, AES
from Crypto.Cipher import Blowfish

from ..core import ChepyCore, ChepyDecorators
from .internal.constants import EncryptionConsts
from ..extras.combinatons import hex_chars


class EncryptionEncoding(ChepyCore):
    """This class handles most operations related to various encryption 
    related operations. This class inherits the ChepyCore class, and all the 
    methods are also available from the Chepy class
    
    Examples:
        >>> from chepy import Chepy
        or
        >>> from chepy.modules.encryptionencoding import EncryptionEncoding
    """

    def __check_mode(self, mode) -> None:
        assert mode in ["CBC", "OFB", "CTR", "ECB"], "Not a valid mode."

    def _convert_key(self, key, iv, hex_key, hex_iv):  # pragma: no cover
        if isinstance(key, str):
            key = key.encode()
        if hex_key:
            key = binascii.unhexlify(key)
        if isinstance(iv, str):
            iv = iv.encode()
        if hex_iv:
            iv = binascii.unhexlify(iv)
        else:
            iv = binascii.unhexlify(binascii.hexlify(iv))
        return key, iv

    @ChepyDecorators.call_stack
    def rotate(self, rotate_by: int):
        """Rotate string by provided number
        
        Args:
            rotate_by (int): Required. Number to rotate by
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            In this example, we will rotate by 20

            >>> Chepy("some data").rotate(20).output
            "migy xunu"
        """
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        lookup = str.maketrans(
            lc + uc, lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by]
        )
        self.state = self.state.translate(lookup)
        return self

    @ChepyDecorators.call_stack
    def rot_13(self):
        """ROT-13 encoding
        
        A simple caesar substitution cipher which rotates alphabet 
        characters by the specified amount (default 13).
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = codecs.encode(self._convert_to_str(), "rot_13")
        return self

    @ChepyDecorators.call_stack
    def rot_47(self):
        """ROT 47 encoding
        
        A slightly more complex variation of a caesar cipher, which includes 
        ASCII characters from 33 '!' to 126 '~'. Default rotation: 47.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some").rot_47().output
            "D@>6"
        """
        x = []
        for i in range(len(self.state)):
            j = ord(self.state[i])
            if j >= 33 and j <= 126:
                x.append(chr(33 + ((j + 14) % 94)))
            else:  # pragma: no cover
                x.append(self.state[i])
        self.state = "".join(x)
        return self

    @ChepyDecorators.call_stack
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
            key (str): Required. The key to xor by
            key_type (str, optional): The key type. Valid values are hex, utf and base64. Defaults to "hex".
            ascii (bool, optional): If the input is in ascii format
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("secret").xor(key="secret", key_type="utf").to_hex()
            000000000000
        """
        assert key_type in [
            "utf",
            "hex",
            "base64",
        ], "Valid key types are hex, utf and base64"

        if isinstance(key, int):
            key = str(key)
        if key_type == "utf":
            key = binascii.hexlify(key.encode())
        elif key_type == "base64":
            key = binascii.hexlify(base64.b64decode(key.encode()))
        key = binascii.unhexlify(key)
        xor = bytearray(b"")
        if ascii:
            for char, key_val in zip(self._convert_to_str(), itertools.cycle(key)):
                xor.append(ord(char) ^ key_val)
        else:
            for char, key_val in zip(self._convert_to_bytes(), itertools.cycle(key)):
                xor.append(char ^ key_val)

        self.state = xor
        return self

    @ChepyDecorators.call_stack
    def xor_bruteforce(self, length: int = 100):
        """Brute force single byte xor

        For multibyte xor bruteforce, use chepy.extras.crypto_extras.xor_bruteforce_multi 
        function
        
        Args:
            length (int, optional): How to bytes to bruteforce. Defaults to 100.
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("pf`qfw").xor_bruteforce()
            {'00': bytearray(b'pf`qfw'),
            '01': bytearray(b'qgapgv'),
            '02': bytearray(b'rdbsdu'),
            '03': bytearray(b'secret'), # here is our secret xored with the hex key 03
            '04': bytearray(b'tbdubs'),
            '05': bytearray(b'ucetcr'),
            ...}
            >>> c.get_by_key("03").bytearray_to_str()
            secret
            >>> c.xor("03").bytearray_to_str()
            pf`qfw
        """
        original = self.state
        found = {}
        keys = hex_chars()
        self.state = original[:length]
        for key in keys:
            self.xor(key)
            found[key] = self.state
            self.state = original[:length]
        self.state = found
        return self

    @ChepyDecorators.call_stack
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

    @ChepyDecorators.call_stack
    def jwt_verify(self, secret: str, algorithm: list = ["HS256"]):
        """Verify JWT token
        
        Args:
            secret (str): Required. Secret key for token
            algorithm (list, optional): Array of valid algorithms. Defaults to ["HS256"]
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = jwt.decode(
            self._convert_to_str(), key=secret, algorithms=algorithm
        )
        return self

    @ChepyDecorators.call_stack
    def jwt_sign(self, secret: str, algorithms: str = "HS256"):
        """Sign a json/dict object in JWT
        
        Args:
            secret (str): Required. Secret to sign with
            algorithms (str, optional): Signing algorithm. Defaults to "HS256".
        
        Returns:
            Chepy: The Chepy object. 
        """
        if isinstance(self.state, dict):
            data = self.state
        elif isinstance(self.state, str):
            data = ujson.loads(self.state)
        self.state = jwt.encode(data, key=secret, algorithm=algorithms)
        return self

    @ChepyDecorators.call_stack
    def jwt_bruteforce(
        self, wordlist: str, b64_encode: bool = False, algorithm: list = ["HS256"]
    ):
        """Brute force JWT token secret

        This method will use the provided wordlist to try and bruteforce the 
        verification.
        
        Args:
            wordlist (str): Required. Path to a wordlist
            b64_encode (bool, optional): Encoded the words in base64. Defaults to False.
            algorithm (list, optional): Array of valid algorithms. Defaults to ["HS256"].
        
        Returns:
            Chepy: The Chepy object. 
        """
        with open(pathlib.Path(wordlist).expanduser().absolute()) as words:
            for word in words:
                try:
                    word = word.strip()
                    if b64_encode:  # pragma: no cover
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
            else:  # pragma: no cover
                return self

    @ChepyDecorators.call_stack
    def rc4_encrypt(self, key: str, hex_key: bool = False):
        """Encrypt raw state with RC4
        
        Args:
            key (str): Required. Secret key
            hex_key (bool, optional): If key is in hex. Defaults to False.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some data").rc4_encrypt("736563726574", hex_key=True).o
            b"9e59bf79a2c0b7d253"
        """
        if hex_key:
            key = binascii.unhexlify(key)
        if isinstance(key, str):
            key = key.encode()
        cipher = ARC4.new(key)
        self.state = binascii.hexlify(cipher.encrypt(self._convert_to_bytes()))
        return self

    @ChepyDecorators.call_stack
    def rc4_decrypt(self, key: str, hex_key: bool = False):
        """Decrypt raw state with RC4
        
        Args:
            key (str): Required. Secret key
            hex_key (bool, optional): If key is in hex. Defaults to False.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("9e59bf79a2c0b7d253").hex_to_str().rc4_decrypt("secret").o
            b"some data"
        """
        if hex_key:
            key = binascii.unhexlify(key)
        if isinstance(key, str):
            key = key.encode()
        cipher = ARC4.new(key)
        self.state = cipher.decrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def des_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        hex_key: bool = False,
        hex_iv: bool = True,
    ):
        """Encrypt raw state with DES

        DES is a previously dominant algorithm for encryption, and was published 
        as an official U.S. Federal Information Processing Standard (FIPS). It is 
        now considered to be insecure due to its small key size. DES uses a key 
        length of 8 bytes (64 bits).<br>Triple DES uses a key length of 24 bytes. 
        You can generate a password-based key using one of the KDF operations. 
        The Initialization Vector should be 8 bytes long. If not entered, it will 
        default to 8 null bytes. Padding: In CBC and ECB mode, PKCS#7 padding will be used.
        
        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some data").des_encrypt("70617373776f7264", hex_key=True).o
            b"1ee5cb52954b211d1acd6e79c598baac"

            To encrypt using a differnt mode

            >>> Chepy("some data").des_encrypt("password", mode="CTR").o
            b"0b7399049b0267d93d"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, hex_key, hex_iv)

        if mode == "CBC":
            cipher = DES.new(key, mode=DES.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = DES.new(key, mode=DES.MODE_ECB)
            self.state = cipher.encrypt(pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "CTR":
            cipher = DES.new(key, mode=DES.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES.new(key, mode=DES.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def des_decrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        hex_key: bool = False,
        hex_iv: bool = True,
    ):
        """Decrypt raw state encrypted with DES. 

        DES is a previously dominant algorithm for encryption, and was published 
        as an official U.S. Federal Information Processing Standard (FIPS). It is 
        now considered to be insecure due to its small key size. DES uses a key 
        length of 8 bytes (64 bits).<br>Triple DES uses a key length of 24 bytes. 
        You can generate a password-based key using one of the KDF operations. 
        The Initialization Vector should be 8 bytes long. If not entered, it will 
        default to 8 null bytes. Padding: In CBC and ECB mode, PKCS#7 padding will be used.
        
        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("1ee5cb52954b211d1acd6e79c598baac").hex_to_str().des_decrypt("password").o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, hex_key, hex_iv)

        if mode == "CBC":
            cipher = DES.new(key, mode=DES.MODE_CBC, iv=iv)
            self.state = unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = DES.new(key, mode=DES.MODE_ECB)
            self.state = unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CTR":
            cipher = DES.new(key, mode=DES.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES.new(key, mode=DES.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def triple_des_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        hex_key: bool = False,
        hex_iv: bool = True,
    ):
        """Encrypt raw state with Triple DES

        Triple DES applies DES three times to each block to increase key size. Key: 
        Triple DES uses a key length of 24 bytes (192 bits).<br>DES uses a key length 
        of 8 bytes (64 bits).<br><br>You can generate a password-based key using one 
        of the KDF operations. IV: The Initialization Vector should be 8 bytes long. 
        If not entered, it will default to 8 null bytes. Padding: In CBC and ECB 
        mode, PKCS#7 padding will be used.
        
        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some data").triple_des_encrypt("super secret password !!", mode="ECB").o
            b"f8b27a0d8c837edc8fb00ea85f502fb4"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, hex_key, hex_iv)

        if mode == "CBC":
            cipher = DES3.new(key, mode=DES3.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = DES3.new(key, mode=DES3.MODE_ECB)
            self.state = cipher.encrypt(pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "CTR":
            cipher = DES3.new(key, mode=DES3.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES3.new(key, mode=DES3.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def triple_des_decrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        hex_key: bool = False,
        hex_iv: bool = True,
    ):
        """Decrypt raw state encrypted with DES. 

        Triple DES applies DES three times to each block to increase key size. Key: 
        Triple DES uses a key length of 24 bytes (192 bits).<br>DES uses a key length 
        of 8 bytes (64 bits).<br><br>You can generate a password-based key using one 
        of the KDF operations. IV: The Initialization Vector should be 8 bytes long. 
        If not entered, it will default to 8 null bytes. Padding: In CBC and ECB 
        mode, PKCS#7 padding will be used.
        
        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("f8b27a0d8c837edce87dd13a1ab41f96")
            >>> c.hex_to_str()
            >>> c.triple_des_decrypt("super secret password !!")
            >>> c.o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, hex_key, hex_iv)

        if mode == "CBC":
            cipher = DES3.new(key, mode=DES3.MODE_CBC, iv=iv)
            self.state = unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = DES3.new(key, mode=DES3.MODE_ECB)
            self.state = unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CTR":
            cipher = DES3.new(key, mode=DES3.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES3.new(key, mode=DES3.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def aes_encrypt(
        self,
        key: str,
        iv: str = "00000000000000000000000000000000",
        mode: str = "CBC",
        hex_key: bool = False,
        hex_iv: bool = True,
    ):
        """Encrypt raw state with AES

        Advanced Encryption Standard (AES) is a U.S. Federal Information Processing 
        Standard (FIPS). It was selected after a 5-year process where 15 competing 
        designs were evaluated.
        
        key: The following algorithms will be used based on the size of the 
            16 bytes = AES-128
            24 bytes = AES-192
            32 bytes = AES-256
        
        You can generate a password-based key using one of the KDF operations. 
        IV: The Initialization Vector should be 16 bytes long. If not entered, it will 
        default to 16 null bytes. Padding: In CBC and ECB mode, PKCS#7 padding will be used.
        
        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. 
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some data").aes_encrypt("secret password!", mode="ECB").o
            b"5fb8c186394fc399849b89d3b6605fa3"
        """

        assert mode in ["CBC", "OFB", "CTR", "ECB", "GCM"], "Not a valid mode."

        key, iv = self._convert_key(key, iv, hex_key, hex_iv)

        if mode == "CBC":
            cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(pad(self._convert_to_bytes(), 16))
            return self
        elif mode == "ECB":
            cipher = AES.new(key, mode=AES.MODE_ECB)
            self.state = cipher.encrypt(pad(self._convert_to_bytes(), 16))
            return self
        elif mode == "CTR":
            cipher = AES.new(key, mode=AES.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "GCM":
            cipher = AES.new(
                key,
                mode=AES.MODE_GCM,
                nonce=binascii.unhexlify("00000000000000000000000000000000"),
            )
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = AES.new(key, mode=AES.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def aes_decrypt(
        self,
        key: str,
        iv: str = "00000000000000000000000000000000",
        mode: str = "CBC",
        hex_key: bool = False,
        hex_iv: bool = True,
    ):
        """Decrypt raw state encrypted with DES. 

        Advanced Encryption Standard (AES) is a U.S. Federal Information Processing 
        Standard (FIPS). It was selected after a 5-year process where 15 competing 
        designs were evaluated.<br><br><b>Key:</b> The following algorithms will 
        be used based on the size of the 
        
        key:
            16 bytes = AES-128
            24 bytes = AES-192
            32 bytes = AES-256
        
        You can generate a password-based key using one of the KDF operations. 
        IV: The Initialization Vector should be 16 bytes long. If not entered, it will 
        default to 16 null bytes. Padding: In CBC and ECB mode, PKCS#7 padding will be used.
        
        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. 
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("5fb8c186394fc399849b89d3b6605fa3")
            >>> c.hex_to_str()
            >>> c.aes_decrypt("7365637265742070617373776f726421", hex_key=True)
            >>> c.o
            b"some data"
        """

        assert mode in ["CBC", "OFB", "CTR", "ECB", "GCM"], "Not a valid mode."

        key, iv = self._convert_key(key, iv, hex_key, hex_iv)

        if mode == "CBC":
            cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
            self.state = unpad(cipher.decrypt(self._convert_to_bytes()), 16)
            return self
        elif mode == "ECB":
            cipher = AES.new(key, mode=AES.MODE_ECB)
            self.state = unpad(cipher.decrypt(self._convert_to_bytes()), 16)
            return self
        elif mode == "CTR":
            cipher = AES.new(key, mode=AES.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "GCM":
            cipher = AES.new(
                key,
                mode=AES.MODE_GCM,
                nonce=binascii.unhexlify("00000000000000000000000000000000"),
            )
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = AES.new(key, mode=AES.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def blowfish_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        hex_key: bool = False,
        hex_iv: bool = True,
    ):
        """Encrypt raw state with Blowfish

        Blowfish is a symmetric-key block cipher designed in 1993 by 
        Bruce Schneier and included in a large number of cipher suites 
        and encryption products. AES now receives more attention.
        IV: The Initialization Vector should be 8 bytes long.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("some data").blowfish_encrypt("password", mode="ECB").o
            b"d9b0a79853f139603951bff96c3d0dd5"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, hex_key, hex_iv)

        if mode == "CBC":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_ECB)
            self.state = cipher.encrypt(pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "CTR":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def blowfish_decrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        hex_key: bool = False,
        hex_iv: bool = True,
    ):
        """Encrypt raw state with Blowfish

        Blowfish is a symmetric-key block cipher designed in 1993 by 
        Bruce Schneier and included in a large number of cipher suites 
        and encryption products. AES now receives more attention.
        IV: The Initialization Vector should be 8 bytes long.
        
        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. 
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("d9b0a79853f13960fcee3cae16e27884")
            >>> c.hex_to_str()
            >>> c.blowfish_decrypt("password")
            >>> c.o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, hex_key, hex_iv)

        if mode == "CBC":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, iv=iv)
            self.state = unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_ECB)
            self.state = unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CTR":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def vigenere_encode(self, key: str):
        """Encode with Vigenere ciper
        
        Args:
            key (str): Required. The secret key
        
        Returns:
            Chepy: The Chepy oject. 

        Examples:
            >>> Chepy("secret").vigenere_encode("secret").o
            "KIEIIM"
        """
        self.state = pycipher.Vigenere(key=key).encipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def vigenere_decode(self, key: str):
        """Decode Vigenere ciper
        
        Args:
            key (str): Required. The secret key
        
        Returns:
            Chepy: The Chepy oject. 

        Examples:
            >>> Chepy("KIEIIM").vigenere_decode("secret").o
            "SECRET"
        """
        self.state = pycipher.Vigenere(key=key).decipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def affine_encode(self, a: int = 1, b: int = 1):
        """Encode with Affine ciper
        
        Args:
            a (int, optional): Multiplier value. Defaults to 1
            b (int, optional): Additive value. Defaults to 1
        
        Returns:
            Chepy: The Chepy oject. 

        Examples:
            >>> Chepy("secret").affine_encode().o
            "TFDSFU"
        """
        self.state = pycipher.Affine(a=a, b=b).encipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def affine_decode(self, a: int = 1, b: int = 1):
        """Decode Affine ciper
        
        Args:
            a (int, optional): Multiplier value. Defaults to 1
            b (int, optional): Additive value. Defaults to 1
        
        Returns:
            Chepy: The Chepy oject. 

        Examples:
            >>> Chepy("TFDSFU").affine_decode().o
            "SECRET"
        """
        self.state = pycipher.Affine(a=a, b=b).decipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def atbash_encode(self):
        """Encode with Atbash ciper
        
        Returns:
            Chepy: The Chepy oject. 

        Examples:
            >>> Chepy("secret").atbash_encode().o
            "HVXIVG"
        """
        self.state = pycipher.Atbash().encipher(self._convert_to_str(), keep_punct=True)
        return self

    @ChepyDecorators.call_stack
    def atbash_decode(self):
        """Decode Atbash ciper
        
        Returns:
            Chepy: The Chepy oject. 

        Examples:
            >>> Chepy("hvxivg").atbash_decode().o
            "SECRET"
        """
        self.state = pycipher.Atbash().decipher(self._convert_to_str(), keep_punct=True)
        return self

    @ChepyDecorators.call_stack
    def to_morse_code(
        self,
        dot: str = ".",
        dash: str = "-",
        letter_delim: str = " ",
        word_delim: str = "\n",
    ):
        """Encode string to morse code
        
        Args:
            dot (str, optional): The char for dot. Defaults to ".".
            dash (str, optional): The char for dash. Defaults to "-".
            letter_delim (str, optional): Letter delimiter. Defaults to " ".
            word_delim (str, optional): Word delimiter. Defaults to "\\n".
        
        Returns:
            Chepy: The Chepy object. 
        """
        encode = ""
        morse_code_dict = EncryptionConsts.MORSE_CODE_DICT
        for k, v in morse_code_dict.items():
            morse_code_dict[k] = v.replace(".", dot).replace("-", dash)
        for word in self._convert_to_str().split():
            for w in word:
                encode += morse_code_dict.get(w.upper()) + letter_delim
            encode += word_delim
        self.state = encode
        return self

    @ChepyDecorators.call_stack
    def from_morse_code(
        self,
        dot: str = ".",
        dash: str = "-",
        letter_delim: str = " ",
        word_delim: str = "\n",
    ):
        """Decode morse code
        
        Args:
            dot (str, optional): The char for dot. Defaults to ".".
            dash (str, optional): The char for dash. Defaults to "-".
            letter_delim (str, optional): Letter delimiter. Defaults to " ".
            word_delim (str, optional): Word delimiter. Defaults to "\\n".
        
        Returns:
            Chepy: The Chepy object. 
        """
        decode = ""
        morse_code_dict = EncryptionConsts.MORSE_CODE_DICT
        for k, v in morse_code_dict.items():
            morse_code_dict[k] = v.replace(".", dot).replace("-", dash)

        morse_code_dict = {value: key for key, value in morse_code_dict.items()}

        for chars in self._convert_to_str().split(letter_delim):
            if word_delim in chars:
                print("here", chars)
                chars = re.sub(word_delim, "", chars, re.I)
                print(chars)
                if morse_code_dict.get(chars) is not None:
                    decode += " " + morse_code_dict.get(chars)
            else:
                decode += morse_code_dict.get(chars)
        self.state = decode
        return self
