from typing import TypeVar
from urllib.parse import urlparse as _pyurlparse

import jsonpath_rw
import lazy_import
import regex as re
import ujson

parsel = lazy_import.lazy_module("parsel")
from ..core import ChepyCore, ChepyDecorators

ExtractorsT = TypeVar("ExtractorsT", bound="Extractors")


class Extractors(ChepyCore):
    def __init__(self, *data):
        super().__init__(*data)

    def _parsel_obj(self):
        """Returns a parsel.Selector object"""
        return parsel.Selector(self._convert_to_str())

    @ChepyDecorators.call_stack
    def extract_hashes(self) -> ExtractorsT:
        """Extract md5, sha1, sha256 and sha512 hashes

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy(
            >>>     ["60b725f10c9c85c70d97880dfe8191b3", "3f786850e387550fdab836ed7e6dc881de23001b"]
            >>> ).extract_hashes()
            {'md5': [b'60b725f10c9c85c70d97880dfe8191b3'], 'sha1': [b'3f786850e387550fdab836ed7e6dc881de23001b'], 'sha256': [], 'sha512': []}
        """
        data = self._convert_to_bytes()
        found = {}
        found["md5"] = re.findall(
            rb"(?:[^a-fA-F\d]|\b)([a-fA-F\d]{32})(?:[^a-fA-F\d]|\b)", data
        )
        found["sha1"] = re.findall(
            rb"(?:[^a-fA-F\d]|\b)([a-fA-F\d]{40})(?:[^a-fA-F\d]|\b)", data
        )
        found["sha256"] = re.findall(
            rb"(?:[^a-fA-F\d]|\b)([a-fA-F\d]{64})(?:[^a-fA-F\d]|\b)", data
        )
        found["sha512"] = re.findall(
            rb"(?:[^a-fA-F\d]|\b)([a-fA-F\d]{128})(?:[^a-fA-F\d]|\b)", data
        )
        self.state = found
        return self

    @ChepyDecorators.call_stack
    def extract_strings(self, length: int = 4) -> ExtractorsT:
        """Extract strings from state

        Args:
            length (int, optional): Min length of string. Defaults to 4.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("tests/files/hello").load_file().extract_strings().o
            [
                b'__PAGEZERO',
                b'__TEXT',
                b'__text',
                b'__TEXT',
                b'__stubs',
                b'__TEXT',
                ...
            ]
        """
        pattern = b"[^\x00-\x1F\x7F-\xFF]{" + str(length).encode() + b",}"
        self.state = re.findall(pattern, self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def extract_ips(
        self, invalid: bool = False, is_binary: bool = False
    ) -> ExtractorsT:
        """Extract ipv4 and ipv6 addresses

        Args:
            invalid (bool, optional): Include :: addresses. Defaults to False.
            is_binary (bool, optional): The state is in binary format. It will then first
                extract the strings from it before matching.

        Returns:
            Chepy: The Chepy object.
        """
        pattern = b"((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))"
        if is_binary:  # pragma: no cover
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else:
            matched = list(
                filter(
                    lambda x: re.search(pattern, x), self._convert_to_bytes().split()
                )
            )
        self.state = matched
        return self

    @ChepyDecorators.call_stack
    def extract_email(self, is_binary: bool = False) -> ExtractorsT:
        """Extract email

        Args:
            is_binary (bool, optional): The state is in binary format. It will then first
                extract the strings from it before matching.

        Returns:
            Chepy: The Chepy object.

        Examples:
            Sometimes, the state is in a binary format, and not readable. In this case
            set the binary flag to True.

            >>> Chepy("tests/files/test.der").load_file().extract_email(is_binary=True).o
        """
        pattern = b"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if is_binary:
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else:  # pragma: no cover
            matched = list(
                filter(
                    lambda x: re.search(pattern, x), self._convert_to_bytes().split()
                )
            )
        self.state = matched
        return self

    @ChepyDecorators.call_stack
    def extract_mac_address(self, is_binary: bool = False) -> ExtractorsT:
        """Extract MAC addresses

        Args:
            is_binary (bool, optional): The state is in binary format. It will then first
                extract the strings from it before matching.

        Returns:
            Chepy: The Chepy object.
        """
        pattern = b"^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$"
        if is_binary:  # pragma: no cover
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else:
            matched = list(
                filter(
                    lambda x: re.search(pattern, x), self._convert_to_bytes().split()
                )
            )
        self.state = matched
        return self

    @ChepyDecorators.call_stack
    def extract_urls(self, is_binary: bool = False) -> ExtractorsT:
        """Extract urls including http, file, ssh and ftp

        Args:
            is_binary (bool, optional): The state is in binary format. It will then first
                extract the strings from it before matching.

        Returns:
            Chepy: The Chepy object.
        """
        pattern = b"(file|ftps?|http[s]?|ssh)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        if is_binary:  # pragma: no cover
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else:
            matched = list(
                filter(
                    lambda x: re.search(pattern, x), self._convert_to_bytes().split()
                )
            )
        self.state = matched
        return self

    @ChepyDecorators.call_stack
    def extract_domains(self, is_binary: bool = False) -> ExtractorsT:
        """Extract domains

        Args:
            is_binary (bool, optional): The state is in binary format. It will then first
                extract the strings from it before matching.

        Returns:
            Chepy: The Chepy object.
        """
        if is_binary:  # pragma: no cover
            matched = list(_pyurlparse(x).netloc for x in self.extract_strings().o)
        else:
            matched = list(
                _pyurlparse(x).netloc
                for x in self._convert_to_bytes().split()
                if x.startswith(b"http")
            )
        self.state = matched
        return self

    @ChepyDecorators.call_stack
    def xpath_selector(self, query: str, namespaces: str = None) -> ExtractorsT:
        """Extract data using valid xpath selectors

        Args:
            query (str): Required. Xpath query
            namespaces (str, optional): Namespace. Applies for XML data. Defaults to None.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("http://example.com")
            >>> c.http_request()
            >>> c.xpath_selector("//title/text()")
            >>> c.get_by_index(0)
            >>> c.o
            "Example Domain"
        """
        self.state = (
            parsel.Selector(self._convert_to_str(), namespaces=namespaces)
            .xpath(query)
            .getall()
        )
        return self

    @ChepyDecorators.call_stack
    def css_selector(self, query: str) -> ExtractorsT:
        """Extract data using valid CSS selectors

        Args:
            query (str): Required. CSS query

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("http://example.com")
            >>> c.http_request()
            >>> c.css_selector("title")
            >>> c.get_by_index(0)
            >>> c.o
            "<title>Example Domain</title>"
        """
        self.state = self._parsel_obj().css(query).getall()
        return self

    @ChepyDecorators.call_stack
    def jpath_selector(self, query: str) -> ExtractorsT:
        """Query JSON with jpath query

        `Reference <https://goessner.net/articles/JsonPath/index.html#e2>`__

        Args:
            query (str): Required. Query. For reference, see the help

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("tests/files/test.json")
            >>> c.load_file()
            >>> c.jpath_selector("[*].name.first")
            >>> c.get_by_index(2)
            >>> c.o
            "Long"
        """
        self.state = list(
            j.value
            for j in jsonpath_rw.parse(query).find(ujson.loads(self._convert_to_str()))
        )
        return self

    @ChepyDecorators.call_stack
    def html_comments(self) -> ExtractorsT:
        """Extract html comments

        Returns:
            Chepy: The Chepy object.
        """
        self.state = list(
            filter(lambda x: x != "", self._parsel_obj().xpath("//comment()").getall())
        )
        return self

    @ChepyDecorators.call_stack
    def javascript_comments(self) -> ExtractorsT:
        """Extract javascript comments

        Some false positives is expected because of inline // comments

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            r"/\*[\w'\s\r\n\*]*\*/|//[\w\s']*|/\*.+?\*/", self._convert_to_str()
        )
        return self

    @ChepyDecorators.call_stack
    def html_tags(self, tag: str) -> ExtractorsT:
        """Extract tags from html along with their attributes

        Args:
            tag (str): A HTML tag

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("http://example.com").http_request().html_tags('p').o
            [
                {'tag': 'p', 'attributes': {}},
                {'tag': 'p', 'attributes': {}},
                {'tag': 'p', 'attributes': {}}
            ]
        """
        tags = []

        for element in self._parsel_obj().xpath("//{}".format(tag)):
            attributes = []
            for index, attribute in enumerate(element.xpath("@*"), start=1):
                attribute_name = element.xpath("name(@*[%d])" % index).extract_first()
                attributes.append((attribute_name, attribute.extract()))
            tags.append({"tag": tag, "attributes": dict(attributes)})

        self.state = tags
        return self

    @ChepyDecorators.call_stack
    def extract_google_api(self) -> ExtractorsT:
        """Extract Goolge api keys

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"AIza[0-9A-Za-z-_]{35}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_google_captcha(self) -> ExtractorsT:
        """Extract Goolge captcha keys

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"6L[0-9A-Za-z-_]{38}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_google_oauth(self) -> ExtractorsT:
        """Extract Goolge oauth keys

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"ya29\.[0-9A-Za-z\-_]+", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_aws_keyid(self) -> ExtractorsT:
        """Extract AWS key ids

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"AKIA[0-9A-Z]{16}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_aws_s3_url(self) -> ExtractorsT:
        """Extract AWS S3 URLs

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            r"s3\.amazonaws.com[/]+|[a-zA-Z0-9_-]*\.s3\.amazonaws.com",
            self._convert_to_str(),
        )
        return self

    @ChepyDecorators.call_stack
    def extract_facebook_access_token(self) -> ExtractorsT:
        """Extract Facebook access tokens

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"EAACEdEose0cBA[0-9A-Za-z]+", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_auth_basic(self) -> ExtractorsT:
        """Extract basic authentication tokens

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            r"[B|b]asic\s*[a-zA-Z0-9=:_\+\/-]+", self._convert_to_str()
        )
        return self

    @ChepyDecorators.call_stack
    def extract_auth_bearer(self) -> ExtractorsT:
        """Extract bearer authentication tokens

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            r"[b|B]earer\s*[a-zA-Z0-9_\-\.=:_\+\/]+", self._convert_to_str()
        )
        return self

    @ChepyDecorators.call_stack
    def extract_mailgun_api(self) -> ExtractorsT:
        """Extract Mailgun API key

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"key-[0-9a-zA-Z]{32}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_twilio_api(self) -> ExtractorsT:
        """Extract Twilio API key

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"SK[0-9a-fA-F]{32}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_twilio_sid(self) -> ExtractorsT:
        """Extract Twilio account or app sid

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"A[C|P][a-zA-Z0-9_\-]{32}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_paypal_bt(self) -> ExtractorsT:
        """Extract Paypal braintree access token

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            r"access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}",
            self._convert_to_str(),
        )
        return self

    @ChepyDecorators.call_stack
    def extract_square_oauth(self) -> ExtractorsT:
        """Extract Square oauth secret token

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"sq0csp-[ 0-9A-Za-z\-_]{43}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_square_access(self) -> ExtractorsT:
        """Extract Square access token

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"sqOatp-[0-9A-Za-z\-_]{22}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_stripe_api(self) -> ExtractorsT:
        """Extract Stripe standard or restricted api token

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(r"[s|r]k_live_[0-9a-zA-Z]{24}", self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def extract_github(self) -> ExtractorsT:
        """Extract Github access token

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            r"[a-zA-Z0-9_-]*:[a-zA-Z0-9_\-]+@github\.com*", self._convert_to_str()
        )
        return self

    @ChepyDecorators.call_stack
    def extract_rsa_private(self) -> ExtractorsT:
        """Extract RSA private key

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            r"-----BEGIN RSA PRIVATE KEY-----", self._convert_to_str()
        )
        return self

    @ChepyDecorators.call_stack
    def extract_dsa_private(self) -> ExtractorsT:
        """Extract DSA private key

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            r"-----BEGIN DSA PRIVATE KEY-----", self._convert_to_str()
        )
        return self

    @ChepyDecorators.call_stack
    def extract_jwt_token(self) -> ExtractorsT:
        """Extract JWT token

        Returns:
            Chepy: The Chepy object.
        """
        self.state = re.findall(
            r"ey[A-Za-z0-9_-]*\.[A-Za-z0-9._-]*|ey[A-Za-z0-9_\/+-]*\.[A-Za-z0-9._\/+-]*",
            self._convert_to_str(),
        )
        return self

    @ChepyDecorators.call_stack
    def extract_base64(self, min: int = 20) -> ExtractorsT:
        """Extract base64 encoded strings

        Args:
            min (int, optional): Minium length to match. Defaults to 20.

        Returns:
            Chepy: The Chepy object.
        """
        found = re.findall("[a-zA-Z0-9+/=]{%s,}" % str(20), self._convert_to_str())
        if len(found) > 1:  # pragma: no cover
            self.state = found
        else:
            self.state = found[0]
        return self
