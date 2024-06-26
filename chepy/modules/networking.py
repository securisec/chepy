import collections
import ipaddress
import socket
import ssl
import urllib.parse as _py_urlparse
from typing import TypeVar

import regex as re

from ..core import ChepyCore, ChepyDecorators

NetworkingT = TypeVar("NetworkingT", bound="Networking")


class Networking(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    @ChepyDecorators.call_stack
    def defang_url(self) -> NetworkingT:
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

    @ChepyDecorators.call_stack
    def refang_url(self) -> NetworkingT:
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

    @ChepyDecorators.call_stack
    def defang_ip(self) -> NetworkingT:
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

    @ChepyDecorators.call_stack
    def refang_ip(self) -> NetworkingT:
        """Refangs an IP address

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("127[.]0[.]0[.]1").refang_ip().o
            "127.0.0.1"
        """
        self.state = re.sub(r"\[\.\]|\[\:\]", ".", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def parse_uri(self) -> NetworkingT:
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

    @ChepyDecorators.call_stack
    def parse_ip_range(self) -> NetworkingT:
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

    @ChepyDecorators.call_stack
    def parse_ipv6(self) -> NetworkingT:
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

    @ChepyDecorators.call_stack
    def get_ssl_cert(self, port: int = 443) -> NetworkingT:
        """Get the server side SSL certificate for a domain

        Args:
            port (int, optional): Server port. Defaults to 443.

        Returns:
            Chepy: The Chepy object

        Examples:
            >>> Chepy('google.com').get_ssl_cert().o
            {
                'subject': {
                    'commonName': '*.google.com',
                    'organizationName': 'Google LLC',
                ...
                'caIssuers': ('http://pki.goog/gsr2/GTS1O1.crt',),
                'crlDistributionPoints': ('http://crl.pki.goog/GTS1O1.crl',)
            }
        """
        domain = re.sub(r"^\w+://", "", self._convert_to_str())
        with socket.create_connection((domain, port)) as sock:
            context = ssl.create_default_context()
            context.check_hostname = False
            with context.wrap_socket(sock, server_hostname=domain) as sslsock:
                cert = sslsock.getpeercert()
                final = {}
                for key in cert.keys():
                    if key == "subject" or key == "issuer":
                        final[key] = dict(
                            collections.ChainMap(*list(map(dict, cert[key])))
                        )
                    elif key == "subjectAltName":
                        final[key] = list(
                            map(lambda x: dict([x]), cert["subjectAltName"])
                        )
                    else:
                        final[key] = cert[key]
                self.state = final
                return self

    @ChepyDecorators.call_stack
    def int_to_ip(self) -> NetworkingT:
        """Convert an integer to an IP address

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy(3232235777).int_to_ip().o
        """
        self.state = str(ipaddress.ip_address(self._convert_to_int()))
        return self

    @ChepyDecorators.call_stack
    def ip_to_int(self) -> NetworkingT:
        """Convert an integer to an IP address

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy(3232235777).int_to_ip().o
        """
        self.state = int(ipaddress.ip_address(self._convert_to_str()))
        return self
