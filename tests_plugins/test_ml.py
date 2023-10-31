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


def test_ml_magic():
    assert (
        Chepy("Ca6wMuk9H4Y3rYb8uMQordMrH6JbvsaWx2Ua7dNQvF1tujWPvi2AEijEKsD6Mpe7Ld37T1y")
        .ml_magic()
        .o[-1]
        == b"hello world"
    )

    assert (
        Chepy(
            "KZWTCNCVGFEXSUTOJJHFM3LIKVMWWZDPKZLFS522I44VOYSHPB5FSVLDGVLGWMKXKNWGYWSNI5UFAVSHPBQWGMKOONREM4COKJWHATKXK52GCWKWLJLVE3SGLBREQQTTLFMHAV2NNRNHCU3KKJMGEVS2JFKWY2DXMFDEU42XNM4VMYSYKIZVMMC2MFJDC4CFKVWXATSSIZNDMV2WKJHWIMLMK5JW4SSUMJDEUV2ZK52EOTJROBCVE3DQNRLFIRS2K5VWI43BI5LHEV3MNBLVEM3IOZKWURTLKIYXARTBIZNGSUSWOBMFOVSSI5SDERSHMEZWIWDCLBJFSVTKIEYVEMKZPFGVIUTIKIYVUMC2KVLGWVRSJJDWGRSSK5QWWWT2KZVEM22XK5DEQYKFGVHGERLQMFLDCWSTKMZEK52NJBUFOYJSKJKFM23EGRKWYWSXKVMGIUCVKQYDS==="
        )
        .ml_magic(10)
        .o[-1]
        == b"InfoSeCon2023{1af5856c70878f8566085bc13849ef4d}"
    )
