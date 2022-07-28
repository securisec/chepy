from chepy.extras.crypto import one_time_pad_crib


def test_one_time_pad_crib():
    assert (
        one_time_pad_crib(
            "51060328ac104b70881b267fb254d7914948e697aff2ce1c07c91c51b4ff2a172b6477c7e006",
            "560b032eb6481826df19237ce403d7c34c4db194fff59a4f559a4d09b6fa72157a642797e31a",
            b"a" * 38,
        )[0]
        == "flag{9276cdb76a3dd6b1f523209cd9c0a11b}"
    )
