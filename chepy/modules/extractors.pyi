from ..core import ChepyCore as ChepyCore, ChepyDecorators as ChepyDecorators
from typing import Any, TypeVar

parsel: Any
ExtractorsT = TypeVar('ExtractorsT', bound='Extractors')

class Extractors(ChepyCore):
    def __init__(self, *data: Any) -> None: ...
    state: Any = ...
    def extract_hashes(self) -> ExtractorsT: ...
    def extract_strings(self, length: int=...) -> ExtractorsT: ...
    def extract_ips(self, invalid: bool=..., is_binary: bool=...) -> ExtractorsT: ...
    def extract_email(self, is_binary: bool=...) -> ExtractorsT: ...
    def extract_mac_address(self, is_binary: bool=...) -> ExtractorsT: ...
    def extract_urls(self, is_binary: bool=...) -> ExtractorsT: ...
    def extract_domains(self, is_binary: bool=...) -> ExtractorsT: ...
    def xpath_selector(self, query: str, namespaces: str=...) -> ExtractorsT: ...
    def css_selector(self, query: str) -> ExtractorsT: ...
    def jpath_selector(self, query: str) -> ExtractorsT: ...
    def html_comments(self) -> ExtractorsT: ...
    def javascript_comments(self) -> ExtractorsT: ...
    def html_tags(self, tag: str) -> ExtractorsT: ...
    def extract_google_api(self) -> ExtractorsT: ...
    def extract_google_captcha(self) -> ExtractorsT: ...
    def extract_google_oauth(self) -> ExtractorsT: ...
    def extract_aws_keyid(self) -> ExtractorsT: ...
    def extract_aws_s3_url(self) -> ExtractorsT: ...
    def extract_facebook_access_token(self) -> ExtractorsT: ...
    def extract_auth_basic(self) -> ExtractorsT: ...
    def extract_auth_bearer(self) -> ExtractorsT: ...
    def extract_mailgun_api(self) -> ExtractorsT: ...
    def extract_twilio_api(self) -> ExtractorsT: ...
    def extract_twilio_sid(self) -> ExtractorsT: ...
    def extract_paypal_bt(self) -> ExtractorsT: ...
    def extract_square_oauth(self) -> ExtractorsT: ...
    def extract_square_access(self) -> ExtractorsT: ...
    def extract_stripe_api(self) -> ExtractorsT: ...
    def extract_github(self) -> ExtractorsT: ...
    def extract_rsa_private(self) -> ExtractorsT: ...
    def extract_dsa_private(self) -> ExtractorsT: ...
    def extract_jwt_token(self) -> ExtractorsT: ...
    def extract_base64(self, min: int=...) -> ExtractorsT: ...
