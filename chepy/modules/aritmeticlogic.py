import binascii
from ..core import ChepyCore


class AritmeticLogic(ChepyCore):
    def str_bit_shift_right(self, amount: int):
        """Bit shift string right
        
        Args:
            amount (int): Amount to shift
        
        Returns:
            Chepy: The Chepy object
        """
        self.state = binascii.unhexlify(
            "".join(list(format(ord(x) >> int(amount), "02x") for x in list("hello")))
        )
        return self
