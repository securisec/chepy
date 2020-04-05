import binascii
import hmac
import hashlib
import hashid
from typing import Union
from typing_extensions import Literal
from Crypto.Hash import MD2, MD4, MD5, SHA512, SHA1, SHA256
from Crypto.Hash import keccak
from Crypto.Hash import SHAKE128, SHAKE256
from Crypto.Hash import RIPEMD
from Crypto.Hash import BLAKE2b, BLAKE2s
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Protocol.KDF import bcrypt as _crypto_bcrypt
from Crypto.Protocol.KDF import bcrypt_check as _crypto_bcrypt_check
from Crypto.Protocol.KDF import scrypt as _crypto_scrypt
from crccheck.crc import CrcArc, Crc32, Crc8

from ..core import ChepyCore, ChepyDecorators


class Hashing(ChepyCore):
    @ChepyDecorators.call_stack
    def identify_hash(self):
        """Identify hash type
        
        Tries to determine information about a given hash and suggests which 
        algorithm may have been used to generate it based on its length. 
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("6dcd4ce23d88e2ee9568ba546c007c63d9131c1b").identify_hash().o
            [
                {'hashcat': 100, 'john': 'raw-sha1', 'name': 'SHA-1'},
                {'hashcat': 4500, 'john': None, 'name': 'Double SHA-1'},
                {'hashcat': 6000, 'john': 'ripemd-160', 'name': 'RIPEMD-160'},
                {'hashcat': None, 'john': None, 'name': 'Haval-160'},
                ...
            ]
        """
        hashes = []
        for h in hashid.HashID().identifyHash(self._convert_to_str()):
            hashes.append({"name": h.name, "hashcat": h.hashcat, "john": h.john})
        self.state = hashes
        return self

    @ChepyDecorators.call_stack
    def sha1(self):
        """Get SHA1 hash
        
        The SHA (Secure Hash Algorithm) hash functions were designed by the NSA. 
        SHA-1 is the most established of the existing SHA hash functions and it is 
        used in a variety of security applications and protocols. However, SHA-1's 
        collision resistance has been weakening as new attacks are discovered or improved.

        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("A").sha1().output
            "6dcd4ce23d88e2ee9568ba546c007c63d9131c1b"
        """
        self.state = hashlib.sha1(self._convert_to_bytes()).hexdigest()
        return self

    @ChepyDecorators.call_stack
    def sha2_256(self):
        """Get SHA2-256 hash
        
        The SHA-2 (Secure Hash Algorithm 2) hash functions were designed by the NSA. SHA-2 
        includes significant changes from its predecessor, SHA-1. The SHA-2 family consists of 
        hash functions with digests (hash values) that are 224, 256, 384 or 512 bits: SHA224, 
        SHA256, SHA384, SHA512. SHA-512 operates on 64-bit words. SHA-256 operates on 32-bit 
        words. SHA-384 is largely identical to SHA-512 but is truncated to 384 bytes. SHA-224 
        is largely identical to SHA-256 but is truncated to 224 bytes. SHA-512/224 and SHA-512/256 
        are truncated versions of SHA-512, but the initial values are generated using the method 
        described in Federal Information Processing Standards (FIPS) PUB 180-4.

        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("A").sha2_256().output
            "559aead08264d5795d3909718cdd05abd49572e84fe55590eef31a88a08fdffd"
        """
        self.state = hashlib.sha256(self._convert_to_bytes()).hexdigest()
        return self

    @ChepyDecorators.call_stack
    def sha2_512(self):
        """Get SHA2-512 hash
        
        The SHA-2 (Secure Hash Algorithm 2) hash functions were designed by the NSA. SHA-2 
        includes significant changes from its predecessor, SHA-1. The SHA-2 family consists of 
        hash functions with digests (hash values) that are 224, 256, 384 or 512 bits: SHA224, 
        SHA256, SHA384, SHA512. SHA-512 operates on 64-bit words. SHA-256 operates on 32-bit 
        words. SHA-384 is largely identical to SHA-512 but is truncated to 384 bytes. SHA-224 
        is largely identical to SHA-256 but is truncated to 224 bytes. SHA-512/224 and SHA-512/256 
        are truncated versions of SHA-512, but the initial values are generated using the method 
        described in Federal Information Processing Standards (FIPS) PUB 180-4.

        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("A").sha2_512().out()
            21b4f4bd9e64ed355c3eb676a28ebedaf6d8f17bdc365995b319097153044080516bd083bfcce66121a3072646994c8430cc382b8dc543e84880183bf856cff5
        """
        self.state = hashlib.sha512(self._convert_to_bytes()).hexdigest()
        return self

    @ChepyDecorators.call_stack
    def sha2_512_truncate(self, truncate: int = 256):
        """Get SHA2-512/bits hash
        
        The SHA-2 (Secure Hash Algorithm 2) hash functions were designed by the NSA. SHA-2 
        includes significant changes from its predecessor, SHA-1. The SHA-2 family consists of 
        hash functions with digests (hash values) that are 224, 256, 384 or 512 bits: SHA224, 
        SHA256, SHA384, SHA512. SHA-512 operates on 64-bit words. SHA-256 operates on 32-bit 
        words. SHA-384 is largely identical to SHA-512 but is truncated to 384 bytes. SHA-224 
        is largely identical to SHA-256 but is truncated to 224 bytes. SHA-512/224 and SHA-512/256 
        are truncated versions of SHA-512, but the initial values are generated using the method 
        described in Federal Information Processing Standards (FIPS) PUB 180-4.

        Args:
            truncate (int, optional): The bits to truncate by. Defaults to 256

        Returns:
            Chepy: The Chepy object. 
        """
        assert truncate in [256, 224], "Valid truncates are 256, 224"
        h = SHA512.new(self._convert_to_bytes(), truncate=str(truncate))
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def sha2_384(self):
        """Get SHA2-384 hash
        
        The SHA-2 (Secure Hash Algorithm 2) hash functions were designed by the NSA. SHA-2 
        includes significant changes from its predecessor, SHA-1. The SHA-2 family consists of 
        hash functions with digests (hash values) that are 224, 256, 384 or 512 bits: SHA224, 
        SHA256, SHA384, SHA512. SHA-512 operates on 64-bit words. SHA-256 operates on 32-bit 
        words. SHA-384 is largely identical to SHA-512 but is truncated to 384 bytes. SHA-224 
        is largely identical to SHA-256 but is truncated to 224 bytes. SHA-512/224 and SHA-512/256 
        are truncated versions of SHA-512, but the initial values are generated using the method 
        described in Federal Information Processing Standards (FIPS) PUB 180-4.

        Returns:
            Chepy: The Chepy object. 
        """
        self.state = hashlib.sha384(self._convert_to_bytes()).hexdigest()
        return self

    @ChepyDecorators.call_stack
    def sha2_224(self):
        """Get SHA2-224 hash
        
        The SHA-2 (Secure Hash Algorithm 2) hash functions were designed by the NSA. SHA-2 
        includes significant changes from its predecessor, SHA-1. The SHA-2 family consists of 
        hash functions with digests (hash values) that are 224, 256, 384 or 512 bits: SHA224, 
        SHA256, SHA384, SHA512. SHA-512 operates on 64-bit words. SHA-256 operates on 32-bit 
        words. SHA-384 is largely identical to SHA-512 but is truncated to 384 bytes. SHA-224 
        is largely identical to SHA-256 but is truncated to 224 bytes. SHA-512/224 and SHA-512/256 
        are truncated versions of SHA-512, but the initial values are generated using the method 
        described in Federal Information Processing Standards (FIPS) PUB 180-4.

        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("A").sha2_224().out()
            "5cfe2cddbb9940fb4d8505e25ea77e763a0077693dbb01b1a6aa94f2"
        """
        self.state = hashlib.sha224(self._convert_to_bytes()).hexdigest()
        return self

    @ChepyDecorators.call_stack
    def sha3_512(self):
        """Get SHA3-512 hash
        
        The SHA-3 (Secure Hash Algorithm 3) hash functions were released by NIST on August 5, 2015. 
        Although part of the same series of standards, SHA-3 is internally quite different from the 
        MD5-like structure of SHA-1 and SHA-2.<br><br>SHA-3 is a subset of the broader cryptographic 
        primitive family Keccak designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche, 
        building upon RadioGatún.

        Returns:
            Chepy: The Chepy object. 
        """
        self.state = hashlib.sha3_512(self._convert_to_bytes()).hexdigest()
        return self

    @ChepyDecorators.call_stack
    def sha3_256(self):
        """Get SHA3-256 hash
        
        The SHA-3 (Secure Hash Algorithm 3) hash functions were released by NIST on August 5, 2015. 
        Although part of the same series of standards, SHA-3 is internally quite different from the 
        MD5-like structure of SHA-1 and SHA-2.<br><br>SHA-3 is a subset of the broader cryptographic 
        primitive family Keccak designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche, 
        building upon RadioGatún.

        Returns:
            Chepy: The Chepy object. 
        """
        self.state = hashlib.sha3_256(self._convert_to_bytes()).hexdigest()
        return self

    @ChepyDecorators.call_stack
    def sha3_384(self):
        """Get SHA3-384 hash
        
        The SHA-3 (Secure Hash Algorithm 3) hash functions were released by NIST on August 5, 2015. 
        Although part of the same series of standards, SHA-3 is internally quite different from the 
        MD5-like structure of SHA-1 and SHA-2.<br><br>SHA-3 is a subset of the broader cryptographic 
        primitive family Keccak designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche, 
        building upon RadioGatún.

        Returns:
            Chepy: The Chepy object. 
        """
        self.state = hashlib.sha3_384(self._convert_to_bytes()).hexdigest()
        return self

    @ChepyDecorators.call_stack
    def sha3_224(self):
        """Get SHA2-224 hash
        
        The SHA-3 (Secure Hash Algorithm 3) hash functions were released by NIST on August 5, 2015. 
        Although part of the same series of standards, SHA-3 is internally quite different from the 
        MD5-like structure of SHA-1 and SHA-2.<br><br>SHA-3 is a subset of the broader cryptographic 
        primitive family Keccak designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche, 
        building upon RadioGatún.

        Returns:
            Chepy: The Chepy object. 
        """
        self.state = hashlib.sha3_224(self._convert_to_bytes()).hexdigest()
        return self

    @ChepyDecorators.call_stack
    def md2(self):
        """Get MD2 hash
        
        The MD2 (Message-Digest 2) algorithm is a cryptographic hash function developed by 
        Ronald Rivest in 1989. The algorithm is optimized for 8-bit computers.Although MD2 is 
        no longer considered secure, even as of 2014, it remains in use in public key 
        infrastructures as part of certificates generated with MD2 and RSA.

        Returns:
            Chepy: The Chepy object. 
        """
        h = MD2.new()
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def md4(self):
        """Get MD4 hash
        
        The MD4 (Message-Digest 4) algorithm is a cryptographic hash function 
        developed by Ronald Rivest in 1990. The digest length is 128 bits. The algorithm 
        has influenced later designs, such as the MD5, SHA-1 and RIPEMD algorithms.

        Returns:
            Chepy: The Chepy object. 
        """
        h = MD4.new()
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def md5(self):
        """Get MD5 hash
        
        MD5 (Message-Digest 5) is a widely used hash function. It has been used 
        in a variety of security applications and is also commonly used to check 
        the integrity of files.<br><br>However, MD5 is not collision resistant and 
        it isn't suitable for applications like SSL/TLS certificates or digital 
        signatures that rely on this property.

        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("A").md5().output
            "7fc56270e7a70fa81a5935b72eacbe29"
        """
        h = MD5.new()
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def keccak_512(self):
        """Get KECCAK-512 hash
        
        The Keccak hash algorithm was designed by Guido Bertoni, Joan Daemen, 
        Michaël Peeters, and Gilles Van Assche, building upon RadioGatún. It was 
        selected as the winner of the SHA-3 design competition. This version of the 
        algorithm is Keccak[c=2d] and differs from the SHA-3 specification.

        Returns:
            Chepy: The Chepy object. 
        """
        h = keccak.new(digest_bits=512)
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def keccak_384(self):
        """Get KECCAK-384 hash
        
        The Keccak hash algorithm was designed by Guido Bertoni, Joan Daemen, 
        Michaël Peeters, and Gilles Van Assche, building upon RadioGatún. It was 
        selected as the winner of the SHA-3 design competition. This version of the 
        algorithm is Keccak[c=2d] and differs from the SHA-3 specification.

        Returns:
            Chepy: The Chepy object. 
        """
        h = keccak.new(digest_bits=384)
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def keccak_256(self):
        """Get KECCAK-256 hash
        
        The Keccak hash algorithm was designed by Guido Bertoni, Joan Daemen, 
        Michaël Peeters, and Gilles Van Assche, building upon RadioGatún. It was 
        selected as the winner of the SHA-3 design competition. This version of the 
        algorithm is Keccak[c=2d] and differs from the SHA-3 specification.

        Returns:
            Chepy: The Chepy object. 
        """
        h = keccak.new(digest_bits=256)
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def keccak_224(self):
        """Get KECCAK-224 hash
        
        The Keccak hash algorithm was designed by Guido Bertoni, Joan Daemen, 
        Michaël Peeters, and Gilles Van Assche, building upon RadioGatún. It was 
        selected as the winner of the SHA-3 design competition. This version of the 
        algorithm is Keccak[c=2d] and differs from the SHA-3 specification.

        Returns:
            Chepy: The Chepy object. 
        """
        h = keccak.new(digest_bits=224)
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def shake_256(self, size: int = 64):
        """Get Shake-256 hash
        
        Shake is an Extendable Output Function (XOF) of the SHA-3 hash algorithm, 
        part of the Keccak family, allowing for variable output length/size.

        Args:
            size (int, optional): How many bytes to read, by default 64

        Returns:
            Chepy: The Chepy object. 
        """
        h = SHAKE256.new()
        h.update(self._convert_to_bytes())
        self.state = binascii.hexlify(h.read(size))
        return self

    @ChepyDecorators.call_stack
    def shake_128(self, size: int = 64):
        """Get Shake-128 hash
        
        Shake is an Extendable Output Function (XOF) of the SHA-3 hash algorithm, 
        part of the Keccak family, allowing for variable output length/size.

        Args:
            size (int, optional): How many bytes to read, by default 64

        Returns:
            Chepy: The Chepy object. 
        """
        h = SHAKE128.new()
        h.update(self._convert_to_bytes())
        self.state = binascii.hexlify(h.read(size))
        return self

    @ChepyDecorators.call_stack
    def ripemd_160(self):
        """Get RIPEMD-160 hash
        
        RIPEMD (RACE Integrity Primitives Evaluation Message Digest) is a family of 
        cryptographic hash functions developed in Leuven, Belgium, by Hans Dobbertin, 
        Antoon Bosselaers and Bart Preneel at the COSIC research group at the Katholieke 
        Universiteit Leuven, and first published in 1996.<br><br>RIPEMD was based upon the 
        design principles used in MD4, and is similar in performance to the more popular SHA-1.

        Returns:
            Chepy: The Chepy object. 
        """
        h = RIPEMD.new()
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def blake_2b(self, bits: int = 256, key: bytes = ""):
        """Get Balke-2b hash
        
        Performs BLAKE2b hashing on the input. BLAKE2b is a flavour of the 
        BLAKE cryptographic hash function that is optimized for 64-bit 
        platforms and produces digests of any size between 1 and 64 bytes. 
        Supports the use of an optional key.
        
        Args:
            bits (int, optional): Number of digest bits, by default 256
            key (bytes, optional): Encryption secret key, by default ''
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("A").blake_2b(bits=128, key="key").output
            "6d2e4cba3bc564e02d1a76f585a6795d"
        """
        assert bits in [
            512,
            384,
            256,
            160,
            128,
        ], "Valid bits are 512, 384, 256, 160, 128"
        h = BLAKE2b.new(digest_bits=bits, key=key.encode())
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def blake_2s(self, bits: int = 256, key: bytes = ""):
        """Get Blake-2s hash
        
        Performs BLAKE2s hashing on the input. BLAKE2s is a flavour of 
        the BLAKE cryptographic hash function that is optimized for 8- to 
        32-bit platforms and produces digests of any size between 1 and 32 bytes. 
        Supports the use of an optional key.
        
        Args:
            bits (int, optional): Number of digest bits, by default 256
            key (bytes, optional): Encryption secret key, by default ''
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("A").blake_2s(bits=128, key="key").output
            "4e33cc702e9d08c28a5e9691f23bc66a"
        """
        assert bits in [256, 160, 128], "Valid bits are 256, 160, 128"
        h = BLAKE2s.new(digest_bits=bits, key=key.encode())
        h.update(self._convert_to_bytes())
        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def crc8_checksum(self):
        """Get CRC8 checksum
        
        A cyclic redundancy check (CRC) is an error-detecting code commonly 
        used in digital networks and storage devices to detect accidental changes 
        to raw data. The CRC was invented by W. Wesley Peterson in 1961.

        Returns:
            Chepy: The Chepy object. 
        """
        self.state = Crc8().process(self._convert_to_bytes()).finalhex()
        return self

    @ChepyDecorators.call_stack
    def crc16_checksum(self):
        """Get CRC16 checksum
        
        A cyclic redundancy check (CRC) is an error-detecting code commonly 
        used in digital networks and storage devices to detect accidental changes 
        to raw data. The CRC was invented by W. Wesley Peterson in 1961.

        Returns:
            Chepy: The Chepy object. 
        """
        self.state = CrcArc().process(self._convert_to_bytes()).finalhex()
        return self

    @ChepyDecorators.call_stack
    def crc32_checksum(self):
        """Get CRC32 checksum
        
        A cyclic redundancy check (CRC) is an error-detecting code commonly 
        used in digital networks and storage devices to detect accidental changes 
        to raw data. The CRC was invented by W. Wesley Peterson in 1961.

        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("a").crc32_checksum().output
            "e8b7be43"
        """
        self.state = Crc32().process(self._convert_to_bytes()).finalhex()
        return self

    @ChepyDecorators.call_stack
    def hmac_hash(self, key: bytes = b"", digest: str = "sha1"):
        """Get HMAC hash
        
        HMAC hash the state

        Keyed-Hash Message Authentication Codes (HMAC) are a mechanism for 
        message authentication using cryptographic hash functions.
        
        Args:
            key (bytes, optional): Starting key for the hash, by default b''
            digest (str, optional): The digest type, by default "sha1". Possible values are 
                md5, sha1, sha256 and sha512
        
        Returns:
            Chepy: The Chepy object. 
        
        Raises:
            TypeError: If key is not in bytes
            TypeError: If not a valid/allowed digest type
        """
        if not isinstance(key, bytes):
            if isinstance(key, str):
                key = key.encode()
            elif isinstance(key, int):  # pragma: no cover
                key = bytes(key)
            else:  # pragma: no cover
                raise TypeError("key has to be bytes")

        if digest == "md5":
            h = hmac.new(key, self._convert_to_bytes(), hashlib.md5)
        elif digest == "sha1":
            h = hmac.new(key, self._convert_to_bytes(), hashlib.sha1)
        elif digest == "sha256":
            h = hmac.new(key, self._convert_to_bytes(), hashlib.sha256)
        elif digest == "sha512":
            h = hmac.new(key, self._convert_to_bytes(), hashlib.sha512)
        else:  # pragma: no cover
            raise TypeError(
                "Currently supported digests are md5, sha1, sha256 and sha512"
            )

        self.state = h.hexdigest()
        return self

    @ChepyDecorators.call_stack
    def derive_pbkdf2_key(
        self,
        password: Union[str, bytes],
        salt: Union[str, bytes],
        key_size: int = 256,
        iterations: int = 1000,
        hash_type: Literal["md5", "sha1", "sha256", "sh512"] = "sha1",
        hex_salt: bool = True,
        show_full_key: bool = False,
    ):
        """Derive a PBKDF2 key
        
        Args:
            password (Union[str, bytes]): Password
            salt (Union[str, bytes]): Salt
            key_size (int, optional): Key size. Defaults to 256.
            iterations (int, optional): Number of iterations. Defaults to 1000.
            hash_type (Literal[, optional): Hash type. Defaults to "sha1".
            hex_salt (bool, optional): If salt is in hex format. Defaults to True.
            show_full_key (bool, optional): Show AES256 64 bit key only. Defaults to False.
        
        Raises:
            TypeError: If hash type is not one of md5, sha1, sha256, sha512
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy(".").derive_pbkdf2_key("mR3m", "d9016d44c374f5fb62604683f4d61578").o[:10]
            "7c8898f222"
        """        
        if isinstance(salt, str):
            salt = salt.encode()

        if hex_salt:
            salt = binascii.unhexlify(salt)

        if hash_type == "md5":
            h = PBKDF2(password, salt, key_size, count=iterations, hmac_hash_module=MD5)
        elif hash_type == "sha1":
            h = PBKDF2(password, salt, key_size, count=iterations, hmac_hash_module=SHA1)
        elif hash_type == "sha256":
            h = PBKDF2(password, salt, key_size, count=iterations, hmac_hash_module=SHA256)
        elif hash_type == "sha512":
            h = PBKDF2(password, salt, key_size, count=iterations, hmac_hash_module=SHA512)
        else:  # pragma: no cover
            raise TypeError(
                "Currently supported digests are md5, sha1, sha256 and sha512"
            )

        if show_full_key:
            self.state = h.hex()
        else:
            self.state = h.hex()[:64]
        return self

    @ChepyDecorators.call_stack
    def bcrypt_hash(self, rounds: int = 10):
        """Get Bcrypt hash
        
        bcrypt is a password hashing function designed by Niels Provos and David Mazières, 
        based on the Blowfish cipher, and presented at USENIX in 1999. Besides incorporating 
        a salt to protect against rainbow table attacks, bcrypt is an adaptive function: over 
        time, the iteration count (rounds) can be increased to make it slower, so it remains 
        resistant to brute-force search attacks even with increasing computation power.
        
        Args:
            rounds (int, optional): rounds of hashing, by default 10
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = _crypto_bcrypt(self._convert_to_str(), cost=rounds)
        return self

    @ChepyDecorators.call_stack
    def bcrypt_compare(self, hash: str):
        """Compare Bcrypt hash
        
        Tests whether the provided hash matches the given string at init.
        
        Args:
            hash (str): Required. brypt hash
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> c = Chepy("abc")
            >>> c.bcrypt_compare("$2a$10$SpXMRnrQ4IQqC710xMHfAu0BBr4nJkuPqDvzhiAACnykgn87iE2S2")
            True
        """
        try:
            if _crypto_bcrypt_check(self._convert_to_str(), hash) is None:
                self.state = True
                return self
            else:  # pragma: no cover
                self.state = False
                return self
        except ValueError:  # pragma: no cover
            self.state = False
            return self

    @ChepyDecorators.call_stack
    def scrypt_hash(
        self, salt: str = "", key_length: int = 64, N: int = 14, r: int = 8, p: int = 1
    ):
        """Get Scrypt hash

        scrypt is a password-based key derivation function (PBKDF) created by Colin Percival. 
        The algorithm was specifically designed to make it costly to perform large-scale 
        custom hardware attacks by requiring large amounts of memory. In 2016, the scrypt 
        algorithm was published by IETF as RFC 7914.
        
        Args:
            salt (str, optional): A string of characters that modifies the hash. Defaults to "".
            key_length (int, optional): number of bytes to use when autogenerating new salts. Defaults to 64.
            N (int, optional): CPU/memory cost parameter. Defaults to 14.
            r (int, optional): The blocksize parameter. Defaults to 8.
            p (int, optional): Parallelization parameter;. Defaults to 1.
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("abc").scrypt_hash(salt="", key_length=16).out()
            "f352f3374cf4e344dde4108b96985248"
        """
        assert N < 32, "N must be less than 32"
        self.state = _crypto_scrypt(
            self._convert_to_bytes(), salt=salt, key_len=key_length, N=2 ** N, r=r, p=p
        ).hex()
        return self
