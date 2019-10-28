from chepy import Chepy


def test_identify_hash():
    assert (
        Chepy("6dcd4ce23d88e2ee9568ba546c007c63d9131c1b").identify_hash()[0]["name"]
        == "SHA-1"
    )

