import regex as re

from ..core import Core


class Utils(Core):
    def reverse(self) -> "Baked":
        """Reverses the string.

        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = self._holder[::-1]
        return self

    def count_occurances(self, regex: str, case_sensitive: bool = False) -> "Baked":
        """Counts the number of times the provided string occurs in the input.

        Parameters
        ----------
        regex : str
            Regex string to search for
        case_sensitive : bool, optional
            If search should be case insensitive, by default False

        Returns
        -------
        Baked
            The Baked object. 
        """
        if case_sensitive:
            r = re.compile(regex)
        else:
            r = re.compile(regex, re.IGNORECASE)
        self._holder = len(r.findall(self._convert_to_str()))
        return self
