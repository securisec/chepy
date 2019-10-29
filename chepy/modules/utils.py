import re

from ..core import Core


class Utils(Core):
    def reverse(self) -> "Chepy":
        """Reverses the string.

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out()` or `output` or 
            copy to clipboard with `copy()`
        """
        self._holder = self._holder[::-1]
        return self

    def count_occurances(self, regex: str, case_sensitive: bool = False) -> "Chepy":
        """Counts the number of times the provided string occurs in the input.

        Parameters
        ----------
        regex : str
            Regex string to search for
        case_sensitive : bool, optional
            If search should be case insensitive, by default False

        Returns
        -------
        Chepy
            The Chepy object. Extract data with `out()` or `output` or 
            copy to clipboard with `copy()`
        """
        if case_sensitive:
            r = re.compile(regex)
        else:
            r = re.compile(regex, re.IGNORECASE)
        self._holder = len(r.findall(self._convert_to_str()))
        return self
