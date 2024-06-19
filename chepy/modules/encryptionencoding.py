import base64
import binascii
import codecs
import itertools
import string
import random
from typing import Literal, TypeVar, Dict, Any, Union
from .internal.ls47 import (
    encrypt_pad as _ls47_enc,
    decrypt_pad as _ls47_dec,
    derive_key as _derive_key,
)
from .internal.constants import Ciphers, Rabbit
from .internal.helpers import detect_delimiter

import lazy_import

jwt = lazy_import.lazy_module("jwt")

import regex as re
import json

AES = lazy_import.lazy_module("Crypto.Cipher.AES")
ARC4 = lazy_import.lazy_module("Crypto.Cipher.ARC4")
DES = lazy_import.lazy_module("Crypto.Cipher.DES")
ChaCha20 = lazy_import.lazy_module("Crypto.Cipher.ChaCha20")
DES3 = lazy_import.lazy_module("Crypto.Cipher.DES3")
RSA = lazy_import.lazy_module("Crypto.PublicKey.RSA")
Hash = lazy_import.lazy_module("Crypto.Hash")
Counter = lazy_import.lazy_module("Crypto.Util.Counter")
PKCS1_15 = lazy_import.lazy_module("Crypto.Signature.pkcs1_15")
PKCS1_OAEP = lazy_import.lazy_module("Crypto.Cipher.PKCS1_OAEP")
PKCS1_v1_5 = lazy_import.lazy_module("Crypto.Cipher.PKCS1_v1_5")
Blowfish = lazy_import.lazy_module("Crypto.Cipher.Blowfish")
Padding = lazy_import.lazy_module("Crypto.Util.Padding")
pycipher = lazy_import.lazy_module("pycipher")
Fernet = lazy_import.lazy_callable("cryptography.fernet.Fernet")

from ..core import ChepyCore, ChepyDecorators
from ..extras.combinatons import hex_chars
from .internal.constants import EncryptionConsts

EncryptionEncodingT = TypeVar("EncryptionEncodingT", bound="EncryptionEncoding")


