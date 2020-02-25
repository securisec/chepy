from pathlib import Path
from chepy import Chepy


def test_extract_strings():
    assert len(Chepy("tests/files/hello").load_file().extract_strings().o) == 29


def test_extract_hashes():
    assert Chepy(
        ["60b725f10c9c85c70d97880dfe8191b3", "3f786850e387550fdab836ed7e6dc881de23001b"]
    ).extract_hashes().o == {
        "md5": [b"60b725f10c9c85c70d97880dfe8191b3"],
        "sha1": [b"3f786850e387550fdab836ed7e6dc881de23001b"],
        "sha256": [],
        "sha512": [],
    }


def test_extract_ips():
    assert len(Chepy("127.0.0.1\n::80").extract_ips().o) == 2


def test_extract_email():
    assert (
        len(Chepy("tests/files/test.der").load_file().extract_email(is_binary=True).o)
        == 2
    )


def test_extract_mac_address():
    assert (
        len(
            Chepy("01:23:45:67:89:ab | 127.0.0.1 | fE:dC:bA:98:76:54")
            .extract_mac_address()
            .o
        )
        == 2
    )


def test_extract_urls():
    assert (
        len(
            Chepy(
                "https://google.com, https://google.com/app&lo=lol, \
                http://localhost:800, file://test, ftp://test,]"
            )
            .extract_urls()
            .o
        )
        == 5
    )


def test_extract_domains():
    assert (
        len(
            Chepy(
                "https://google.com, https://google.com/app&lo=lol, \
                http://localhost:800, file://test, ftp://test,]"
            )
            .extract_domains()
            .o
        )
        == 3
    )


def test_xpath():
    assert (
        Chepy("tests/files/test.html")
        .load_file()
        .xpath_selector("//title/text()")
        .get_by_index(0)
        .o
        == "Example Domain"
    )


def test_css():
    assert (
        Chepy("http://example.com")
        .http_request()
        .css_selector("title")
        .get_by_index(0)
        .o
        == "<title>Example Domain</title>"
    )


def test_jpath():
    assert (
        Chepy("tests/files/test.json")
        .load_file()
        .jpath_selector("[*].name.first")
        .get_by_index(2)
        .o
        == "Long"
    )


def test_html_comments():
    assert len(Chepy("tests/files/test.html").load_file().html_comments().o) == 3


def test_js_comments():
    assert len(Chepy("tests/files/test.js").load_file().javascript_comments().o) == 3


def test_html_tag():
    assert Chepy("tests/files/test.html").load_file().html_tags("p").o == [
        {"tag": "p", "attributes": {"someval": "someval", "ano-ther": "another"}},
        {"tag": "p", "attributes": {}},
    ]


def test_extract_basicauth():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_auth_basic().o)
        == 1
    )


def test_extract_bearerauth():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_auth_bearer().o)
        == 1
    )


def test_extract_awskeyid():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_aws_keyid().o)
        == 1
    )


def test_extract_s3url():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_aws_s3_url().o)
        == 1
    )


def test_extract_dsaprivate():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_dsa_private().o)
        == 1
    )


def test_extract_fbaccess():
    assert (
        len(
            Chepy("tests/files/fake_secrets.txt")
            .read_file()
            .extract_facebook_access_token()
            .o
        )
        == 1
    )


def test_extract_githubtoken():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_github().o) == 1
    )


def test_extract_googleapi():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_google_api().o)
        == 1
    )


def test_extract_googlecaptcha():
    assert (
        len(
            Chepy("tests/files/fake_secrets.txt").read_file().extract_google_captcha().o
        )
        == 1
    )


def test_extract_googleoauth():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_google_oauth().o)
        == 1
    )


def test_extract_jwttoken():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_jwt_token().o)
        == 1
    )


def test_extract_mailgun():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_mailgun_api().o)
        == 1
    )


def test_extract_paypal():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_paypal_bt().o)
        == 1
    )


def test_extract_rsaprivate():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_rsa_private().o)
        == 1
    )


def test_extract_squareaccess():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_square_access().o)
        == 1
    )


def test_extract_squareoauth():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_square_oauth().o)
        == 1
    )


def test_extract_stripeapi():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_stripe_api().o)
        == 2
    )


def test_extract_twilioapi():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_twilio_api().o)
        == 1
    )


def test_extract_twiliosid():
    assert (
        len(Chepy("tests/files/fake_secrets.txt").read_file().extract_twilio_sid().o)
        == 2
    )

