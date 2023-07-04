import json
import lazy_import
from typing import Iterator, Dict, List, Union
from binascii import hexlify, unhexlify
from itertools import cycle
from urllib.request import urlopen
RSA = lazy_import.lazy_module("Crypto.PublicKey.RSA")

from .combinatons import generate_combo, hex_chars
from chepy import Chepy


def factordb(n: int) -> dict:  # pragma: no cover
    """Query the factordb api and get primes if available

    Args:
        n (int): n is the modulus for the public key and the private keys

    Returns:
        dict: response from api as a dictionary. None if status code is not 200
    """
    res = urlopen("http://factordb.com/api/?query={}".format(str(n)))
    if res.status != 200:
        return None
    return json.loads(res.read().decode())


def construct_private_key(
    n: int, e: int, d: int, format: str = "PEM", passphrase: str = None
) -> str:  # pragma: no cover
    """Construct a private key given n, e and d

    Args:
        n (int): n
        e (int): e
        d (int): d
        format (str, optional): Supports PEM, DER and OpenSSH. Defaults to "PEM".
        passphrase (str, optional): [description]. Defaults to None.

    Returns:
        str: Private key
    """
    valid_formats = ["PEM", "DER", "OpenSSH"]
    assert format in valid_formats, "Valid formats are {}".format(
        " ".join(valid_formats)
    )
    priv = RSA.construct((n, e, d))
    return priv.export_key(format=format, passphrase=passphrase)


def xor_bruteforce_multi(
    data: str, min: int = 0, max: int = None, errors: str = "backslashreplace"
) -> Iterator[Dict[str, str]]:
    """Bruteforce multibyte xor encryption. For faster results, use pypy3.
    It is important to set the min and max values if the key size is known.

    Args:
        data (str): XORed data
        min (int, optional): Minimum key length. Default will start at 1 byte
            . Defaults to 0.
        max (int, optional): Maximum key length. Maximum value is 257 bytes. Defaults to None.
        errors (str, optional): How should the errors be handled? Defaults to backslashreplace.
            Valid options are replace, ignore, backslashreplace

    Returns:
        Iterator[Dict[str, str]]: A dictionary where key is key, and value is xored data

    Yields:
        Iterator[Dict[str, str]]: A generator which contains a dictionary with the
            keys: `key` and `out`
    """
    for key in generate_combo(
        hex_chars(), min_length=min, max_length=max, join_by=""
    ):  # pragma: no cover
        yield {
            "key": key,
            "out": Chepy(data).xor(key).bytearray_to_str(errors=errors).o,
        }


def xor_repeating_key(
    data1: bytes, data2: bytes, min: int = 1, max: int = 257
) -> Union[bytes, None]:  # pragma: no cover
    """Recover repeating key xor keys.

    Args:
        data1 (bytes): File 1 path
        data2 (bytes): File 2 path
        min (int, optional): Min chars to test. Defaults to 1.
        max (int, optional): Max chars to test. Defaults to 257.

    Returns:
        Union[bytes, None]: Key as hex bytes or None if no key found
    """

    def find_same(s: bytes):
        i = (s + s).find(s, 1, -1)
        return None if i == -1 else s[:i]

    for i in range(min, max):
        d1 = data1[:i]

        d2 = data2[:i]

        x = bytes(a ^ b for a, b in zip(d1, d2))
        o = find_same(x)
        if o is not None:
            return o


def xor(data: bytes, key: bytes) -> bytes:  # pragma: no cover
    """XOR data with a hex key

    Args:
        data (bytes): Data to be xored
        key (bytes): Hex key to xor data with

    Returns:
        bytes: XORed data

    Example:
        >>> xor(b"hello", unhexlify(b"aabbccdd"))
        b'c2dea0b1c5'
    """
    return hexlify(bytes(a ^ b for a, b in zip(data, cycle(key))))


def one_time_pad_crib(
    cipherText1: Union[bytes, str], cipherText2: Union[bytes, str], crib: bytes
) -> List[str]:
    """One time pad crib attack.

    Args:
        cipherText1 (Union[bytes, str]): Cipher text 1 as hex
        cipherText2 (Union[bytes, str]): Cipher text 2 as hex
        crib (bytes): Crib (known text) as bytes

    Returns:
        List[str]: List of possible plaintexts
    """
    cipherText1 = unhexlify(cipherText1)
    cipherText2 = unhexlify(cipherText2)
    xored = bytearray(a ^ b for a, b in zip(cipherText1, cipherText2))
    hold = []
    for offset in range(0, len(xored) - len(crib) + 1):
        piece = xored[offset : offset + len(crib)]
        piece = bytearray(a ^ b for a, b in zip(crib, piece))
        if all(32 <= c <= 126 for c in piece):
            piece = (
                ("." * offset)
                + piece.decode()
                + ("." * (len(xored) - len(crib) - offset))
            )
            hold.append(piece)
    return hold


def generate_rsa_keypair(
    bits: int = 1024, passphrase: str = None
) -> Dict[str, dict]:  # pragma: no cover
    """Generates an RSA keypair with the specified number of bits.

    Args:
      bits: The number of bits for the RSA keypair.

    Returns:
      A tuple of the RSA public key and RSA private key, both in PEM format.
    """

    keypair = RSA.generate(bits)
    return {
        "pem": {
            "public": keypair.publickey().exportKey("PEM"),
            "private": keypair.exportKey("PEM", passphrase=passphrase),
        },
        "der": {
            "public": keypair.publickey().exportKey("DER"),
            "private": keypair.exportKey("DER", passphrase=passphrase),
        },
    }