class EncryptionEncoding(ChepyCore):
    """This class handles most operations related to various encryption
    related operations. This class inherits the ChepyCore class, and all the
    methods are also available from the Chepy class

    Examples:
        >>> from chepy import Chepy
        or
        >>> from chepy.modules.encryptionencoding import EncryptionEncoding
    """

    def __init__(self, *data):
        super().__init__(*data)

    def __check_mode(self, mode) -> None:
        assert mode in ["CBC", "OFB", "CTR", "ECB"], "Not a valid mode."

    def _convert_key(
        self, key, iv, key_format: str, iv_format: str
    ) -> EncryptionEncodingT:  # pragma: no cover
        key = self._str_to_bytes(key)
        # modify key according to mode
        if key_format == "hex":
            key = binascii.unhexlify(key)
        if key_format == "base64" or key_format == "b64":
            key = base64.b64decode(key)
        if key_format == "utf-8" or key_format == "utf8":
            key = key.decode().encode("utf-8")
        if key_format == "latin-1":
            key = key.decode().encode("latin-1")
        if key_format == "raw":
            key = key

        # modify iv according to mode
        iv = self._str_to_bytes(iv)
        if iv_format == "hex":
            iv = binascii.unhexlify(iv)
        if iv_format == "base64" or iv_format == "b64":
            iv = base64.b64decode(iv)
        if iv_format == "utf-8" or iv_format == "utf8":
            iv = iv.decode().encode("utf-8")
        if iv_format == "latin-1":
            iv = iv.decode().encode("latin-1")
        if iv_format == "raw":
            iv = iv
        else:
            iv = binascii.unhexlify(binascii.hexlify(iv))
        return key, iv

    def _rsa_process_key(self, key: str, is_file: bool, passphrase=None):
        """Returns an RSA instance for either keyfile or string key"""
        if is_file:
            with open(str(self._abs_path(key)), "r") as f:
                return RSA.import_key(f.read(), passphrase)
        return RSA.import_key(key, passphrase)

    def _rsa_cipher(self, c_format: str, rsa):
        """Returns an RSA Cipher instance based for cipher type"""
        if c_format == "PKCS":
            return PKCS1_v1_5.new(rsa)
        return PKCS1_OAEP.new(rsa)

    @ChepyDecorators.call_stack
    def rotate(self, rotate_by: int) -> EncryptionEncodingT:
        """Rotate string by provided number

        Args:
            rotate_by (int): Required. Number to rotate by

        Returns:
            Chepy: The Chepy object.

        Examples:
            In this example, we will rotate by 20

            >>> Chepy("some data").rotate(20).out
            "migy xunu"
        """
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        lookup = str.maketrans(
            lc + uc, lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by]
        )
        self.state = self.state.translate(lookup).encode()
        return self

    @ChepyDecorators.call_stack
    def rotate_bruteforce(self) -> EncryptionEncodingT:
        """Brute force rotation from 1 to 26.
        Returned value is a dict where key is the rotation count.

        Returns:
            Chepy: The Chepy object.

        Examples:
            In this example, we will rotate by 20

            >>> Chepy('uryyb').rotate_bruteforce()
            {
                '1': 'vszzc',
                '2': 'wtaad',
                ...
                '13': 'hello',
                ...
            }
        """
        hold = {}
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        for rotate_by in range(1, 27):
            lookup = str.maketrans(
                lc + uc,
                lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by],
            )
            hold[str(rotate_by)] = self.state.translate(lookup).encode()
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def rot_13(self, amount=13, rotate_lower=True, rotate_upper=True, rotate_numbers=False) -> EncryptionEncodingT:
        """Rot 13

        Args:
            amount (int, optional): Rotate amount. Defaults to 13.
            rotate_lower (bool, optional): Rotate lowercase. Defaults to True.
            rotate_upper (bool, optional): Rotate uppercase. Defaults to True.
            rotate_numbers (bool, optional): Rotate numbers. Defaults to False.

        Returns:
            Chepy: The Chepy object. 
        """
        text = self._convert_to_str()
        result = []
        for char in text:
            if rotate_lower and 'a' <= char <= 'z':  # Lowercase letters
                result.append(chr((ord(char) - ord('a') + amount) % 26 + ord('a')))
            elif rotate_upper and 'A' <= char <= 'Z':  # Uppercase letters
                result.append(chr((ord(char) - ord('A') + amount) % 26 + ord('A')))
            elif rotate_numbers and '0' <= char <= '9':  # Numbers
                result.append(chr((ord(char) - ord('0') + amount) % 10 + ord('0')))
            else:
                result.append(char)  # Non-alphabetical characters remain unchanged
        self.state = ''.join(result)
        return self

    @ChepyDecorators.call_stack
    def rot_47(self, rotation: int = 47) -> EncryptionEncodingT:
        """ROT 47 encoding

        A slightly more complex variation of a caesar cipher, which includes
        ASCII characters from 33 '!' to 126 '~'. Default rotation: 47.

        Args:
            rotation (int, optional): Amount to rotate by. Defaults to 14.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some").rot_47().out
            b"D@>6"
        """
        decoded_string = ""
        for char in self._convert_to_str():
            if ord(char) >= 33 and ord(char) <= 126:
                decoded_char = chr((ord(char) - 33 + rotation) % 94 + 33)
                decoded_string += decoded_char
            else:
                decoded_string += char  # pragma: no cover
        self.state = decoded_string.encode()
        return self

    @ChepyDecorators.call_stack
    def rot_47_bruteforce(self) -> EncryptionEncodingT:
        """ROT 47 bruteforce

        Returns:
            Chepy: The Chepy object.
        """
        hold = {}
        data = self._convert_to_str()
        for r in range(1, 94):
            decoded_string = ""
            for char in data:
                if ord(char) >= 33 and ord(char) <= 126:
                    decoded_char = chr((ord(char) - 33 + r) % 94 + 33)
                    decoded_string += decoded_char
                else:
                    decoded_string += char  # pragma: no cover
            hold[str(r)] = decoded_string.encode()
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def rot_8000(self):
        """Rot8000

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_str()
        valid_code_points = {
            33: True,
            127: False,
            161: True,
            5760: False,
            5761: True,
            8192: False,
            8203: True,
            8232: False,
            8234: True,
            8239: False,
            8240: True,
            8287: False,
            8288: True,
            12288: False,
            12289: True,
            55296: False,
            57344: True,
        }

        BMP_SIZE = 0x10000

        rotlist = {}  # the mapping of char to rotated char
        hiddenblocks = []
        startblock = 0

        for key, value in valid_code_points.items():
            if value:
                hiddenblocks.append({"start": startblock, "end": key - 1})
            else:
                startblock = key

        validintlist = []  # list of all valid chars
        currvalid = False

        for i in range(BMP_SIZE):
            if i in valid_code_points:
                currvalid = valid_code_points[i]
            if currvalid:
                validintlist.append(i)

        rotatenum = len(validintlist) // 2

        # go through every valid char and find its match
        for i in range(len(validintlist)):
            rotlist[chr(validintlist[i])] = chr(
                validintlist[(i + rotatenum) % (rotatenum * 2)]
            )

        outstring = ""

        for char in data:
            # if it is not in the mappings list, just add it directly (no rotation)
            if char not in rotlist:
                outstring += char  # pragma: no cover
                continue  # pragma: no cover

            # otherwise, rotate it and add it to the string
            outstring += rotlist[char]

        self.state = outstring.encode()
        return self

    @ChepyDecorators.call_stack
    def xor(
        self,
        key: str,
        key_type: Literal["hex", "utf", "base64", "decimal"] = "hex",
    ) -> EncryptionEncodingT:
        """XOR state with a key

        Args:
            key (str): Required. The key to xor by
            key_type (str, optional): The key type. Valid values are hex, utf, decimal and base64. Defaults to "hex".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("secret").xor(key="secret", key_type="utf").to_hex()
            000000000000
        """

        x = bytearray(b"")
        # check if state is a list and keys are list
        if isinstance(self.state, bytearray) and isinstance(key, bytearray):
            for char, key_val in zip(self.state, itertools.cycle(key)):
                x.append(char ^ key_val)

        else:
            if key_type == "utf":
                key = str(key)
                key = binascii.hexlify(key.encode())
            elif key_type == "base64":
                key = binascii.hexlify(base64.b64decode(key.encode()))
            elif key_type == "decimal":
                key = binascii.hexlify(
                    int(key).to_bytes(len(str(key)), byteorder="big")
                )

            key = binascii.unhexlify(key)
            for char, key_val in zip(self._convert_to_bytes(), itertools.cycle(key)):
                x.append(char ^ key_val)

        self.state = bytes(x)
        return self

    @ChepyDecorators.call_stack
    def xor_bruteforce(
        self, length: int = 100, crib: Union[bytes, str, None] = None
    ) -> EncryptionEncodingT:
        """Brute force single byte xor

        For multibyte xor bruteforce, use chepy.extras.crypto_extras.xor_bruteforce_multi
        function

        Args:
            length (int, optional): How to bytes to bruteforce. Defaults to 100.
            crib (Union[bytes, str, None], optional): Check for crib in xored value. Defaults to None.

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
        crib = self._str_to_bytes(crib)
        original = self.state
        found = {}
        keys = hex_chars()
        self.state = original[:length]
        for key in keys:
            self.xor(key)
            if crib is not None:
                if crib in self.state:
                    found[key] = self.state
            else:
                found[key] = self.state
            self.state = original[:length]
        self.state = found
        return self

    @ChepyDecorators.call_stack
    def jwt_decode(self) -> EncryptionEncodingT:
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
    def jwt_verify(
        self, secret: str, algorithm: list = ["HS256"]
    ) -> EncryptionEncodingT:
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
    def jwt_sign(self, secret: str, algorithms: str = "HS256") -> EncryptionEncodingT:
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
            data = json.loads(self.state)
        self.state = jwt.encode(data, key=secret, algorithm=algorithms)
        return self

    @ChepyDecorators.call_stack
    def jwt_token_generate_none_alg(
        self, headers: Dict[str, Any] = {}
    ) -> EncryptionEncodingT:
        """Generate a jwt token with none algorithm

        Args:
            headers (Dict[str, Any], optional): Headers. `alg` key will be overwritten. Defaults to {}.

        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, dict), "State should be a dictionary"
        headers["alg"] = "none"
        encoded_headers = base64.b64encode(json.dumps(headers).encode()).replace(
            b"=", b""
        )
        encoded_payload = base64.b64encode(json.dumps(self.state).encode()).replace(
            b"=", b""
        )
        self.state = encoded_headers + b"." + encoded_payload + b"."
        return self

    @ChepyDecorators.call_stack
    def jwt_token_generate_embedded_jwk(
        self,
        private_key_pem: str,
        private_key_passphrase: str = None,
        headers: dict = {},
        alg: str = "RS256",
    ) -> EncryptionEncodingT:
        """Generate a JWT token with an embedded JWK

        Args:
            private_key_pem (str): Private key to sign token
            private_key_passphrase (str, optional): Private key passphrase. Defaults to None.
            headers (dict, optional): Token headers. Defaults to {}.
            alg (str, optional): Token algorithm. Defaults to "RS256".

        Returns:
            Chepy: The Chepy object.
        """
        payload = self.state
        assert isinstance(payload, dict), "State should be a dictionary"
        private_key = RSA.import_key(private_key_pem, private_key_passphrase)

        n = private_key.n
        e = private_key.e

        jwk_header = {
            "kty": "RSA",
            "e": base64.urlsafe_b64encode(e.to_bytes((e.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("="),
            "n": base64.urlsafe_b64encode(n.to_bytes((n.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("="),
        }
        if headers.get("kid"):
            jwk_header["kid"] = headers.get("kid")
        headers["jwk"] = jwk_header
        headers["alg"] = alg

        encoded_header = (
            base64.urlsafe_b64encode(bytes(json.dumps(headers), "utf-8"))
            .decode("utf-8")
            .rstrip("=")
        )
        encoded_payload = (
            base64.urlsafe_b64encode(bytes(json.dumps(payload), "utf-8"))
            .decode("utf-8")
            .rstrip("=")
        )

        signature_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
        hashed_input = Hash.SHA256.new(signature_input)
        signature = PKCS1_15.new(private_key).sign(hashed_input)

        token = f"{encoded_header}.{encoded_payload}.{base64.urlsafe_b64encode(signature).decode('utf-8').replace('=', '')}"

        self.state = token
        return self

    @ChepyDecorators.call_stack
    def rc4_encrypt(self, key: str, key_format: str = "hex") -> EncryptionEncodingT:
        """Encrypt raw state with RC4

        Args:
            key (str): Required. Secret key
            key_format (str, optional): Key format. Defaults to "hex".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").rc4_encrypt("736563726574").o
            b"9e59bf79a2c0b7d253"
        """
        if isinstance(key, str):
            key = key.encode()
        if key_format == "hex":
            key = binascii.unhexlify(key)
        elif key_format == "base64":
            key = base64.b64decode(key)
        elif key_format == "utf-16-le":
            key = key.decode().encode("utf-16-le")
        elif key_format == "utf-16-be":
            key = key.decode().encode("utf-16-be")
        cipher = ARC4.new(key)
        self.state = binascii.hexlify(cipher.encrypt(self._convert_to_bytes()))
        return self

    @ChepyDecorators.call_stack
    def rc4_decrypt(self, key: str, key_format: str = "hex") -> EncryptionEncodingT:
        """Decrypt raw state with RC4

        Args:
            key (str): Required. Secret key
            key_format (str, optional): Key format. Defaults to "hex".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("9e59bf79a2c0b7d253").hex_to_str().rc4_decrypt("secret").o
            b"some data"
        """
        if isinstance(key, str):
            key = key.encode()
        if key_format == "hex":
            key = binascii.unhexlify(key)
        elif key_format == "base64":
            key = base64.b64decode(key)
        elif key_format == "utf-16-le":
            key = key.decode().encode("utf-16-le")
        elif key_format == "utf-16-be":
            key = key.decode().encode("utf-16-be")
        cipher = ARC4.new(key)
        self.state = cipher.decrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def des_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with DES

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").des_encrypt("70617373776f7264").o
            b"1ee5cb52954b211d1acd6e79c598baac"

            To encrypt using a different mode

            >>> Chepy("some data").des_encrypt("password", mode="CTR").o
            b"0b7399049b0267d93d"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES.new(key, mode=DES.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = DES.new(key, mode=DES.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
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
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with DES.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("1ee5cb52954b211d1acd6e79c598baac").hex_to_str().des_decrypt("password").o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES.new(key, mode=DES.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = DES.new(key, mode=DES.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
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
    def chacha_encrypt(
        self,
        key: str,
        nonce: str = "0000000000000000",
        key_format: str = "hex",
        nonce_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with ChaCha 20 rounds

        Args:
            key (str): Required. The secret key
            nonce (str, optional): Nonce. Defaults to '0000000000000000'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            nonce_format (str, optional): Format of nonce. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.
        """

        key, nonce = self._convert_key(key, nonce, key_format, nonce_format)

        cipher = ChaCha20.new(key=key, nonce=nonce)
        self.state = cipher.encrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def chacha_decrypt(
        self,
        key: str,
        nonce: str = "0000000000000000",
        key_format: str = "hex",
        nonce_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with ChaCha 20 rounds.

        Args:
            key (str): Required. The secret key
            nonce (str, optional): nonce for certain modes only. Defaults to '0000000000000000'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            nonce_format (str, optional): Format of nonce. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.
        """

        key, nonce = self._convert_key(key, nonce, key_format, nonce_format)

        cipher = ChaCha20.new(key=key, nonce=nonce)
        self.state = cipher.decrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def triple_des_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with Triple DES

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").triple_des_encrypt("super secret password !!", mode="ECB").o
            b"f8b27a0d8c837edc8fb00ea85f502fb4"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES3.new(key, mode=DES3.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = DES3.new(key, mode=DES3.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
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
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with DES.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("f8b27a0d8c837edce87dd13a1ab41f96")
            >>> c.hex_to_str()
            >>> c.triple_des_decrypt("super secret password !!")
            >>> c.o
            b"some data"
        """

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES3.new(key, mode=DES3.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CBC/NoPadding":
            cipher = DES3.new(key, mode=DES3.MODE_CBC, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "ECB":
            cipher = DES3.new(key, mode=DES3.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB/NoPadding":
            cipher = DES3.new(key, mode=DES3.MODE_ECB)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "CTR":
            cipher = DES3.new(key, mode=DES3.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES3.new(key, mode=DES3.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        else:  # pragma: no cover
            raise ValueError("Invalid mode")

    @ChepyDecorators.call_stack
    def aes_encrypt(
        self,
        key: str,
        iv: str = "00000000000000000000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with AES.
        CFB mode reflects Cyberchef and not native python behaviour.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only.
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").aes_encrypt("secret password!", mode="ECB").o
            b"5fb8c186394fc399849b89d3b6605fa3"
        """

        assert mode in ["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"], "Not a valid mode."

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 16))
            return self
        elif mode == "CFB":
            cipher = AES.new(key, mode=AES.MODE_CFB, iv=iv, segment_size=128)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "ECB":
            cipher = AES.new(key, mode=AES.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 16))
            return self
        elif mode == "CTR":
            counter = Counter.new(128, initial_value=int.from_bytes(iv, "big"))
            cipher = AES.new(key, mode=AES.MODE_CTR, counter=counter)
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
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with AES.
        CFB mode reflects Cyberchef and not native python behaviour.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only.
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("5fb8c186394fc399849b89d3b6605fa3")
            >>> c.hex_to_str()
            >>> c.aes_decrypt("7365637265742070617373776f726421")
            >>> c.o
            b"some data"
        """

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 16)
            return self
        elif mode == "CBC/NoPadding":
            cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "CFB":
            cipher = AES.new(key, mode=AES.MODE_CFB, iv=iv, segment_size=128)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "ECB":
            cipher = AES.new(key, mode=AES.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 16)
            return self
        elif mode == "ECB/NoPadding":
            cipher = AES.new(key, mode=AES.MODE_ECB)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "CTR":
            counter = Counter.new(128, initial_value=int.from_bytes(iv, "big"))
            cipher = AES.new(key, mode=AES.MODE_CTR, counter=counter)
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
        else:  # pragma: no cover
            raise ValueError("Invalid AES mode")

    @ChepyDecorators.call_stack
    def blowfish_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with Blowfish

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").blowfish_encrypt("password", mode="ECB").o
            b"d9b0a79853f139603951bff96c3d0dd5"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
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
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with Blowfish

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only.
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("d9b0a79853f13960fcee3cae16e27884")
            >>> c.hex_to_str()
            >>> c.blowfish_decrypt("password", key_format="utf-8")
            >>> c.o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
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
    def vigenere_encode(self, key: str) -> EncryptionEncodingT:
        """Vigenere encode

        Args:
            key (str): Key

        Raises:
            ValueError: Key is not alpha
            ValueError: Key is not provided

        Returns:
            Chepy: The Chepy object.
        """
        input_str = self._convert_to_str()
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        key = key.lower()
        output = ""
        fail = 0

        if not key:
            raise ValueError("No key entered")  # pragma: no cover
        if not key.isalpha():
            raise ValueError("The key must consist only of letters")  # pragma: no cover

        for i in range(len(input_str)):
            if input_str[i].isalpha():
                is_upper = input_str[i].isupper()
                input_char = input_str[i].lower()
                key_char = key[(i - fail) % len(key)]
                key_index = alphabet.index(key_char)
                input_index = alphabet.index(input_char)
                encoded_index = (key_index + input_index) % 26
                encoded_char = alphabet[encoded_index]
                output += encoded_char.upper() if is_upper else encoded_char
            else:
                output += input_str[i]
                fail += 1

        self.state = output
        return self

    @ChepyDecorators.call_stack
    def vigenere_decode(self, key: str) -> EncryptionEncodingT:
        """Vigenere decode

        Args:
            key (str): Key

        Raises:
            ValueError: Key is not alpha
            ValueError: Key is not provided

        Returns:
            Chepy: The Chepy object.
        """
        input_str = self._convert_to_str()
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        output = ""
        fail = 0
        key = key.lower()

        if not key:
            raise ValueError("No key entered")  # pragma: no cover
        if not key.isalpha():
            raise ValueError("The key must consist only of letters")  # pragma: no cover

        for i in range(len(input_str)):
            if input_str[i].isalpha():
                is_upper = input_str[i].isupper()
                input_char = input_str[i].lower()
                key_char = key[(i - fail) % len(key)]
                key_index = alphabet.index(key_char)
                input_index = alphabet.index(input_char)
                encoded_index = (input_index - key_index + len(alphabet)) % len(
                    alphabet
                )
                encoded_char = alphabet[encoded_index]
                output += encoded_char.upper() if is_upper else encoded_char
            else:
                output += input_str[i]
                fail += 1

        self.state = output
        return self

    @ChepyDecorators.call_stack
    def affine_encode(self, a: int = 1, b: int = 1) -> EncryptionEncodingT:
        """Encode with Affine cipher

        Args:
            a (int, optional): Multiplier value. Defaults to 1
            b (int, optional): Additive value. Defaults to 1

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("secret").affine_encode().o
            "TFDSFU"
        """
        self.state = pycipher.Affine(a=a, b=b).encipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def affine_decode(self, a: int = 1, b: int = 1) -> EncryptionEncodingT:
        """Decode Affine cipher

        Args:
            a (int, optional): Multiplier value. Defaults to 1
            b (int, optional): Additive value. Defaults to 1

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("TFDSFU").affine_decode().o
            "SECRET"
        """
        self.state = pycipher.Affine(a=a, b=b).decipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def atbash_encode(self) -> EncryptionEncodingT:
        """Encode with Atbash cipher

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("secret").atbash_encode().o
            "HVXIVG"
        """
        self.state = pycipher.Atbash().encipher(self._convert_to_str(), keep_punct=True)
        return self

    @ChepyDecorators.call_stack
    def atbash_decode(self) -> EncryptionEncodingT:
        """Decode Atbash cipher

        Returns:
            Chepy: The Chepy object.

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
    ) -> EncryptionEncodingT:
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
                encode += morse_code_dict.get(w.upper(), "") + letter_delim
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
    ) -> EncryptionEncodingT:
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
                chars = re.sub(word_delim, "", chars, re.I)
                if morse_code_dict.get(chars) is not None:
                    decode += " " + morse_code_dict.get(chars, "")
                else:  # pragma: no cover
                    decode += " " + chars
            else:
                decode += morse_code_dict.get(chars, "")
        self.state = decode
        return self

    @ChepyDecorators.call_stack
    def rsa_encrypt(
        self,
        public_key: str,
        is_file: bool = True,
        passphrase: str = None,
        cipher: Literal["OAEP", "PKCS"] = "OAEP",
    ) -> EncryptionEncodingT:
        """Encrypt data with RSA Public key in PEM format

        Args:
            public_key (str): Path to Public key
            is_file (bool): If supplied argument is a PEM file path. Defaults to false
            passphrase (str): passphrase. Defaults to None
            cipher (str): Cipher type. Defaults to OAEP

        Returns:
            Chepy: The Chepy object
        """
        rsa = self._rsa_process_key(public_key, is_file, passphrase)
        c = self._rsa_cipher(cipher, rsa)
        self.state = c.encrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def rsa_decrypt(
        self,
        private_key: str,
        is_file: bool = True,
        passphrase: str = None,
        cipher: Literal["OAEP", "PKCS"] = "OAEP",
    ) -> EncryptionEncodingT:
        """Decrypt data with RSA Private key in PEM format

        Args:
            private_key (str): Path to Private key
            is_file (bool): If supplied argument is a PEM file path. Defaults to false
            passphrase (str): passphrase. Defaults to None
            cipher (str): Cipher type. Defaults to OAEP

        Returns:
            Chepy: The Chepy object
        """
        rsa = self._rsa_process_key(private_key, is_file, passphrase)
        c = self._rsa_cipher(cipher, rsa)
        if cipher == "PKCS":
            self.state = c.decrypt(self._convert_to_bytes(), None)
        else:
            self.state = c.decrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def rsa_sign(
        self,
        private_key: str,
        is_file: bool = True,
        passphrase: str = None,
        hash_format: Literal["SHA256", "SHA512", "SHA1", "MD5", "SHA384"] = "SHA256",
    ) -> EncryptionEncodingT:
        """Sign data in state with RSA Private key in PEM format

        Args:
            private_key (str): Private key
            is_file (bool): If supplied argument is a PEM file path. Defaults to false
            passphrase (str): passphrase. Defaults to None
            hash_format (str): hash type. Defaults to SHA256

        Returns:
            Chepy: The Chepy object
        """
        rsa = self._rsa_process_key(private_key, is_file, passphrase)
        h = getattr(Hash, hash_format).new(self._convert_to_bytes())
        self.state = PKCS1_15.new(rsa).sign(h)
        return self

    @ChepyDecorators.call_stack
    def rsa_verify(
        self,
        signature: bytes,
        public_key: str,
        is_file: bool = True,
        passphrase: str = None,
        hash_format: Literal["SHA256", "SHA512", "SHA1", "MD5", "SHA384"] = "SHA256",
    ) -> EncryptionEncodingT:  # pragma: no cover
        """Verify data in state with RSA Public key in PEM format

        Args:
            signature (bytes): The signature as bytes
            public_key (str): Path to Private key
            is_file (bool): If supplied argument is a PEM file path. Defaults to false
            passphrase (str): passphrase. Defaults to None
            hash_format (str): Cipher type. Defaults to SHA256

        Returns:
            Chepy: The Chepy object
        """
        rsa = self._rsa_process_key(public_key, is_file, passphrase)
        h = getattr(Hash, hash_format).new(self._convert_to_bytes())
        self.state = PKCS1_15.new(rsa).verify(h, signature)
        return self

    @ChepyDecorators.call_stack
    def rsa_private_pem_to_jwk(self) -> EncryptionEncodingT:
        """Convert RSA PEM private key to jwk format

        Returns:
            Chepy: The Chepy object.
        """
        # Load the PEM private key
        private_key = RSA.import_key(self._convert_to_str())

        n = private_key.n
        e = private_key.e
        d = private_key.d
        p = private_key.p
        q = private_key.q
        dp = private_key.d % (p - 1)
        dq = private_key.d % (q - 1)
        qi = pow(q, -1, p)

        n_base64url = (
            base64.urlsafe_b64encode(n.to_bytes((n.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        e_base64url = (
            base64.urlsafe_b64encode(e.to_bytes((e.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        d_base64url = (
            base64.urlsafe_b64encode(d.to_bytes((d.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        p_base64url = (
            base64.urlsafe_b64encode(p.to_bytes((p.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        q_base64url = (
            base64.urlsafe_b64encode(q.to_bytes((q.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        dp_base64url = (
            base64.urlsafe_b64encode(dp.to_bytes((dp.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        dq_base64url = (
            base64.urlsafe_b64encode(dq.to_bytes((dq.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        qi_base64url = (
            base64.urlsafe_b64encode(qi.to_bytes((qi.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )

        private = {
            "p": p_base64url,
            "kty": "RSA",
            "q": q_base64url,
            "d": d_base64url,
            "e": e_base64url,
            "qi": qi_base64url,
            "dp": dp_base64url,
            "dq": dq_base64url,
            "n": n_base64url,
        }

        public = {"kty": "RSA", "e": e_base64url, "n": n_base64url}
        self.state = {"private": private, "public": public}
        return self

    @ChepyDecorators.call_stack
    def rsa_public_key_from_jwk(self) -> EncryptionEncodingT:
        """Generate RSA public key in PEM format from JWK

        Raises:
            AssertionError: If n or e not found

        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, dict), "State should be a dict"
        jwk_key = self.state
        if not "e" in jwk_key or "n" not in jwk_key:
            raise AssertionError("e or n not found")  # pragma: no cover
        e = int.from_bytes(base64.urlsafe_b64decode(jwk_key["e"] + "=="), "big")
        n = int.from_bytes(base64.urlsafe_b64decode(jwk_key["n"] + "=="), "big")

        public_key = RSA.construct((n, e))

        self.state = public_key.export_key().decode("utf-8")
        return self

    @ChepyDecorators.call_stack
    def monoalphabetic_substitution(
        self, mapping: Dict[str, str] = {}
    ) -> EncryptionEncodingT:
        """Monoalphabetic substitution. Re-map characters

        Args:
            mapping (Dict[str, str], optional): Mapping of characters where key is the character to map and value is the new character to replace with. Defaults to {}.

        Returns:
            Chepy: The Chepy object
        """
        hold = ""
        cipher = self._convert_to_str()
        for c in cipher:
            hold += mapping.get(c.lower(), c)
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def to_letter_number_code(
        self, join_by: Union[str, bytes] = b" "
    ) -> EncryptionEncodingT:
        """Encode to A1Z26

        Args:
            join_by (Union[str, bytes], optional): join output by. Defaults to b' '.

        Returns:
            Chepy: The Chepy object.
        """
        join_by = self._str_to_bytes(join_by)
        data = list(self._convert_to_str())
        hold = []
        for i, d in enumerate(data):
            hold.append(f"{d}{i}".encode())
        random.shuffle(hold)
        self.state = join_by.join(hold)
        return self

    @ChepyDecorators.call_stack
    def from_letter_number_code(
        self, delimiter: Union[str, bytes] = " ", join_by: Union[str, bytes] = ""
    ) -> EncryptionEncodingT:
        """Decode A1Z26

        Args:
            delimiter (Union[str, bytes], optional): Split on. Defaults to ' '.
            join_by (Union[str, bytes], optional): Join output by. Defaults to ''.

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_str()
        delimiter = detect_delimiter(data, default_delimiter=delimiter)
        data = data.split(delimiter)
        hold = ["§" for _ in range(len(data))]
        for d in data:
            try:
                hold[int(d[1:])] = d[0]
            except:  # pragma: no cover
                continue
        self.state = join_by.join(hold).encode()
        return self

    @ChepyDecorators.call_stack
    def ls47_encrypt(
        self, password: str, padding: int = 10, signature: str = ""
    ) -> EncryptionEncodingT:
        """LS47 encrypt

        Args:
            password (str): password
            padding (int, optional): Padding. Defaults to 10.
            signature (str, optional): Signature to prepend. Defaults to ''.

        Returns:
            Chepy: The Chepy object.
        """
        key = _derive_key(password)
        self.state = _ls47_enc(
            key, self._convert_to_str(), padding_size=padding, signature=signature
        )
        return self

    @ChepyDecorators.call_stack
    def ls47_decrypt(self, password: str, padding: int = 10) -> EncryptionEncodingT:
        """LS47 decrypt

        Args:
            password (str): password
            padding (int, optional): Padding. Defaults to 10.

        Returns:
            Chepy: The Chepy object.
        """
        key = _derive_key(password)
        self.state = _ls47_dec(key, padding, self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def bifid_encode(self, key: Union[bytes, str] = "") -> EncryptionEncodingT:
        """Bifid / polybius decode

        Args:
            key (Union[str, bytes], optional): Key. Defaults to "".

        Returns:
            Chepy: The Chepy object.
        """
        key = self._bytes_to_str(key)
        key = "".join(re.findall(r"[A-Z]+", key))
        keyword_str = key.upper().replace("J", "I")
        # keyword_set = set(keyword_str)
        # keyword_list = []
        alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        x_co = []
        y_co = []
        structure = []

        output = ""
        count = 0

        polybius = Ciphers.gen_polybius_square(keyword_str)

        for letter in self._convert_to_str().replace("J", "I"):
            alp_ind = letter.upper() in alpha
            pol_ind = -1

            if alp_ind:
                for i in range(5):
                    if letter.upper() in polybius[i]:
                        pol_ind = polybius[i].index(letter.upper())
                        x_co.append(pol_ind)
                        y_co.append(i)

                if letter in alpha:
                    structure.append(True)  # pragma: no cover
                elif alp_ind:
                    structure.append(False)
            else:
                structure.append(letter)  # pragma: no cover

        trans = "".join(map(str, y_co)) + "".join(map(str, x_co))

        for pos in structure:
            if isinstance(pos, bool):
                coords = trans[2 * count : 2 * count + 2]
                coords = list(map(int, coords))

                output += (
                    polybius[coords[0]][coords[1]]
                    if pos
                    else polybius[coords[0]][coords[1]].lower()
                )
                count += 1
            else:
                output += pos  # pragma: no cover

        self.state = output
        return self

    @ChepyDecorators.call_stack
    def bifid_decode(self, key: Union[str, bytes] = ""):
        """Bifid / polybius decode

        Args:
            key (Union[str, bytes], optional): Key. Defaults to "".

        Returns:
            Chepy: The Chepy object.
        """
        key = self._bytes_to_str(key)
        key = "".join(re.findall(r"[A-Z]+", key))
        keyword_str = key.upper().replace("J", "I")
        # keyword_set = set(keyword_str)
        alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        structure = []

        output = ""
        count = 0
        trans = ""

        polybius = Ciphers.gen_polybius_square(keyword_str)

        for letter in self._convert_to_str().replace("J", "I"):
            alp_ind = letter.upper() in alpha
            pol_ind = -1

            if alp_ind:
                for i in range(5):
                    if letter.upper() in polybius[i]:
                        pol_ind = polybius[i].index(letter.upper())
                        trans += f"{i}{pol_ind}"

                if letter in alpha:
                    structure.append(True)  # pragma: no cover
                elif alp_ind:
                    structure.append(False)
            else:
                structure.append(letter)  # pragma: no cover

        for pos in structure:
            if isinstance(pos, bool):
                coords = [int(trans[count]), int(trans[count + len(trans) // 2])]

                output += (
                    polybius[coords[0]][coords[1]]
                    if pos
                    else polybius[coords[0]][coords[1]].lower()
                )
                count += 1
            else:
                output += pos  # pragma: no cover

        self.state = output
        return self

    @ChepyDecorators.call_stack
    def huffman_encode(self) -> EncryptionEncodingT:
        """Huffman encode

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_str()
        root = Ciphers.build_huffman_tree(data)
        huffman_codes = {}
        Ciphers.build_huffman_codes(root, "", huffman_codes)
        encoded_data = "".join(huffman_codes[char] for char in data)
        self.state = {"encoded": encoded_data, "codes": huffman_codes}
        return self

    @ChepyDecorators.call_stack
    def huffman_decode(self, huffman_codes: Dict[str, str]) -> EncryptionEncodingT:
        """Huffman decode

        Args:
            huffman_codes (Dict[str, str]): Huffman codes as a dict

        Returns:
            Chepy: The Chepy object.
        """
        decoded_data = ""
        current_code = ""

        encoded_data = self._convert_to_str()
        for bit in encoded_data:
            current_code += bit
            for char, code in huffman_codes.items():
                if code == current_code:
                    decoded_data += char
                    current_code = ""
                    break

        self.state = decoded_data
        return self

    @ChepyDecorators.call_stack
    def cetacean_encode(self) -> EncryptionEncodingT:
        """Cetacean encode

        Returns:
            Chepy: The Chepy object.
        """
        result = []
        charArray = list(self._convert_to_str())

        for character in charArray:
            if character == " ":
                result.append(character)
            else:
                binaryArray = format(ord(character), "016b")
                result.append(
                    "".join(["e" if bit == "1" else "E" for bit in binaryArray])
                )

        self.state = "".join(result)
        return self

    @ChepyDecorators.call_stack
    def cetacean_decode(self) -> EncryptionEncodingT:
        """Cetacean decode

        Returns:
            Chepy: The Chepy object.
        """
        binaryArray = []

        for char in self._convert_to_str():
            if char == " ":
                binaryArray.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
            else:
                binaryArray.append(1 if char == "e" else 0)

        byteArray = []

        for i in range(0, len(binaryArray), 16):
            byteArray.append("".join(map(str, binaryArray[i : i + 16])))

        self.state = "".join([chr(int(byte, 2)) for byte in byteArray])
        return self

    @ChepyDecorators.call_stack
    def rabbit(self, key: str, iv: Union[None, str] = None) -> EncryptionEncodingT:
        """Rabbit encryption/decryption

        Args:
            key (str): Key
            iv (Union[None,str], optional): IV. Defaults to None.

        Returns:
            Chepy: The Chepy object.
        """
        self.state = Rabbit(key, iv).encrypt(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def fernet_encrypt(
        self, key: Union[bytes, str], encode_key: bool = False
    ) -> EncryptionEncodingT:
        """Fernet encrypt

        Args:
            key (Union[bytes, str]): Key to encrypt with. This should be 32 bytes long
            encode_key (bool, optional): If key should be base64 encoded. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        key = self._str_to_bytes(key)
        if encode_key:
            key = base64.b64encode(key)
        out = Fernet(key).encrypt(self._convert_to_bytes())
        self.state = out
        return self

    @ChepyDecorators.call_stack
    def fernet_decrypt(
        self, key: Union[bytes, str], encode_key: bool = False
    ) -> EncryptionEncodingT:
        """Fernet decrypt

        Args:
            key (Union[bytes, str]): Key to encrypt with. This should be 32 bytes long
            encode_key (bool, optional): If key should be base64 encoded. Defaults to False.

        Returns:
            Chepy: The Chepy object.
        """
        key = self._str_to_bytes(key)
        if encode_key:
            key = base64.b64encode(key)
        out = Fernet(key).decrypt(self._convert_to_bytes())
        self.state = out
        return self

    @ChepyDecorators.call_stack
    def railfence_encode(self, key=2, offset=0) -> EncryptionEncodingT:
        """Encode to railfence

        Args:
            key (int, optional): Key. Should be equal or larger than data. Defaults to 2.
            offset (int, optional): Offset. Defaults to 0.

        Returns:
            Chepy: The Chepy object.
        """
        key, offset = int(key), int(offset)
        data = self._convert_to_str()
        if key < 2:
            raise ValueError("Key has to be bigger than 2")  # pragma: no cover
        elif key > len(data):
            raise ValueError(
                "Key should be smaller than the plain text's length"
            )  # pragma: no cover

        if offset < 0:
            raise ValueError("Offset has to be a positive integer")  # pragma: no cover

        cycle = (key - 1) * 2
        rows = [""] * key

        for pos in range(len(data)):
            row_idx = key - 1 - abs(cycle // 2 - (pos + offset) % cycle)
            rows[row_idx] += data[pos]

        self.state = "".join(rows).strip()
        return self

    @ChepyDecorators.call_stack
    def railfence_decode(self, key=2, offset=0) -> EncryptionEncodingT:
        """Decode railfence

        Args:
            key (int, optional): Key. Should be equal or larger than data. Defaults to 2.
            offset (int, optional): Offset. Defaults to 0.

        Returns:
            Chepy: The Chepy object.
        """
        key, offset = int(key), int(offset)
        cipher = self._convert_to_str()

        if key < 2:
            raise ValueError("Key has to be bigger than 2")  # pragma: no cover
        elif key > len(cipher):
            raise ValueError(
                "Key should be smaller than the cipher's length"
            )  # pragma: no cover

        if offset < 0:
            raise ValueError("Offset has to be a positive integer")  # pragma: no cover

        cycle = (key - 1) * 2
        plaintext = [""] * len(cipher)

        j = 0
        for y in range(key):
            for x in range(len(cipher)):
                if (y + x + offset) % cycle == 0 or (y - x - offset) % cycle == 0:
                    plaintext[x] = cipher[j]
                    j += 1

        self.state = "".join(plaintext).strip()
        return self
