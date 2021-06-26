from chepy import Chepy


def test_rot_47():
    assert Chepy("some").rot_47().output == "D@>6"


def test_rotate():
    assert Chepy("some data").rotate(20).output == "migy xunu"


def test_rotate_bruteforce():
    assert Chepy("uryyb").rotate_bruteforce().o["13"] == "hello"


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
    assert (
        Chepy("./tests/files/hello").load_file().xor(41, "utf").to_hex().o.decode()[0:6]
        == "fbcbd9"
    )
    assert (
        Chepy("./tests/files/hello")
        .xor(key=41, key_type="utf", ascii=True)
        .to_hex()
        .o.decode()[0:6]
        == "1a1e40"
    )


def test_xor_bruteforce():
    assert Chepy(
        b"\x85\x88\x81\x81\x82\xcd\x9a\x82\x9f\x81\x89"
    ).xor_bruteforce().get_by_key("ed").o == bytearray(b"hello world")


def test_jwt_decode():
    assert Chepy(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmF\
            tZSI6IkFtYXppbmcgSGF4eDByIiwiZXhwIjoiMTQ2NjI3MDcyMiIsImFkbWluIjp0\
                cnVlfQ.UL9Pz5HbaMdZCV9cS9OcpccjrlkcmLovL2A2aiKiAOY"
    ).jwt_decode().o == {
        "payload": {
            "sub": "1234567890",
            "name": "Amazing Haxx0r",
            "exp": "1466270722",
            "admin": True,
        },
        "header": {"alg": "HS256", "typ": "JWT"},
    }


def test_jwt_sign():
    assert (
        Chepy({"some": "payload"}).jwt_sign("secret", "HS512").o.decode()
        == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzb21lIjoicGF5bG9hZCJ9.EgMnzcJYrElON09Bw_OwaqR_Z7Cq30n7cgTZGJqtK1YHfG1cGnGJoJGwOLj6AWg9taOyJN3Dnqd9NXeTCjTCwA"
    )
    assert (
        Chepy('{"some": "payload"}').jwt_sign("secret", "HS512").o.decode()
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


def test_jwt_bruteforce():
    assert (
        Chepy(
            b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJoZWxsbyI6IndvcmxkIn0.bqxXg9VwcbXKoiWtp-osd0WKPX307RjcN7EuXbdq-CE"
        )
        .jwt_bruteforce("tests/files/wordlist.txt")
        .get_by_key("secret")
        .o
        == "secret"
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
        Chepy("some data").des_encrypt("70617373776f7264", hex_key=True).to_hex().o
        == b"1ee5cb52954b211d1acd6e79c598baac"
    )
    assert (
        Chepy("some data").des_encrypt("password").to_hex().o
        == b"1ee5cb52954b211d1acd6e79c598baac"
    )
    assert (
        Chepy("some data").des_encrypt("password", mode="ECB").to_hex().o
        == b"1ee5cb52954b211da5b1a0072da15156"
    )
    assert (
        Chepy("some data").des_encrypt("password", mode="CTR").to_hex().o
        == b"0b7399049b0267d93d"
    )
    assert (
        Chepy("some data").des_encrypt("password", mode="OFB").to_hex().o
        == b"0b7399049b0267d9a9"
    )


def test_triple_des_encrypt():
    assert (
        Chepy("some data")
        .triple_des_encrypt(
            "7375706572207365637265742070617373776f7264202121", hex_key=True
        )
        .to_hex()
        .o
        == b"f8b27a0d8c837edce87dd13a1ab41f96"
    )
    assert (
        Chepy("some data").triple_des_encrypt("super secret password !!").to_hex().o
        == b"f8b27a0d8c837edce87dd13a1ab41f96"
    )
    assert (
        Chepy("some data")
        .triple_des_encrypt("super secret password !!", mode="ECB")
        .to_hex()
        .o
        == b"f8b27a0d8c837edc8fb00ea85f502fb4"
    )
    assert (
        Chepy("some data")
        .triple_des_encrypt("super secret password !!", mode="CTR")
        .to_hex()
        .o
        == b"51710aefbd5bbb5b40"
    )
    assert (
        Chepy("some data")
        .triple_des_encrypt("super secret password !!", mode="OFB")
        .to_hex()
        .o
        == b"51710aefbd5bbb5bf9"
    )


def test_aes_encrypt():
    assert (
        Chepy("some data")
        .aes_encrypt("7365637265742070617373776f726421", hex_key=True)
        .to_hex()
        .o
        == b"5fb8c186394fc399849b89d3b6605fa3"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!").to_hex().o
        == b"5fb8c186394fc399849b89d3b6605fa3"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!", mode="ECB").to_hex().o
        == b"5fb8c186394fc399849b89d3b6605fa3"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!", mode="CTR").to_hex().o
        == b"4ab2b4f72e9d92960b"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!", mode="GCM").to_hex().o
        == b"97a6227556b2be0763"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!", mode="OFB").to_hex().o
        == b"4ab2b4f72e9d92960b"
    )


def test_des_decrypt():
    assert (
        Chepy("1ee5cb52954b211d1acd6e79c598baac")
        .hex_to_str()
        .des_decrypt("70617373776f7264", hex_key=True)
        .o
        == b"some data"
    )
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
        .triple_des_decrypt(
            "7375706572207365637265742070617373776f7264202121", hex_key=True
        )
        .o
        == b"some data"
    )
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
        .aes_decrypt("7365637265742070617373776f726421", hex_key=True)
        .o
        == b"some data"
    )
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
        Chepy("some data").blowfish_encrypt("70617373776f7264", hex_key=True).to_hex().o
        == b"d9b0a79853f13960fcee3cae16e27884"
    )
    assert (
        Chepy("some data").blowfish_encrypt("password").to_hex().o
        == b"d9b0a79853f13960fcee3cae16e27884"
    )
    assert (
        Chepy("some data").blowfish_encrypt("password", mode="ECB").to_hex().o
        == b"d9b0a79853f139603951bff96c3d0dd5"
    )
    assert (
        Chepy("some data").blowfish_encrypt("password", mode="CTR").to_hex().o
        == b"82bdcb75a4d655c63a"
    )
    assert (
        Chepy("some data").blowfish_encrypt("password", mode="OFB").to_hex().o
        == b"82bdcb75a4d655c6f0"
    )


