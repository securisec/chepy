import time
from datetime import datetime
from ..core import Core


class DateTime(Core):
    def from_unix_ts(self):
        """Convert UNIX timestamp to datetime
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = datetime.fromtimestamp(self._convert_to_int()).strftime("%c")
        return self

    def to_unix_ts(self): # pragma: no cover
        """Convert datetime string to unix ts

        The format for the string is %a %b %d %H:%M:%S %Y, which is equivalent to 
        %c from datatime.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = int(
            time.mktime(time.strptime(self._convert_to_str(), "%a %b %d %H:%M:%S %Y"))
        )
        return self

