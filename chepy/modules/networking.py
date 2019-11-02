import regex as re
from ..core import Core


class Networking(Core):
    def defang_url(self) -> "Baked":
        """Takes a Universal Resource Locator (URL) and 'Defangs' it; 
        meaning the URL becomes invalid, neutralising the risk of accidentally 
        clicking on a malicious link. This is often used when dealing with 
        malicious links or IOCs.
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = re.sub(r"(^htt)", "hxx", self._convert_to_str())
        self._holder = re.sub(r"\.", "[.]", self._convert_to_str())
        return self

    def refang_url(self) -> "Baked":
        """Refangs a URL so that it is clickable
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = re.sub(r"(^hxx)", "htt", self._convert_to_str())
        self._holder = re.sub(r"\[\.\]", ".", self._convert_to_str())
        return self

    def defang_ip(self) -> "Baked":
        """Takes a IPv4 or IPv6 address and 'Defangs' it, meaning the 
        IP becomes invalid, removing the risk of accidentally utilising 
        it as an IP address.
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        if ":" in self._convert_to_str():
            self._holder = re.sub(r":", "[:]", self._convert_to_str())
        else:
            self._holder = re.sub(r"\.|:", "[.]", self._convert_to_str())
        return self

    def refang_ip(self) -> "Baked":
        """Refangs an IP address
        
        Returns
        -------
        Baked
            The Baked object. 
        """
        self._holder = re.sub(r"\[\.\]|\[\:\]", ".", self._convert_to_str())
        return self
