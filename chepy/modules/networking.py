import ipaddress
import regex as re
import urllib.parse as _py_urlparse
from ua_parser.user_agent_parser import Parse as _uap_parse
from ..core import Core


class Networking(Core):
    def defang_url(self):
        """Make a URL harmless
        
        Takes a Universal Resource Locator (URL) and 'Defangs' it; 
        meaning the URL becomes invalid, neutralising the risk of accidentally 
        clicking on a malicious link. This is often used when dealing with 
        malicious links or IOCs.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = re.sub(r"(^htt)", "hxx", self._convert_to_str())
        self.state = re.sub(r"\.", "[.]", self._convert_to_str())
        return self

    def refang_url(self):
        """Refangs a URL so that it is clickable
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = re.sub(r"(^hxx)", "htt", self._convert_to_str())
        self.state = re.sub(r"\[\.\]", ".", self._convert_to_str())
        return self

    def defang_ip(self):
        """Make an IP address harmless
        
        Takes a IPv4 or IPv6 address and 'Defangs' it, meaning the 
        IP becomes invalid, removing the risk of accidentally utilising 
        it as an IP address.
        
        Returns:
            Chepy: The Chepy object. 
        """
        if ":" in self._convert_to_str():
            self.state = re.sub(r":", "[:]", self._convert_to_str())
        else:
            self.state = re.sub(r"\.|:", "[.]", self._convert_to_str())
        return self

    def refang_ip(self):
        """Refangs an IP address
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = re.sub(r"\[\.\]|\[\:\]", ".", self._convert_to_str())
        return self

    def parse_user_agent(self):
        """Parse a User-Agent string.
        
        Attempts to identify and categorise information contained in a user-agent string.
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = _uap_parse(self._convert_to_str())
        return self

    def parse_uri(self):
        """Parse a URI
        
        Returns:
            Chepy: The Chepy object.
        """
        parsed = _py_urlparse.urlparse(self._convert_to_str())
        self.state = {
            "scheme": parsed.scheme,
            "location": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": _py_urlparse.parse_qs(parsed.query),
            "fragment": parsed.fragment,
        }
        return self

    def parse_ip_range(self):
        """Enumerate IP address in a CIDR range
        
        Returns:
            Chepy: The Chepy object.
        """
        self.state = [str(i) for i in ipaddress.ip_network(self._convert_to_str(), strict=False).hosts()]
        return self

    def parse_ipv6(self):
        """Get longhand and shorthand of IPv6
        
        Returns:
            Chepy: The Chepy object.
        """
        ip = ipaddress.ip_address(self._convert_to_str())
        self.state = {'long': ip.exploded, 'short': ip.compressed}
        return self
