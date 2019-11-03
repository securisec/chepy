import regex as re
from ua_parser.user_agent_parser import Parse as _uap_parse
from ..core import Core


class Networking(Core):
    def defang_url(self):
        """Takes a Universal Resource Locator (URL) and 'Defangs' it; 
        meaning the URL becomes invalid, neutralising the risk of accidentally 
        clicking on a malicious link. This is often used when dealing with 
        malicious links or IOCs.
        
        Returns
        -------
        Chepy
            The Chepy object. 
        """
        self._holder = re.sub(r"(^htt)", "hxx", self._convert_to_str())
        self._holder = re.sub(r"\.", "[.]", self._convert_to_str())
        return self

    def refang_url(self):
        """Refangs a URL so that it is clickable
        
        Returns
        -------
        Chepy
            The Chepy object. 
        """
        self._holder = re.sub(r"(^hxx)", "htt", self._convert_to_str())
        self._holder = re.sub(r"\[\.\]", ".", self._convert_to_str())
        return self

    def defang_ip(self):
        """Takes a IPv4 or IPv6 address and 'Defangs' it, meaning the 
        IP becomes invalid, removing the risk of accidentally utilising 
        it as an IP address.
        
        Returns
        -------
        Chepy
            The Chepy object. 
        """
        if ":" in self._convert_to_str():
            self._holder = re.sub(r":", "[:]", self._convert_to_str())
        else:
            self._holder = re.sub(r"\.|:", "[.]", self._convert_to_str())
        return self

    def refang_ip(self):
        """Refangs an IP address
        
        Returns
        -------
        Chepy
            The Chepy object. 
        """
        self._holder = re.sub(r"\[\.\]|\[\:\]", ".", self._convert_to_str())
        return self

    def parse_user_agent(self):
        """Attempts to identify and categorise information contained in a user-agent string.
        
        Returns
        -------
        Chepy
            The Chepy object.
        """
        self._holder = _uap_parse(self._convert_to_str())
        return self
