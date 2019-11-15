import json
from urllib.request import urlopen
from Crypto.PublicKey import RSA


def factordb(n: int) -> dict:
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
) -> str:
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
