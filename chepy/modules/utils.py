import regex as re

from ..core import Core


class Utils(Core):
    def reverse(self, count: int = 1):
        """Reverses the string.

        Parameters
        ----------
        count : int
            Reverse by the number of characters indicated in count

        Returns
        -------
        Chepy
            The Chepy object. 
        """
        if count == 1:
            self._holder = self._holder[::-1]
            return self
        else:
            self._holder = "".join([self._holder[x:x+count] for x in range(0,len(self._holder),count)][::-1])
            return self

    def count_occurances(self, regex: str, case_sensitive: bool = False):
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
            The Chepy object. 
        """
        if case_sensitive:
            r = re.compile(regex)
        else:
            r = re.compile(regex, re.IGNORECASE)
        self._holder = len(r.findall(self._convert_to_str()))
        return self
