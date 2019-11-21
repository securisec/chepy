from chepy.extras.bruteforce import *


def test_zip_brute():
    assert (
        zip_password_bruteforce("tests/files/test.zip", "tests/files/wordlist.txt")
        == b"password"
    )

