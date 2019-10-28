from chepy import Chepy


def test_identify_hash():
    assert (
        Chepy("6dcd4ce23d88e2ee9568ba546c007c63d9131c1b").identify_hash()[0]["name"]
        == "SHA-1"
    )


def test_sha1():
    assert Chepy("A").sha1.output == "6dcd4ce23d88e2ee9568ba546c007c63d9131c1b"


def test_sha256():
    assert (
        Chepy("A").sha256.output
        == "559aead08264d5795d3909718cdd05abd49572e84fe55590eef31a88a08fdffd"
    )

