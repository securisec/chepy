import ujson
from typing import Iterator, Dict
from urllib.request import urlopen
from Crypto.PublicKey import RSA

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
    return ujson.loads(res.read().decode())


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
