from chepy import Chepy


def test_protobuf_dict():
    c = Chepy("tests/files/pbuf").load_file()
    assert c.protobuf_decode_dict().o["1"] == 1617862179230365600


def test_protobuf_json():
    c = Chepy("tests/files/pbuf").load_file()
    assert c.protobuf_decode_json(True).json_to_dict().o["1"] == "1617862179230365600"
