import hashlib
import hashid

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
    def sha256(self):
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