def test_blowfish_decrypt():
    assert (
        Chepy("d9b0a79853f13960fcee3cae16e27884")
        .hex_to_str()
        .blowfish_decrypt("70617373776f7264", hex_key=True)
        .o
        == b"some data"
    )
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


def test_vigener_encode():
    assert Chepy("secret").vigenere_encode("secret").o == "KIEIIM"


def test_vigenere_decode():
    assert Chepy("KIEIIM").vigenere_decode("secret").o == "SECRET"


def test_affin_encode():
    assert Chepy("secret").affine_encode().o == "TFDSFU"


def test_affine_decode():
    assert Chepy("TFDSFU").affine_decode().o == "SECRET"


def test_atbash_encode():
    assert Chepy("secret").atbash_encode().o == "hvxivg".upper()


def test_atbash_decode():
    assert Chepy("hvxivg").atbash_decode().o == "secret".upper()


def test_to_morse_code():
    assert (
        Chepy("hello world").to_morse_code(word_delim="/").o
        == ".... . .-.. .-.. --- /.-- --- .-. .-.. -.. /"
    )


def test_from_morse_code():
    assert (
        Chepy(".... . .-.. .-.. --- \n.-- --- .-. .-.. -..").from_morse_code().o
        == "HELLO WORLD"
    )


def test_rsa_encrypt_decrypt():
    assert (
        Chepy("lol")
        .rsa_encrypt("tests/files/public.pem")
        .rsa_decrypt("tests/files/private.pem")
        .o
        == b"lol"
    )


def test_rsa_sign():
    assert (
        Chepy("lol").rsa_sign("tests/files/private.pem").to_hex().o
        == b"ae12fa91f12af7e1c04e7893ce43fc76195d30203ad0ab88fac3631feb026ee8832d57584a977fe9f70139d8dd7c74b904643ab11493935c642e563752325c1ecde98a29bfaaa714e513d7c3548e9fbea6f2f2705eec3567f4ba868b3ca16f8ede4155e71b854042810bb836dda031c2e540175f4573103c065311d38b7246a6"
    )
