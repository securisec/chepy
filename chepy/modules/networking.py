import ipaddress
import regex as re
import urllib.parse as _py_urlparse
from ua_parser.user_agent_parser import Parse as _uap_parse
from ..core import ChepyCore


class Networking(ChepyCore):
    def defang_url(self):
        """Make a URL harmless
        
        Takes a Universal Resource Locator (URL) and 'Defangs' it; 
        meaning the URL becomes invalid, neutralising the risk of accidentally 
        clicking on a malicious link. This is often used when dealing with 
        malicious links or IOCs.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("https://app.google.com/?lol=some data&a=1").defang_url().o
            "hxxps://app[.]google[.]com/?lol=some data&a=1"
        """
        self.state = re.sub(r"(^htt)", "hxx", self._convert_to_str())
        self.state = re.sub(r"\.", "[.]", self._convert_to_str())
        return self

    def refang_url(self):
        """Refangs a URL so that it is clickable
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("hxxps://app[.]google[.]com/?lol=some data&a=1").refang_url().o
            "https://app.google.com/?lol=some data&a=1"
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

        Examples:
            >>> Chepy("2001:4860:4860::8844").defang_ip().o
            "2001[:]4860[:]4860[:][:]8844"
            
            >>> Chepy("127.0.0.1").defang_ip().o
            "127[.]0[.]0[.]1"
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

        Examples:
            >>> Chepy("127[.]0[.]0[.]1").refang_ip().o
            "127.0.0.1"
        """
        self.state = re.sub(r"\[\.\]|\[\:\]", ".", self._convert_to_str())
        return self

    def parse_user_agent(self):
        """Parse a User-Agent string.
        
        Attempts to identify and categorise information contained in a user-agent string.
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> ua = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0"
            >>> Chepy(ua).parse_user_agent().o
            {
                "user_agent": {"family": "Firefox", "major": "62", "minor": "0", "patch": None},
                "os": {
                    "family": "Mac OS X",
                    "major": "10",
                    "minor": "10",
                    "patch": None,
                    "patch_minor": None,
                },
                "device": {"family": "Other", "brand": None, "model": None},
                "string": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0",
            }
        """
        self.state = _uap_parse(self._convert_to_str())
        return self

    def parse_uri(self):
        """Parse a URI
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("http://example.com/resource?foo=bar#fragment").parse_uri().o
            {
                "scheme": "http",
                "location": "example.com",
                "path": "/resource",
                "params": "",
                "query": {"foo": ["bar"]},
                "fragment": "fragment",
            }
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

        Examples:
            >>> Chepy("10.10.10.1/24").parse_ip_range().o
            [
                "10.10.10.1",
                "10.10.10.2,
                ...
                "10.10.10.254"
            ]
        """
        self.state = [
            str(i)
            for i in ipaddress.ip_network(self._convert_to_str(), strict=False).hosts()
        ]
        return self

    def parse_ipv6(self):
        """Get longhand and shorthand of IPv6
        
        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("2001:4860:4860::8888").parse_ipv6().o
            {
                "long": "2001:4860:4860:0000:0000:0000:0000:8888",
                "short": "2001:4860:4860::8888",
            }
        """
        ip = ipaddress.ip_address(self._convert_to_str())
        self.state = {"long": ip.exploded, "short": ip.compressed}
        return self
