import sys

from ..core import Core


class Utils(Core):
    def reverse(self) -> "Chepy":
        """Reverses the string.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out` or `output()` or 
            copy to clipboard with `copy()`
        """
        self._holder = self._holder[::-1]
        return self
