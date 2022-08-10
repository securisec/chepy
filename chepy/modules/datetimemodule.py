import time
from datetime import datetime
from typing import TypeVar

from ..core import ChepyCore, ChepyDecorators

DateTimeT = TypeVar("DateTimeT", bound="DateTime")


class DateTime(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    @ChepyDecorators.call_stack
    def from_unix_timestamp(self, format: str='%c') -> DateTimeT:
        """Convert UNIX timestamp to datetime

        Args:
            format: Format to use for datetime.strftime()

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("1573426649").from_unix_timestamp()
            "Sun Nov 10 17:57:29 2019"
        """
        self.state = datetime.fromtimestamp(self._convert_to_int()).strftime(format)
        return self

    @ChepyDecorators.call_stack
    def to_unix_timestamp(self) -> DateTimeT:  # pragma: no cover
        """Convert datetime string to unix ts

        The format for the string is %a %b %d %H:%M:%S %Y, which is equivalent to
        %c from datatime.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("Sun Nov 10 17:57:29 2019").to_unix_timestamp()
            "1573426649"
        """
        self.state = int(
            time.mktime(time.strptime(self._convert_to_str(), "%a %b %d %H:%M:%S %Y"))
        )
        return self
