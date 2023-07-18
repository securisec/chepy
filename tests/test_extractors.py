from chepy import Chepy


def test_extract_strings():
    assert (
        Chepy("tests/files/hello").load_file().extract_strings().o.splitlines()[0]
        == b"__PAGEZERO"
    )


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


def test_js_comments():
    assert len(Chepy("tests/files/test.js").load_file().javascript_comments().o) == 3


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


def test_extract_b64():
    data = """
    when an unknown printer took a galley of type c2VjdXJpc2VjLnRlc3QuZGF0YQo= and scrambled it to make a type specimen book. 
    """
    assert Chepy(data).extract_base64().o == b"c2VjdXJpc2VjLnRlc3QuZGF0YQo="


def test_find_longest_continious_pattern():
    str1 = "Helhello worldlo World"
    str2 = "hello world"
    assert Chepy(str1).find_longest_continious_pattern(str2).o == b"hello world"
    str1 = b"Helhello worldlo World"
    str2 = b"hello world"
    assert Chepy(str1).find_longest_continious_pattern(str2).o == b"hello world"


def test_find_continuous_patterns():
    str1 = "Helhello worldlo World"
    str2 = "hello world"
    assert len(Chepy(str1).find_continuous_patterns(str2, 3).o) == 73
    str1 = b"Helhello worldlo World"
    str2 = b"hello world"
    assert len(Chepy(str1).find_continuous_patterns(str2, 3).o) == 73


def test_zero_with_chars_tags():
    assert (
        Chepy("this 󠁮󠁩󠁣is 󠁣󠁻󠀰just 󠁲󠁟󠀱a 󠀵󠁟󠀱simple 󠀷󠁽text file")
        .extract_zero_width_chars_tags()
        .o
        == b"nicc{0r_15_17}"
    )


def test_decode_zero_width():
    assert (
        Chepy(
            "e2808be2808be2808be2808befbbbfe280ace2808b68656c6c6fe2808be2808be2808be2808befbbbfe2808be2808ce2808be2808be2808be2808be280acefbbbfefbbbfe2808be2808be2808be2808befbbbfe2808defbbbfe2808be2808be2808be2808befbbbfe2808be2808ce2808be2808be2808be2808befbbbfe280ace2808c"
        )
        .from_hex()
        .decode_zero_width("\u200B\u200c\u200d\u202c\ufeff")
        .o["hidden"]
        == "secret"
    )
    assert (
        Chepy(
            "e2808ce2808ce2808ce2808ce2808defbbbfe2808cefbbbfe2808ce2808ce2808ce2808ce2808de280ace2808de2808de2808ce2808ce2808ce2808ce2808de280ace2808cefbbbfe2808ce2808ce2808ce2808ce2808defbbbfe2808ce280ac68656c6c6fe2808ce2808ce2808ce2808ce2808de280ace2808de2808de2808ce2808ce2808ce2808ce2808defbbbfe2808de2808c"
        )
        .from_hex()
        .decode_zero_width("\u200c\u200d\u202c\ufeff")
        .o["hidden"]
        == "secret"
    )
    assert (
        Chepy(
            "e2808be2808be2808ce2808ce280ace2808be2808be2808ce2808be2808ce2808be2808be2808befbbbfefbbbf68656c6c6fe2808be2808be2808ce2808ce280aae2808be2808be2808ce2808be2808ce2808be2808be2808ce2808ce280ad"
        )
        .from_hex()
        .decode_zero_width(
            "\u200B\u200C\u200D\u200E\u202A\u202C\u202D\u2062\u2063\ufeff"
        )
        .o["hidden"]
        == "secret"
    )
