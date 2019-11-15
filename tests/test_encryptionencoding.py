from chepy import Chepy


def test_rot_47():
    assert Chepy("some").rot_47().output == "D@>6"


def test_rotate():
    assert Chepy("some data").rotate(20).output == "migy xunu"


def test_xor_utf():
    assert Chepy("some data").xor("UD", "utf").output.decode() == "&+8!u 404"


def test_xor_base64():
    assert Chepy("&+8!u 404").xor("VUQ=", "base64").output.decode() == "some data"


def test_xor_hex():
    assert Chepy("some data").xor("5544", "hex").output.decode() == "&+8!u 404"


def test_xor_binary():
    assert (
        Chepy("./tests/files/hello")
        .load_file()
        .to_hex()
        .xor("A", "utf")
        .to_hex()
        .o.decode()[0:6]
        == "222727"
    )


def test_jwt_decode():
    assert (
        Chepy(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmF\
            tZSI6IkFtYXppbmcgSGF4eDByIiwiZXhwIjoiMTQ2NjI3MDcyMiIsImFkbWluIjp0\
                cnVlfQ.UL9Pz5HbaMdZCV9cS9OcpccjrlkcmLovL2A2aiKiAOY"
        )
        .jwt_decode()
        .o
        == {
            "payload": {
                "sub": "1234567890",
                "name": "Amazing Haxx0r",
                "exp": "1466270722",
                "admin": True,
            },
            "header": {"alg": "HS256", "typ": "JWT"},
        }
    )


def test_jwt_sign():
    assert (
        Chepy({"some": "payload"}).jwt_sign("secret", "HS512").o.decode()
        == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzb21lIjoicGF5bG9hZCJ9.EgMnzcJYrElON09Bw_OwaqR_Z7Cq30n7cgTZGJqtK1YHfG1cGnGJoJGwOLj6AWg9taOyJN3Dnqd9NXeTCjTCwA"
    )


def test_jwt_verify():
    assert (
        Chepy(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5N\
            iznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg"
        )
        .jwt_verify("secret")
        .o
        == {"some": "payload"}
    )


def test_rc4_encrypt():
    assert Chepy("some data").rc4_encrypt("secret").o == b"9e59bf79a2c0b7d253"
    assert (
        Chepy("some data").rc4_encrypt("736563726574", hex_key=True).o
        == b"9e59bf79a2c0b7d253"
    )


def test_rc4_decrypt():
    assert (
        Chepy("9e59bf79a2c0b7d253").hex_to_str().rc4_decrypt("secret").o == b"some data"
    )
    assert (
        Chepy("9e59bf79a2c0b7d253")
        .hex_to_str()
        .rc4_decrypt("736563726574", hex_key=True)
        .o
        == b"some data"
    )


def test_des_encrypt():
    assert (
        Chepy("some data").des_encrypt("password").o
        == b"1ee5cb52954b211d1acd6e79c598baac"
    )
    assert (
        Chepy("some data").des_encrypt("password", mode="ECB").o
        == b"1ee5cb52954b211da5b1a0072da15156"
    )
    assert (
        Chepy("some data").des_encrypt("password", mode="CTR").o
        == b"0b7399049b0267d93d"
    )
    assert (
        Chepy("some data").des_encrypt("password", mode="OFB").o
        == b"0b7399049b0267d9a9"
    )


def test_triple_des_encrypt():
    assert (
        Chepy("some data").triple_des_encrypt("super secret password !!").o
        == b"f8b27a0d8c837edce87dd13a1ab41f96"
    )
    assert (
        Chepy("some data").triple_des_encrypt("super secret password !!", mode="ECB").o
        == b"f8b27a0d8c837edc8fb00ea85f502fb4"
    )
    assert (
        Chepy("some data").triple_des_encrypt("super secret password !!", mode="CTR").o
        == b"51710aefbd5bbb5b40"
    )
    assert (
        Chepy("some data").triple_des_encrypt("super secret password !!", mode="OFB").o
        == b"51710aefbd5bbb5bf9"
    )


