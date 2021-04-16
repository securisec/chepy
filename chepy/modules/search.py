from typing import TypeVar

import regex as re

from ..core import ChepyCore, ChepyDecorators

SearchT = TypeVar("SearchT", bound="Search")


class Search(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    """Class that is geared towards regex searches of secrets

    `Reference <https://github.com/dxa4481/truffleHog>`__
    """

    @ChepyDecorators.call_stack
    def search(self, pattern: str) -> SearchT:
        """Search. Group matches are returned as tuples.

        Args:
            pattern (str): String pattern to search

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("abcdefg123 and again abcdefg123").search("abc(de)fg(12)(3)").o
            [('abcdefg123', 'de', '12', '3'), ('abcdefg123', 'de', '12', '3')]
        """
        self.state = re.findall("({})".format(pattern), self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def search_ctf_flags(self, prefix: str, postfix: str = ".+?\{*\}") -> SearchT:
        """Search CTF style flags.

        This by default assumes that the flag format is similar
        to something like picoCTF{some_flag} as an example.

        Args:
            prefix (str): Prefix of the flag. Like `picoCTF`
            postfix (str, optional): Regex for the remainder of the flag.
                Defaults to '.+\{.+}'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("tests/files/flags").read_file().search_ctf_flags("pico").get_by_index(0)
            picoCTF{r3source_pag3_f1ag}
        """
        self.state = re.findall(prefix + postfix, self._convert_to_str(), re.IGNORECASE)
        return self

    @ChepyDecorators.call_stack
    def search_slack_tokens(self) -> SearchT:
        """Search slack tokens

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("tests/files/flags").read_file().search_slack_tokens().get_by_index(0)
            xoxp...859
        """
        self.state = re.findall(
            "(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
            self._convert_to_str(),
        )
        return self

    @ChepyDecorators.call_stack
    def search_slack_webhook(self) -> SearchT:
        """Search slack webhook

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            "https://hooks\.slack\.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
            self._convert_to_str(),
        )
        return self

    @ChepyDecorators.call_stack
    def search_private_key(self) -> SearchT:
        """Search varios private key headers

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            "-----BEGIN (RSA|OPENSSH|DSA|EC) PRIVATE KEY-----", self._convert_to_str()
        )
        return self

    @ChepyDecorators.call_stack
    def search_twilio_key(self) -> SearchT:
        """Search for Twilio api key

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall("SK[a-z0-9]{32}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def search_aws_key(self) -> SearchT:
        """Search for AWS key id

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall("AKIA[0-9A-Z]{16}", self._convert_to_str())
        return self
