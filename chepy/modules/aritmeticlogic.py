import binascii
import statistics
from typing import TypeVar, Union, Literal
from functools import reduce as functools_reduce

from ..core import ChepyCore, ChepyDecorators
from .exceptions import StateNotList
from .internal.helpers import detect_delimiter


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
    def addition(self, delimiter=None) -> AritmeticLogicT:
        """Adds a list of numbers. If an item in the string is not a number it is excluded from the list.

        Args:
            delimiter (str, optional): Delimiter. Defaults to None.

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_str()
        print("🟢 ", data)
        if not delimiter:
            delimiter = detect_delimiter(data)
        # only work on numbers
        nums = []
        for n in data.split(delimiter):
            try:
                nums.append(int(n))
            except:  # noqa: E722
                continue

        self.state = functools_reduce(lambda x, y: x + y, nums)
        return self

    @ChepyDecorators.call_stack
    def sub(self, n: int) -> AritmeticLogicT:
        """SUB the input with the given key

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
    def subtract(self, delimiter=None) -> AritmeticLogicT:
        """Subtracts a list of numbers. If an item in the string is not a number it is excluded from the list.

        Args:
            delimiter (str, optional): Delimiter. Defaults to None.

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_str()
        if not delimiter:
            delimiter = detect_delimiter(data)
        # only work on numbers
        nums = []
        for n in data.split(delimiter):
            try:
                nums.append(int(n))
            except:  # noqa: E722
                continue

        self.state = functools_reduce(lambda x, y: x - y, nums)
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

    @ChepyDecorators.call_stack
    def bit_shift_right(
        self,
        amount: int = 1,
        operation_type: Literal["logical", "arithmetic"] = "logical",
    ) -> AritmeticLogicT:
        """Shifts the bits in each byte towards the right by the specified amount.

        Args:
            amount (int, optional): Amount. Defaults to 1
            operation_type (Literal['logical', 'arithmetic'], optional): Operation type. Defaults to 'logical'.

        Returns:
            Chepy: The Chepy object.
        """
        mask = 0x80 if operation_type.lower() != "logical" else 0
        output_bytes = [
            (byte >> int(amount)) ^ (byte & mask) for byte in self._convert_to_bytes()
        ]
        self.state = bytearray(output_bytes)
        return self

    @ChepyDecorators.call_stack
    def bit_shift_left(self, amount: int = 1):
        """Shifts each byte in the input byte array to the left by a specified amount.

        Args:
            amount (int, optional): Amount. Defaults to 1.

        Returns:
            Chepy: The Chepy object.
        """
        output_bytes = [(byte << amount) & 0xFF for byte in self._convert_to_bytes()]
        self.state = bytearray(output_bytes)
        return self
