import binascii
import hashlib
import hashid
from Crypto.Hash import MD2, MD4, MD5
from Crypto.Hash import keccak
from Crypto.Hash import SHAKE128, SHAKE256
from Crypto.Hash import RIPEMD, RIPEMD160

from ..core import Core


class Hashing(Core):
    def identify_hash(self) -> dict:
        """Tries to determine information about a given hash and suggests which 
        algorithm may have been used to generate it based on its length. 
        
        Returns
        -------
        dict
            Dictionary of hash name, hashcat and john the ripper types
        """
        hashes = []
        for h in hashid.HashID().identifyHash(self._holder):
            hashes.append({"name": h.name, "hashcat": h.hashcat, "john": h.john})
        return hashes

    @property
    def sha1(self) -> "Chepy":
        """The SHA (Secure Hash Algorithm) hash functions were designed by the NSA. 
        SHA-1 is the most established of the existing SHA hash functions and it is 
        used in a variety of security applications and protocols. However, SHA-1's 
        collision resistance has been weakening as new attacks are discovered or improved.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = hashlib.sha1(self._convert_to_bytes()).hexdigest()
        return self

    @property
    def sha2_256(self) -> "Chepy":
        """The SHA-2 (Secure Hash Algorithm 2) hash functions were designed by the NSA. SHA-2 
        includes significant changes from its predecessor, SHA-1. The SHA-2 family consists of 
        hash functions with digests (hash values) that are 224, 256, 384 or 512 bits: SHA224, 
        SHA256, SHA384, SHA512. SHA-512 operates on 64-bit words. SHA-256 operates on 32-bit 
        words. SHA-384 is largely identical to SHA-512 but is truncated to 384 bytes. SHA-224 
        is largely identical to SHA-256 but is truncated to 224 bytes. SHA-512/224 and SHA-512/256 
        are truncated versions of SHA-512, but the initial values are generated using the method 
        described in Federal Information Processing Standards (FIPS) PUB 180-4.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = hashlib.sha256(self._convert_to_bytes()).hexdigest()
        return self

    @property
    def sha2_512(self) -> "Chepy":
        """The SHA-2 (Secure Hash Algorithm 2) hash functions were designed by the NSA. SHA-2 
        includes significant changes from its predecessor, SHA-1. The SHA-2 family consists of 
        hash functions with digests (hash values) that are 224, 256, 384 or 512 bits: SHA224, 
        SHA256, SHA384, SHA512. SHA-512 operates on 64-bit words. SHA-256 operates on 32-bit 
        words. SHA-384 is largely identical to SHA-512 but is truncated to 384 bytes. SHA-224 
        is largely identical to SHA-256 but is truncated to 224 bytes. SHA-512/224 and SHA-512/256 
        are truncated versions of SHA-512, but the initial values are generated using the method 
        described in Federal Information Processing Standards (FIPS) PUB 180-4.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = hashlib.sha512(self._convert_to_bytes()).hexdigest()
        return self

    @property
    def sha2_384(self) -> "Chepy":
        """The SHA-2 (Secure Hash Algorithm 2) hash functions were designed by the NSA. SHA-2 
        includes significant changes from its predecessor, SHA-1. The SHA-2 family consists of 
        hash functions with digests (hash values) that are 224, 256, 384 or 512 bits: SHA224, 
        SHA256, SHA384, SHA512. SHA-512 operates on 64-bit words. SHA-256 operates on 32-bit 
        words. SHA-384 is largely identical to SHA-512 but is truncated to 384 bytes. SHA-224 
        is largely identical to SHA-256 but is truncated to 224 bytes. SHA-512/224 and SHA-512/256 
        are truncated versions of SHA-512, but the initial values are generated using the method 
        described in Federal Information Processing Standards (FIPS) PUB 180-4.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = hashlib.sha384(self._convert_to_bytes()).hexdigest()
        return self

    @property
    def sha2_224(self) -> "Chepy":
        """The SHA-2 (Secure Hash Algorithm 2) hash functions were designed by the NSA. SHA-2 
        includes significant changes from its predecessor, SHA-1. The SHA-2 family consists of 
        hash functions with digests (hash values) that are 224, 256, 384 or 512 bits: SHA224, 
        SHA256, SHA384, SHA512. SHA-512 operates on 64-bit words. SHA-256 operates on 32-bit 
        words. SHA-384 is largely identical to SHA-512 but is truncated to 384 bytes. SHA-224 
        is largely identical to SHA-256 but is truncated to 224 bytes. SHA-512/224 and SHA-512/256 
        are truncated versions of SHA-512, but the initial values are generated using the method 
        described in Federal Information Processing Standards (FIPS) PUB 180-4.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = hashlib.sha224(self._convert_to_bytes()).hexdigest()
        return self

    @property
    def sha3_512(self) -> "Chepy":
        """The SHA-3 (Secure Hash Algorithm 3) hash functions were released by NIST on August 5, 2015. 
        Although part of the same series of standards, SHA-3 is internally quite different from the 
        MD5-like structure of SHA-1 and SHA-2.<br><br>SHA-3 is a subset of the broader cryptographic 
        primitive family Keccak designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche, 
        building upon RadioGatún.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = hashlib.sha3_512(self._convert_to_bytes()).hexdigest()
        return self

    @property
    def sha3_256(self) -> "Chepy":
        """The SHA-3 (Secure Hash Algorithm 3) hash functions were released by NIST on August 5, 2015. 
        Although part of the same series of standards, SHA-3 is internally quite different from the 
        MD5-like structure of SHA-1 and SHA-2.<br><br>SHA-3 is a subset of the broader cryptographic 
        primitive family Keccak designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche, 
        building upon RadioGatún.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = hashlib.sha3_256(self._convert_to_bytes()).hexdigest()
        return self

    @property
    def sha3_384(self) -> "Chepy":
        """The SHA-3 (Secure Hash Algorithm 3) hash functions were released by NIST on August 5, 2015. 
        Although part of the same series of standards, SHA-3 is internally quite different from the 
        MD5-like structure of SHA-1 and SHA-2.<br><br>SHA-3 is a subset of the broader cryptographic 
        primitive family Keccak designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche, 
        building upon RadioGatún.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = hashlib.sha3_384(self._convert_to_bytes()).hexdigest()
        return self

    @property
    def sha3_224(self) -> "Chepy":
        """The SHA-3 (Secure Hash Algorithm 3) hash functions were released by NIST on August 5, 2015. 
        Although part of the same series of standards, SHA-3 is internally quite different from the 
        MD5-like structure of SHA-1 and SHA-2.<br><br>SHA-3 is a subset of the broader cryptographic 
        primitive family Keccak designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche, 
        building upon RadioGatún.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = hashlib.sha3_224(self._convert_to_bytes()).hexdigest()
        return self

    @property
    def md2(self):
        """The MD2 (Message-Digest 2) algorithm is a cryptographic hash function developed by 
        Ronald Rivest in 1989. The algorithm is optimized for 8-bit computers.Although MD2 is 
        no longer considered secure, even as of 2014, it remains in use in public key 
        infrastructures as part of certificates generated with MD2 and RSA.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = MD2.new()
        h.update(self._convert_to_bytes())
        self._holder = h.hexdigest()
        return self

    @property
    def md4(self):
        """The MD4 (Message-Digest 4) algorithm is a cryptographic hash function 
        developed by Ronald Rivest in 1990. The digest length is 128 bits. The algorithm 
        has influenced later designs, such as the MD5, SHA-1 and RIPEMD algorithms.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = MD4.new()
        h.update(self._convert_to_bytes())
        self._holder = h.hexdigest()
        return self

    @property
    def md5(self):
        """MD5 (Message-Digest 5) is a widely used hash function. It has been used 
        in a variety of security applications and is also commonly used to check 
        the integrity of files.<br><br>However, MD5 is not collision resistant and 
        it isn't suitable for applications like SSL/TLS certificates or digital 
        signatures that rely on this property.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = MD5.new()
        h.update(self._convert_to_bytes())
        self._holder = h.hexdigest()
        return self

    @property
    def keccak_512(self):
        """The Keccak hash algorithm was designed by Guido Bertoni, Joan Daemen, 
        Michaël Peeters, and Gilles Van Assche, building upon RadioGatún. It was 
        selected as the winner of the SHA-3 design competition. This version of the 
        algorithm is Keccak[c=2d] and differs from the SHA-3 specification.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = keccak.new(digest_bits=512)
        h.update(self._convert_to_bytes())
        self._holder = h.hexdigest()
        return self

    @property
    def keccak_384(self):
        """The Keccak hash algorithm was designed by Guido Bertoni, Joan Daemen, 
        Michaël Peeters, and Gilles Van Assche, building upon RadioGatún. It was 
        selected as the winner of the SHA-3 design competition. This version of the 
        algorithm is Keccak[c=2d] and differs from the SHA-3 specification.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = keccak.new(digest_bits=384)
        h.update(self._convert_to_bytes())
        self._holder = h.hexdigest()
        return self

    @property
    def keccak_256(self):
        """The Keccak hash algorithm was designed by Guido Bertoni, Joan Daemen, 
        Michaël Peeters, and Gilles Van Assche, building upon RadioGatún. It was 
        selected as the winner of the SHA-3 design competition. This version of the 
        algorithm is Keccak[c=2d] and differs from the SHA-3 specification.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = keccak.new(digest_bits=256)
        h.update(self._convert_to_bytes())
        self._holder = h.hexdigest()
        return self

    @property
    def keccak_224(self):
        """The Keccak hash algorithm was designed by Guido Bertoni, Joan Daemen, 
        Michaël Peeters, and Gilles Van Assche, building upon RadioGatún. It was 
        selected as the winner of the SHA-3 design competition. This version of the 
        algorithm is Keccak[c=2d] and differs from the SHA-3 specification.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = keccak.new(digest_bits=224)
        h.update(self._convert_to_bytes())
        self._holder = h.hexdigest()
        return self

    def shake_256(self, size: int = 64) -> "Chepy":
        """Shake is an Extendable Output Function (XOF) of the SHA-3 hash algorithm, 
        part of the Keccak family, allowing for variable output length/size.

        Parameters
        ----------
        size : int, optional
            How many bytes to read, by default 64

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = SHAKE256.new()
        h.update(self._convert_to_bytes())
        self._holder = binascii.hexlify(h.read(size))
        return self

    def shake_128(self, size: int = 64) -> "Chepy":
        """Shake is an Extendable Output Function (XOF) of the SHA-3 hash algorithm, 
        part of the Keccak family, allowing for variable output length/size.

        Parameters
        ----------
        size : int, optional
            How many bytes to read, by default 64

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = SHAKE128.new()
        h.update(self._convert_to_bytes())
        self._holder = binascii.hexlify(h.read(size))
        return self

    @property
    def ripemd_160(self) -> "Chepy":
        """RIPEMD (RACE Integrity Primitives Evaluation Message Digest) is a family of 
        cryptographic hash functions developed in Leuven, Belgium, by Hans Dobbertin, 
        Antoon Bosselaers and Bart Preneel at the COSIC research group at the Katholieke 
        Universiteit Leuven, and first published in 1996.<br><br>RIPEMD was based upon the 
        design principles used in MD4, and is similar in performance to the more popular SHA-1.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        h = RIPEMD.new()
        h.update(self._convert_to_bytes())
        self._holder = h.hexdigest()
        return self
