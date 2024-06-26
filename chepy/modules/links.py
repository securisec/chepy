import base64
from typing import TypeVar

import regex as re

from ..core import ChepyCore, ChepyDecorators

LinksT = TypeVar("LinksT", bound="Links")


class Links(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    @ChepyDecorators.call_stack
    def pastebin_to_raw(self) -> LinksT:
        """Convert a pastebin link to raw pastebin link

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("https://pastebin.com/abCD").pastebin_to_raw()
            'https://pastebin.com/raw/abCD'
        """
        self.state = re.sub(r"(pastebin\.com)(/)", r"\1/raw\2", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def github_to_raw(self) -> LinksT:
        """Convert a github link to raw github link

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("https://github.com/securisec/chepy/blob/master/README.md").github_to_raw()
            'https://raw.githubusercontent.com/securisec/chepy/master/README.md'
        """
        self.state = re.sub(
            "/blob",
            "",
            re.sub(
                r"(github\.com)(/)",
                r"raw.githubusercontent.com\2",
                self._convert_to_str(),
            ),
        )
        return self

    @ChepyDecorators.call_stack
    def google_search_ei_to_epoch(self) -> LinksT:
        """Convert a google search ei query param to epoch

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("Bh8hYqykHc64mAXkkoTgCg==").google_search_ei_to_epoch()
            1646337798
        """
        decoded = base64.urlsafe_b64decode(self._convert_to_str())
        timestamp = ord(chr(decoded[0]))
        timestamp += ord(chr(decoded[1])) * 256
        timestamp += ord(chr(decoded[2])) * 256**2
        timestamp += ord(chr(decoded[3])) * 256**3
        self.state = timestamp
        return self
