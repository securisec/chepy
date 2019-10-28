import sys

from ..core import Core


class Utils(Core):
    @property
    def reverse(self, by_line: bool = False) -> "Chepy":
        # todo by line
        self._holder = self._holder[::-1]
        return self
