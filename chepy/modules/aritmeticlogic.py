import binascii
import statistics
from typing import TypeVar

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
            n (int): Number to add with

        Returns:
            Chepy: The Chepy object.
        """
        if not isinstance(self.state, int):
            self.state = self.__hex_to_int(self.state)
        self.state = self.state + n
        return self

    @ChepyDecorators.call_stack
    def subtract(self, n: int) -> AritmeticLogicT:
        """Subtract a number to the state

        Args:
            n (int): Number to subtract with

        Returns:
            Chepy: The Chepy object.
        """
        if not isinstance(self.state, int):
            self.state = self.__hex_to_int(self.state)
        self.state = self.state - n
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
        """Divide a number to the state

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
        self.state = self.state ** n
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
