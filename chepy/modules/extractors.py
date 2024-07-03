import math
from binascii import unhexlify
import base64
from typing import TypeVar, Union, List
from urllib.parse import urlparse as _pyurlparse
import lazy_import

import regex as re
import re as old_re

parsel = lazy_import.lazy_module("parsel")

from ..core import ChepyCore, ChepyDecorators

ExtractorsT = TypeVar("ExtractorsT", bound="Extractors")

_zw_chars = []
_zw_codelengthText = 0
_zw_radix = 0


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
        # TODO make this more efficient. because at the moment, we are compiling and running this 4 separate times.
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
    def extract_strings(
        self, length: int = 4, join_by: Union[str, bytes] = "\n"
    ) -> ExtractorsT:
        """Extract strings from state

        Args:
            length (int, optional): Min length of string. Defaults to 4.
            join_by (str, optional): String to join by. Defaults to newline.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("tests/files/hello").load_file().extract_strings().o
            __PAGEZERO'
            __TEXT'
            __text'
            __TEXT'
            __stubs'
            __TEXT'
            ...
        """
        pattern = b"[^\x00-\x1f\x7f-\xff]{" + str(length).encode() + b",}"
        matches = re.findall(pattern, self._convert_to_bytes())
        self.state = self._str_to_bytes(join_by).join([m for m in matches])
        return self

    @ChepyDecorators.call_stack
    def extract_ips(self, is_binary: bool = False) -> ExtractorsT:
        """Extract ipv4 and ipv6 addresses

        Args:
            is_binary (bool, optional): The state is in binary format. It will then first
                extract the strings from it before matching.

        Returns:
            Chepy: The Chepy object.
        """
        pattern = r"((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))"
        if is_binary:  # pragma: no cover
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else:
            matched = list(
                filter(
                    lambda x: re.search(pattern.encode(), x),
                    self._convert_to_bytes().split(),
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
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if is_binary:
            matched = list(
                filter(
                    lambda x: re.search(pattern.encode(), x),
                    self.extract_strings().o.splitlines(),
                )
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
        pattern = r"(file|ftps?|http[s]?|ssh)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        if is_binary:  # pragma: no cover
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else:
            matched = list(
                filter(
                    lambda x: re.search(pattern.encode(), x),
                    self._convert_to_bytes().split(),
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
            min (int, optional): Minimum length to match. Defaults to 20.

        Returns:
            Chepy: The Chepy object.
        """
        found = re.findall("[a-zA-Z0-9+/=]{%s,}" % str(20), self._convert_to_str())
        if len(found) > 1:  # pragma: no cover
            self.state = found
        else:
            self.state = found[0]
        return self

    @ChepyDecorators.call_stack
    def find_continuous_patterns(
        self, str2: Union[str, bytes], min_value: int = 10
    ) -> ExtractorsT:
        """Find continius patterns between the state as a string and the provided str2

        Args:
            str2 (Union[str, bytes]): String to find matches against
            min_value (int, optional): Minimum value of continuous matches. Defaults to 10.

        Returns:
            Chepy: The Chepy object.
        """
        str1 = self._convert_to_bytes()
        if isinstance(str2, str):
            str2 = str2.encode()
        combined_data = str1 + str2
        data_length = len(combined_data)
        patterns = []

        for length in range(1, data_length + 1):
            for start in range(data_length - length + 1):
                pattern = combined_data[start : start + length]

                if pattern in str1 and pattern in str2 and len(pattern) > min_value:
                    patterns.append(pattern)

        self.state = patterns
        return self

    @ChepyDecorators.call_stack
    def find_longest_continious_pattern(self, str2: str) -> ExtractorsT:
        """Find longest continuous pattern

        Args:
            str2 (Union[str, bytes]): String to find match against

        Returns:
            Chepy: The Chepy object.
        """
        str1 = self._convert_to_bytes()
        if isinstance(str2, str):
            str2 = str2.encode()
        combined_data = str1 + str2
        data_length = len(combined_data)
        matches = []

        for length in range(1, data_length + 1):
            for start in range(data_length - length + 1):
                pattern = combined_data[start : start + length]

                if (
                    pattern in str1
                    and pattern in str2
                    and len(pattern) > len(matches[-1:])
                ):
                    matches.append(pattern)

        self.state = max(matches, key=len) if matches else ""
        return self

    @ChepyDecorators.call_stack
    def extract_zero_width_chars_tags(self) -> ExtractorsT:
        """Extract zero width characters between U+E0000 to U+E007F. Implements
        https://www.irongeek.com/i.php?page=security/unicode-steganography-homoglyph-encoder

        Returns:
            Chepy: The Chepy object.
        """
        input_string = self._convert_to_str()
        extracted_characters = []

        for char in input_string:
            if "\U000e0000" <= char <= "\U000e007f":
                extracted_characters.append(char)

        self.state = unhexlify(
            b"".join(
                [bytes(x.encode("unicode_escape"))[-2:] for x in extracted_characters]
            )
        )
        return self

    @ChepyDecorators.call_stack
    def decode_zero_width(
        self, _zw_chars: str = "\u200c\u200d\u202c\ufeff"
    ) -> ExtractorsT:
        """Extract zero with characters. Decode implementation of
        https://330k.github.io/misc_tools/unicode_steganography.html

        Args:
            chars (str, optional): Characters for stego. Defaults to '\u200c\u200d\u202c\ufeff'.

        Returns:
            Chepy: The Chepy object.
        """

        def set_use_chars(newchars):
            global _zw_chars, _zw_radix, _zw_codelengthText
            if len(newchars) >= 2:
                _zw_chars = list(newchars)
                _zw_radix = len(_zw_chars)
                _zw_codelengthText = math.ceil(math.log(65536) / math.log(_zw_radix))
            return None

        def split_zerowidth_characters(str1):
            result = {}
            result["originalText"] = old_re.sub(
                "[" + "".join(_zw_chars) + "]", "", str1
            )
            result["hiddenText"] = old_re.sub("[^" + "".join(_zw_chars) + "]", "", str1)
            return result

        def decode_from_zero_width_characters_text(str1):
            r = str1
            result = []
            for i in range(_zw_radix):
                r = r.replace(_zw_chars[i], str(i))
            for i in range(0, len(r), _zw_codelengthText):
                result.append(chr(int(r[i : i + _zw_codelengthText], _zw_radix)))
            return "".join(result)

        def decodeText(text):
            split = split_zerowidth_characters(text)
            return {
                # 'originalText': split['originalText'],
                "hidden": decode_from_zero_width_characters_text(
                    split["hiddenText"]
                )  # , codelengthText)
            }

        set_use_chars(_zw_chars)
        self.state = decodeText(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def xpath_selector(self, query: str, namespaces: str = None):
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
    def css_selector(self, query: str):
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
    def extract_html_tags(self, tags: List[str]):
        """Extract tags from html along with their attributes

        Args:
            tag (str): A HTML tag

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("http://example.com").http_request().html_tags(['p']).o
            [
                {'tag': 'p', 'attributes': {}},
                {'tag': 'p', 'attributes': {}},
                {'tag': 'p', 'attributes': {}}
            ]
        """
        hold = []

        for tag in tags:
            for element in self._parsel_obj().xpath("//{}".format(tag)):
                attributes = []
                for index, attribute in enumerate(element.xpath("@*"), start=1):
                    attribute_name = element.xpath(
                        "name(@*[%d])" % index
                    ).extract_first()
                    attributes.append((attribute_name, attribute.extract()))
                hold.append({"tag": tag, "attributes": dict(attributes)})

        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def extract_html_comments(self):
        """Extract html comments

        Returns:
            Chepy: The Chepy object.
        """
        self.state = list(
            filter(lambda x: x != "", self._parsel_obj().xpath("//comment()").getall())
        )
        return self

    @ChepyDecorators.call_stack
    def aws_account_id_from_access_key(self):
        """Extract AWS account id from access key

        Returns:
            Chepy: The Chepy object. 
        """
        trimmed_AWSKeyID = self._convert_to_str()[4:]
        x = base64.b32decode(trimmed_AWSKeyID)
        y = x[0:6]
        z = int.from_bytes(y, byteorder='big', signed=False)
        mask = int.from_bytes(unhexlify(b'7fffffffff80'), byteorder='big', signed=False)
        
        self.state = (z & mask)>>7
        return self
