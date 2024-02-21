import binascii
import statistics
from typing import TypeVar, Union

from ..core import ChepyCore, ChepyDecorators
from .exceptions import StateNotList


AritmeticLogicT = TypeVar("AritmeticLogicT", bound="AritmeticLogic")


class AritmeticLogic(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    def __hex_to_int(self, n):  # pragma: no cover
        if isinstance(n, str):
            return int(n, 0)
        if isinstance(n, int):
            return n

    @ChepyDecorators.call_stack
    def str_bit_shift_right(self, amount: int) -> AritmeticLogicT:
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

    @ChepyDecorators.call_stack
    def add(self, n: int) -> AritmeticLogicT:
        """Add a number to the state

        Args:
            n (int): Number to add with. Can be decimal or hex string without 0x

        Returns:
            Chepy: The Chepy object.
        """
        # Determine the base of the key (hexadecimal or decimal)
        if isinstance(n, int):
            # Try converting to decimal
            key_int = n
        else:
            try:
                # Try converting to hexadecimal
                key_int = int(n, 16)
            except ValueError:  # pragma: no cover
                self._log.error(
                    "Invalid key format. Must be a decimal or hexadecimal string."
                )
                return self

        hold = b""
        for char_code in self._convert_to_bytes():
            # Add the key to the integer and take the result modulo 255
            result_code = (char_code + key_int) % 256

            # Convert the result back to a byte
            hold += result_code.to_bytes(1, byteorder="big")

        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def subtract(self, n: int) -> AritmeticLogicT:
        """Subtract a number to the state

        Args:
            n (int): Number to subtract with

        Returns:
            Chepy: The Chepy object.
        """
        # Determine the base of the key (hexadecimal or decimal)
        if isinstance(n, int):
            # Try converting to decimal
            key_int = n
        else:
            try:
                # Try converting to hexadecimal
                key_int = int(n, 16)
            except ValueError:  # pragma: no cover
                self._log.error(
                    "Invalid key format. Must be a decimal or hexadecimal string."
                )
                return self

        hold = b""
        for char_code in self._convert_to_bytes():
            # Add the key to the integer and take the result modulo 255
            result_code = (char_code - key_int) % 256

            # Convert the result back to a byte
            hold += result_code.to_bytes(1, byteorder="big")

        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def multiply(self, n: int) -> AritmeticLogicT:
        """Multiply a number to the state

        Args:
            n (int): Number to multiply with

        Returns:
            Chepy: The Chepy object.
        """
        if not isinstance(self.state, int):
            self.state = self.__hex_to_int(self.state)
        self.state = self.state * n
        return self

    @ChepyDecorators.call_stack
    def divide(self, n: int) -> AritmeticLogicT:
        """Divide a number to the state. Chepy is not optimized for float math.
        Subsequent methods may fail.

        Args:
            n (int): Number to divide with

        Returns:
            Chepy: The Chepy object.
        """
        if not isinstance(self.state, int):
            self.state = self.__hex_to_int(self.state)
        self.state = self.state / n
        return self

    @ChepyDecorators.call_stack
    def power(self, n: int) -> AritmeticLogicT:
        """Convert state to the n power of

        Args:
            n (int): Exponent

        Returns:
            Chepy: The Chepy object.
        """
        if not isinstance(self.state, int):
            self.state = self.__hex_to_int(self.state)
        self.state = self.state**n
        return self

    @ChepyDecorators.call_stack
    def sum(self) -> AritmeticLogicT:
        """Calculate the sum of the state

        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, list), StateNotList()
        numbers = list(self.__hex_to_int(x) for x in self.state)
        self.state = sum(numbers)
        return self

    @ChepyDecorators.call_stack
    def mean(self) -> AritmeticLogicT:
        """Calculate the mean of the state

        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, list), StateNotList()
        numbers = list(self.__hex_to_int(x) for x in self.state)
        self.state = statistics.mean(numbers)
        return self

    @ChepyDecorators.call_stack
    def median(self) -> AritmeticLogicT:
        """Calculate the median of the state

        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, list), StateNotList()
        numbers = list(self.__hex_to_int(x) for x in self.state)
        self.state = statistics.median(numbers)
        return self

    @ChepyDecorators.call_stack
    def int_to_base(self, base: Union[int, str]) -> AritmeticLogicT:
        """Convert the state to a different base

        Args:
            base (int): Base to convert to

        Returns:
            Chepy: The Chepy object.
        """
        self.state = int(self.state, base)
        return self
