from chepy import Chepy


def test_ml_detect():
    assert (
        Chepy("https%3A%2F%2Fwww.pennington.com%2Fcategories%2Fwp-content")
        .ml_detect()
        .o.get("from_url_encode")
        != None
    )
    data = "5ZXN4aSn4N2ZVzGA6Q7NbqCRJa2XBt2CEKAvgDUoQj8x9vBJqcrk5fBKZh5XqdAoKnyXMeNmE21QQAqZcKZPamT8he6s8nYRU1unmSb2eAmnnBv8NWSs9f6BgsJ3DGPpdbPm8b9kDSMDTLfZ1"
    assert Chepy(data).ml_detect().o.get("from_base58") != None
    assert Chepy(data).from_base58().ml_detect().o.get("from_hex") != None
    assert (
        Chepy(data).from_base58().from_hex().ml_detect().o.get("lzma_decompress")
        != None
    )


# def test_ml_magic():
#     assert (
#         Chepy("Ca6wMuk9H4Y3rYb8uMQordMrH6JbvsaWx2Ua7dNQvF1tujWPvi2AEijEKsD6Mpe7Ld37T1y")
#         .ml_magic()
#         .o[-1]["out"]
#         == b"hello world"
#     )