def test_aes_encrypt():
    assert (
        Chepy("some data").aes_encrypt("secret password!").o
        == b"5fb8c186394fc399849b89d3b6605fa3"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!", mode="ECB").o
        == b"5fb8c186394fc399849b89d3b6605fa3"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!", mode="CTR").o
        == b"4ab2b4f72e9d92960b"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!", mode="GCM").o
        == b"97a6227556b2be0763"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!", mode="OFB").o
        == b"4ab2b4f72e9d92960b"
    )


def test_des_decrypt():
    assert (
        Chepy("1ee5cb52954b211d1acd6e79c598baac").hex_to_str().des_decrypt("password").o
        == b"some data"
    )
    assert (
        Chepy("1ee5cb52954b211da5b1a0072da15156")
        .hex_to_str()
        .des_decrypt("password", mode="ECB")
        .o
        == b"some data"
    )
    assert (
        Chepy("0b7399049b0267d93d").hex_to_str().des_decrypt("password", mode="CTR").o
        == b"some data"
    )
    assert (
        Chepy("0b7399049b0267d9a9").hex_to_str().des_decrypt("password", mode="OFB").o
        == b"some data"
    )


def test_triple_des_decrypt():
    assert (
        Chepy("f8b27a0d8c837edce87dd13a1ab41f96")
        .hex_to_str()
        .triple_des_decrypt("super secret password !!")
        .o
        == b"some data"
    )
    assert (
        Chepy("f8b27a0d8c837edc8fb00ea85f502fb4")
        .hex_to_str()
        .triple_des_decrypt("super secret password !!", mode="ECB")
        .o
        == b"some data"
    )
    assert (
        Chepy("51710aefbd5bbb5b40")
        .hex_to_str()
        .triple_des_decrypt("super secret password !!", mode="CTR")
        .o
        == b"some data"
    )
    assert (
        Chepy("51710aefbd5bbb5bf9")
        .hex_to_str()
        .triple_des_decrypt("super secret password !!", mode="OFB")
        .o
        == b"some data"
    )



def test_aes_decrypt():
    assert (
        Chepy("5fb8c186394fc399849b89d3b6605fa3")
        .hex_to_str()
        .aes_decrypt("secret password!")
        .o
        == b"some data"
    )
    assert (
        Chepy("5fb8c186394fc399849b89d3b6605fa3")
        .hex_to_str()
        .aes_decrypt("secret password!", mode="ECB")
        .o
        == b"some data"
    )
    assert (
        Chepy("4ab2b4f72e9d92960b")
        .hex_to_str()
        .aes_decrypt("secret password!", mode="CTR")
        .o
        == b"some data"
    )
    assert (
        Chepy("97a6227556b2be0763")
        .hex_to_str()
        .aes_decrypt("secret password!", mode="GCM")
        .o
        == b"some data"
    )
    assert (
        Chepy("4ab2b4f72e9d92960b")
        .hex_to_str()
        .aes_decrypt("secret password!", mode="OFB")
        .o
        == b"some data"
    )


def test_blowfish_encrypt():
    assert (
        Chepy("some data").blowfish_encrypt("password").o
        == b"d9b0a79853f13960fcee3cae16e27884"
    )
    assert (
        Chepy("some data").blowfish_encrypt("password", mode="ECB").o
        == b"d9b0a79853f139603951bff96c3d0dd5"
    )
    assert (
        Chepy("some data").blowfish_encrypt("password", mode="CTR").o
        == b"82bdcb75a4d655c63a"
    )
    assert (
        Chepy("some data").blowfish_encrypt("password", mode="OFB").o
        == b"82bdcb75a4d655c6f0"
    )



def test_blowfish_decrypt():
    assert (
        Chepy("d9b0a79853f13960fcee3cae16e27884")
        .hex_to_str()
        .blowfish_decrypt("password")
        .o
        == b"some data"
    )
    assert (
        Chepy("d9b0a79853f139603951bff96c3d0dd5")
        .hex_to_str()
        .blowfish_decrypt("password", mode="ECB")
        .o
        == b"some data"
    )
    assert (
        Chepy("82bdcb75a4d655c63a")
        .hex_to_str()
        .blowfish_decrypt("password", mode="CTR")
        .o
        == b"some data"
    )
    assert (
        Chepy("82bdcb75a4d655c6f0")
        .hex_to_str()
        .blowfish_decrypt("password", mode="OFB")
        .o
        == b"some data"
    )
