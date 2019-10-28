import hashid

from ..core import Core


class Hashing(Core):
    def identify_hash(self) -> dict:
        hashes = []
        for h in hashid.HashID().identifyHash(self._holder):
            hashes.append({"name": h.name, "hashcat": h.hashcat, "john": h.john})
        return hashes
