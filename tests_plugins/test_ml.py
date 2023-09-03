from chepy import Chepy


def test_ml_detect():
    data = "04224d184070df280000806147567362473867643239796247516761534268625342684948526c633351675a47463059513d3d00000000"
    assert (
        Chepy("https%3A%2F%2Fwww.pennington.com%2Fcategories%2Fwp-content")
        .ml_detect()
        .o.get("to_url_encode")
        != None
    )
    assert Chepy(data).ml_detect().o.get("to_hex") != None
    assert Chepy(data).from_hex().ml_detect().o.get("lz4_compress") != None
    assert (
        Chepy(data).from_hex().lz4_decompress().ml_detect().o.get("to_base64") != None
    )
    assert (
        Chepy(data).from_hex().lz4_decompress().from_base64().o
        == b"hello world i am a test data"
    )
