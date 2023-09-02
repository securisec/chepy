from chepy import Chepy
from binascii import hexlify, unhexlify
from base64 import b64encode

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAh/1QrTsA41NV3SPvYg087PpcWlG90Lhsm3cD/Nwph6DhDqeZ
l+ZyWaA8waOutILBRj1i3oJ9vg36JknyZFDYMglYnK47nKyMHBiWmkHA9124IaLw
b1H1Dh46GslE6/3n1HxldttgDPbkci2zSIi66FqIpJAQEKrAS5wBsELR3VQEgVFm
symTBsdSAWaGOHFgmebWGjW3BiG0jXPcNa3RQI78DuQEDKEGpifKGAmJKXZoxiwM
/Gn8GgJB0Vg63R1Bk/mK4XANqWsqQcclhxt3pPy0H7I4jJfNeIvkFO45oSEctI3Y
bBVtfbLO1/Yb+eofQmyPlRe6yOnocbhJPCdBTwIDAQABAoIBAAbG0E45n6iJtBXX
icEkm2chw21ldQ82yYQRG7vuNWGYBO8ShLG69EgpbIL9HE0hgO52S6bT8N6CMCIt
UtdokfAjDW04CiobYnCvUaib4zj7IhxcVB1FWRqxgJVqIeBICv/zN6ktyG0M9phb
/6Wl2U6P3bmkS4X7xFEK6VNLw80teo1euCARNECallmg43thnlqGazLrKj5N0N+k
cvy4GezYFNG7UGkSOb35KEvDOhB5kIsBIbkVnt0luFPmGD/M69x32xsyUlCXNPov
bgAGNr2HTye8kj11IXd84d2WGA0R2sKrQ+Ae8ivk8aCgQ07HB3/Kuc3aXBde6JV8
4mn5ZU0CgYEAu6hkCKCf3M7u0TCV2c2tgELRIc5Z8zZ2/OR8Y98QCLwJF8XrlgUB
uLNna/Wyk1goch8/9dtdeOQCzBHmlCS+oKRRd8nxHQKbbnjX5K6AZF9l5q4BF1Pq
yMEszN25QMnIbeHxjlXPntcgaOcRxce19pdc0iXVKIKpaCfjAhk23RsCgYEAuYPR
BItwCn/lcNIhBmJyvXWpHskDt3e2LJdROfsoUlOv67G5g0gf2SYJpt7svvGXC5N3
7blACw+y+AteQHjcznmMiq49ibkMQZ0Vi0dMTSeq15rQf+XiAEqK3lJsbvHtWEFN
82mgIC+fg2i94T0w1POUCYeMGmOYT8L/DY8aM90CgYAlEcSA98ncgnwmkqRnW/vU
BF7vgKXAJ5glqLTxvZSbRRm+ungpMGAArl/VsblO5fFHaejmlijGwrPSwA5+YSvO
6+az9Q5OHr+5eOGc6OOv8DBe+yx4ATm14oMJDRuVMscG/cULyuOyiuh6EHswSJ0n
Uwsg8BxFXlo8mvR666Qs1QKBgCNEfvj5NSyZ0dmX6PVYw+1mr+cNWeqIFJb3kVaP
e8Pi6v/IwrbFgGB8zbruiF1oekmWGGeWHym7K0/igWGKWJfcHa7DnylOh5j1rwHS
ZRwJ3X2tjdOytTtO8IWBb+HLlk5/47zRqMJVq2KFCAwI4P6q68q//Q+LPYp0TJ6c
ROP1AoGAfU3LGhjeOTdEN2GE8vG+y4r1j1z1h2UZYMe0si9sTf96Xgh+MaXZpj62
QSlrCXrwKkfREh/JySvSbdZIKEfOqF0kZLTuHIUUjkuIm6Dei8/BA4s6U8F7ot1g
ueXbG9F+jRfRvGaz8fMuoZAT7F72ptZO3HMzHhZcjrHMau1rfVI=
-----END RSA PRIVATE KEY-----
"""


def test_rot_47():
    assert Chepy("some").rot_47().out == b"D@>6"


def test_rot_47_bruteforce():
    c = Chepy("96==@").rot_47_bruteforce().o
    assert c["1"] == b":7>>A"
    assert c["47"] == b"hello"


def test_rot_8000():
    assert Chepy("籯籵籪籰粄类簹籽籽簼籷籽簹籽籱簼籬簹类簼粆").rot_8000().o == b"flag{r0tt3nt0th3c0r3}"


def test_rotate():
    assert Chepy("some data").rotate(20).out == b"migy xunu"


def test_rotate_bruteforce():
    assert Chepy("uryyb").rotate_bruteforce().o["13"] == b"hello"


def test_xor_utf():
    assert Chepy("some data").xor("UD", "utf").o == b"&+8!u 404"


def test_xor_base64():
    assert Chepy("&+8!u 404").xor("VUQ=", "base64").o == b"some data"


def test_xor_hex():
    assert Chepy("some data").xor("5544", "hex").o == b"&+8!u 404"


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
        Chepy("./tests/files/hello").load_file().xor(41, "utf").to_hex().o[0:6]
        == b"fbcbd9"
    )
    assert (
        Chepy("./tests/files/hello").xor(key=41, key_type="utf").to_hex().o[0:6]
        == b"1a1e40"
    )


def test_xor_decimal():
    assert Chepy("kfool").xor(3, "decimal").o == b"hello"


def test_xor_bytearray():
    flag = bytearray(
        [
            212,
            240,
            205,
            31,
            239,
            85,
            80,
            104,
            31,
            167,  #
            180,
            136,
            232,
            240,
            216,
            11,
            195,
            144,
            227,
            19,  #
            239,
            115,
            81,
            3,
            6,
            166,
            183,
            209,
            244,
            241,  #
            245,
            80,
            168,
            210,
            191,
            7,
            166,
        ]
    )  #

    key = bytearray(
        [156, 164, 143, 100, 219, 10, 34, 92, 113, 212, 132, 229, 159, 196, 170, 56]
    )

    assert Chepy(flag).xor(key).o == b"HTB{4_r4ns0mw4r3_4lw4ys_wr34k5_h4v0c}"


def test_xor_bruteforce():
    assert Chepy(
        b"\x85\x88\x81\x81\x82\xcd\x9a\x82\x9f\x81\x89"
    ).xor_bruteforce().get_by_key("ed").o == bytearray(b"hello world")
    assert (
        len(
            Chepy(b"\x85\x88\x81\x81\x82\xcd\x9a\x82\x9f\x81\x89")
            .xor_bruteforce(crib="hell")
            .o.keys()
        )
        == 1
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
        Chepy({"some": "payload"}).jwt_sign("secret", "HS512").o
        == b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzb21lIjoicGF5bG9hZCJ9.EgMnzcJYrElON09Bw_OwaqR_Z7Cq30n7cgTZGJqtK1YHfG1cGnGJoJGwOLj6AWg9taOyJN3Dnqd9NXeTCjTCwA"
    )
    assert (
        Chepy('{"some": "payload"}').jwt_sign("secret", "HS512").o
        == b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzb21lIjoicGF5bG9hZCJ9.EgMnzcJYrElON09Bw_OwaqR_Z7Cq30n7cgTZGJqtK1YHfG1cGnGJoJGwOLj6AWg9taOyJN3Dnqd9NXeTCjTCwA"
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


def test_jwt_non_alg():
    assert (
        Chepy(
            {
                "sub": "administrator",
            }
        )
        .jwt_token_generate_none_alg()
        .o
        == b"eyJhbGciOiAibm9uZSJ9.eyJzdWIiOiAiYWRtaW5pc3RyYXRvciJ9."
    )


def test_rc4_encrypt():
    msg = "some data"
    res = b"9e59bf79a2c0b7d253"
    key = "secret"
    bkey = b"secret"
    assert Chepy(msg).rc4_encrypt(hexlify(bkey)).o == res
    assert Chepy(msg).rc4_encrypt(key, key_format="utf8").o == res
    assert Chepy(msg).rc4_encrypt(b64encode(bkey), key_format="base64").o == res
    assert (
        Chepy(msg).rc4_encrypt(key, key_format="utf-16-be").o == b"3e2a088355ca43b073"
    )
    assert (
        Chepy(msg).rc4_encrypt(key, key_format="utf-16-le").o == b"19bc2ad03cf4e4fbc0"
    )


def test_rc4_decrypt():
    key = b"secret"
    out = b"some data"
    assert Chepy(unhexlify("9e59bf79a2c0b7d253")).rc4_decrypt(hexlify(key)).o == out
    assert (
        Chepy(unhexlify("9e59bf79a2c0b7d253"))
        .rc4_decrypt(key.decode(), key_format="utf8")
        .o
        == out
    )
    assert (
        Chepy(unhexlify("9e59bf79a2c0b7d253"))
        .rc4_decrypt(b64encode(key), key_format="base64")
        .o
        == out
    )
    assert (
        Chepy(unhexlify("3e2a088355ca43b073"))
        .rc4_decrypt(key, key_format="utf-16-be")
        .o
        == out
    )
    assert (
        Chepy(unhexlify("19bc2ad03cf4e4fbc0"))
        .rc4_decrypt(key, key_format="utf-16-le")
        .o
        == out
    )


def test_des_encrypt():
    assert (
        Chepy("some data").des_encrypt("70617373776f7264").to_hex().o
        == b"1ee5cb52954b211d1acd6e79c598baac"
    )
    assert (
        Chepy("some data").des_encrypt("password", key_format="utf-8").to_hex().o
        == b"1ee5cb52954b211d1acd6e79c598baac"
    )
    assert (
        Chepy("some data")
        .des_encrypt("password", mode="ECB", key_format="utf8")
        .to_hex()
        .o
        == b"1ee5cb52954b211da5b1a0072da15156"
    )
    assert (
        Chepy("some data")
        .des_encrypt("password", mode="CTR", key_format="utf8")
        .to_hex()
        .o
        == b"0b7399049b0267d93d"
    )
    assert (
        Chepy("some data")
        .des_encrypt("password", mode="OFB", key_format="utf8")
        .to_hex()
        .o
        == b"0b7399049b0267d9a9"
    )


def test_triple_des_encrypt():
    assert (
        Chepy("some data")
        .triple_des_encrypt("7375706572207365637265742070617373776f7264202121")
        .to_hex()
        .o
        == b"f8b27a0d8c837edce87dd13a1ab41f96"
    )
    assert (
        Chepy("some data")
        .triple_des_encrypt("super secret password !!", key_format="utf8")
        .to_hex()
        .o
        == b"f8b27a0d8c837edce87dd13a1ab41f96"
    )
    assert (
        Chepy("some data")
        .triple_des_encrypt("super secret password !!", mode="ECB", key_format="utf8")
        .to_hex()
        .o
        == b"f8b27a0d8c837edc8fb00ea85f502fb4"
    )
    assert (
        Chepy("some data")
        .triple_des_encrypt("super secret password !!", mode="CTR", key_format="utf8")
        .to_hex()
        .o
        == b"51710aefbd5bbb5b40"
    )
    assert (
        Chepy("some data")
        .triple_des_encrypt("super secret password !!", mode="OFB", key_format="utf8")
        .to_hex()
        .o
        == b"51710aefbd5bbb5bf9"
    )


def test_key_formats():
    key = b"secret password!"
    data = b"some data"
    res = b"5fb8c186394fc399849b89d3b6605fa3"
    assert Chepy(data).aes_encrypt(key, key_format="utf8").to_hex().o == res
    assert Chepy(data).aes_encrypt(hexlify(key), key_format="hex").to_hex().o == res
    assert (
        Chepy(data).aes_encrypt(b64encode(key), key_format="base64").to_hex().o == res
    )
    assert (
        Chepy(data)
        .aes_encrypt(key.decode().encode("latin-1"), key_format="latin-1")
        .to_hex()
        .o
        == res
    )


def test_iv_formats():
    key = hexlify(b"secret password!")
    iv = b"af7d90ad2278c6bde804e90faf92b109"
    data = b"some data"
    res = b"5d2ae9d06625368fab0fda51ed325096"
    assert Chepy(data).aes_encrypt(key, iv, iv_format="hex").to_hex().o == res
    # assert Chepy(data).aes_encrypt(key, iv, iv_format='utf8').to_hex().o == res
    # assert Chepy(data).aes_encrypt(key, iv, iv_format='base64').to_hex().o == res
    # assert Chepy(data).aes_encrypt(key, iv, iv_format='latin-1').to_hex().o == res
    # TODO
    pass


def test_aes_encrypt():
    assert (
        Chepy("some data").aes_encrypt("7365637265742070617373776f726421").to_hex().o
        == b"5fb8c186394fc399849b89d3b6605fa3"
    )
    assert (
        Chepy("some data").aes_encrypt("secret password!", key_format="utf8").to_hex().o
        == b"5fb8c186394fc399849b89d3b6605fa3"
    )
    assert (
        Chepy("some data")
        .aes_encrypt("secret password!", mode="ECB", key_format="utf8")
        .to_hex()
        .o
        == b"5fb8c186394fc399849b89d3b6605fa3"
    )
    assert (
        Chepy("some data")
        .aes_encrypt("secret password!", mode="CFB", key_format="utf8")
        .to_hex()
        .o
        == b"4ab2b4f72e9d92960b"
    )
    assert (
        Chepy("some data")
        .aes_encrypt("secret password!", mode="CTR", key_format="utf8")
        .to_hex()
        .o
        == b"4ab2b4f72e9d92960b"
    )
    assert (
        Chepy("some data")
        .aes_encrypt("secret password!", mode="GCM", key_format="utf8")
        .to_hex()
        .o
        == b"97a6227556b2be0763"
    )
    assert (
        Chepy("some data")
        .aes_encrypt("secret password!", mode="OFB", key_format="utf8")
        .to_hex()
        .o
        == b"4ab2b4f72e9d92960b"
    )


def test_aes_decrypt():
    assert (
        Chepy("5fb8c186394fc399849b89d3b6605fa3")
        .hex_to_str()
        .aes_decrypt("7365637265742070617373776f726421")
        .o
        == b"some data"
    )
    assert (
        Chepy("5fb8c186394fc399849b89d3b6605fa3")
        .hex_to_str()
        .aes_decrypt("secret password!", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("5fb8c186394fc399849b89d3b6605fa3")
        .hex_to_str()
        .aes_decrypt("secret password!", mode="ECB", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("4ab2b4f72e9d92960b")
        .hex_to_str()
        .aes_decrypt("secret password!", mode="CFB", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("4ab2b4f72e9d92960b")
        .hex_to_str()
        .aes_decrypt("secret password!", mode="CTR", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("97a6227556b2be0763")
        .hex_to_str()
        .aes_decrypt("secret password!", mode="GCM", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("4ab2b4f72e9d92960b")
        .hex_to_str()
        .aes_decrypt("secret password!", mode="OFB", key_format="utf8")
        .o
        == b"some data"
    )


def test_des_decrypt():
    assert (
        Chepy("1ee5cb52954b211d1acd6e79c598baac")
        .hex_to_str()
        .des_decrypt("70617373776f7264")
        .o
        == b"some data"
    )
    assert (
        Chepy("1ee5cb52954b211d1acd6e79c598baac")
        .hex_to_str()
        .des_decrypt("password", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("1ee5cb52954b211da5b1a0072da15156")
        .hex_to_str()
        .des_decrypt("password", mode="ECB", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("0b7399049b0267d93d")
        .hex_to_str()
        .des_decrypt("password", mode="CTR", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("0b7399049b0267d9a9")
        .hex_to_str()
        .des_decrypt("password", mode="OFB", key_format="utf8")
        .o
        == b"some data"
    )


def test_triple_des_decrypt():
    assert (
        Chepy("f8b27a0d8c837edce87dd13a1ab41f96")
        .hex_to_str()
        .triple_des_decrypt("7375706572207365637265742070617373776f7264202121")
        .o
        == b"some data"
    )
    assert (
        Chepy("f8b27a0d8c837edce87dd13a1ab41f96")
        .hex_to_str()
        .triple_des_decrypt("super secret password !!", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("f8b27a0d8c837edc8fb00ea85f502fb4")
        .hex_to_str()
        .triple_des_decrypt("super secret password !!", mode="ECB", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("51710aefbd5bbb5b40")
        .hex_to_str()
        .triple_des_decrypt("super secret password !!", mode="CTR", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("51710aefbd5bbb5bf9")
        .hex_to_str()
        .triple_des_decrypt("super secret password !!", mode="OFB", key_format="utf8")
        .o
        == b"some data"
    )


def test_blowfish_encrypt():
    assert (
        Chepy("some data").blowfish_encrypt("70617373776f7264").to_hex().o
        == b"d9b0a79853f13960fcee3cae16e27884"
    )
    assert (
        Chepy("some data").blowfish_encrypt("password", key_format="utf8").to_hex().o
        == b"d9b0a79853f13960fcee3cae16e27884"
    )
    assert (
        Chepy("some data")
        .blowfish_encrypt("password", mode="ECB", key_format="utf8")
        .to_hex()
        .o
        == b"d9b0a79853f139603951bff96c3d0dd5"
    )
    assert (
        Chepy("some data")
        .blowfish_encrypt("password", mode="CTR", key_format="utf8")
        .to_hex()
        .o
        == b"82bdcb75a4d655c63a"
    )
    assert (
        Chepy("some data")
        .blowfish_encrypt("password", mode="OFB", key_format="utf8")
        .to_hex()
        .o
        == b"82bdcb75a4d655c6f0"
    )


def test_blowfish_decrypt():
    assert (
        Chepy("d9b0a79853f13960fcee3cae16e27884")
        .hex_to_str()
        .blowfish_decrypt("70617373776f7264")
        .o
        == b"some data"
    )
    assert (
        Chepy("d9b0a79853f13960fcee3cae16e27884")
        .hex_to_str()
        .blowfish_decrypt("password", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("d9b0a79853f139603951bff96c3d0dd5")
        .hex_to_str()
        .blowfish_decrypt("password", mode="ECB", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("82bdcb75a4d655c63a")
        .hex_to_str()
        .blowfish_decrypt("password", mode="CTR", key_format="utf8")
        .o
        == b"some data"
    )
    assert (
        Chepy("82bdcb75a4d655c6f0")
        .hex_to_str()
        .blowfish_decrypt("password", mode="OFB", key_format="utf8")
        .o
        == b"some data"
    )


def test_vigener_encode():
    assert (
        Chepy("shaktictf{y4Yyy!_M1S5i0n_4cCoMpL1sH3D}").vigenere_encode("victory").o
        == b"npcdhzaon{a4Rmp!_K1N5q0p_4vQfKkT1uA3R}"
    )
    assert Chepy("secret").vigenere_encode("secret").o == b"kieiim"


def test_vigenere_decode():
    assert (
        Chepy("npcdhzaon{a4Rmp!_K1N5q0p_4vQfKkT1uA3R}").vigenere_decode("victory").o
        == b"shaktictf{y4Yyy!_M1S5i0n_4cCoMpL1sH3D}"
    )
    assert Chepy("kieiim").vigenere_decode("secret").o == b"secret"


def test_affine_encode():
    assert Chepy("secret").affine_encode().o == b"TFDSFU"


def test_affine_decode():
    assert Chepy("TFDSFU").affine_decode().o == b"SECRET"


def test_atbash_encode():
    assert Chepy("secret").atbash_encode().o == b"hvxivg".upper()


def test_atbash_decode():
    assert Chepy("hvxivg").atbash_decode().o == b"secret".upper()


def test_to_morse_code():
    assert (
        Chepy("hello world").to_morse_code(word_delim="/").o
        == b".... . .-.. .-.. --- /.-- --- .-. .-.. -.. /"
    )


def test_from_morse_code():
    assert (
        Chepy(".... . .-.. .-.. --- \n.-- --- .-. .-.. -..").from_morse_code().o
        == b"HELLO WORLD"
    )


def test_rsa_encrypt_decrypt():
    assert (
        Chepy("lol")
        .rsa_encrypt("tests/files/public.pem")
        .rsa_decrypt("tests/files/private.pem")
        .o
        == b"lol"
    )

    private = """-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQDDhjb/e1alLSQk+2UmXjuYmJ1CuYHRWkfmKdf5MhNell2PhrTM
tT4ljNb7PTi+n8WcwihAxHVNfKvgSQt6q/yuVPj5t51159XJHov+ySANFsTUxsUw
YzHUJ5yeeHbbcWgNwehHMPGSdDuZ/XnXH3VIk50FIRNjzrrMpHuQso58ewIDAQAB
AoGAczd000n//efC49QMf/aJkdtk2Dvuhsp3kebYcO0UQunCimArzHGFBKWgzX3/
IT2POlejVr8uDJJJyinhDNGqXJw9ZEs33f89B7JBGjViS83d9qWypHOg2/OfAt6S
LNICmpPSmKSSJtenFx7XjV0LdG/+b8rENpNy+8TafThnYekCQQDv8oRfMnur8lLq
oG2Fg8RJvq6OA8UOcE4Duo0uPba0uec48kfhBvLsCVhW/vDBDU14o5nUoFKn1sBa
7jU7Mb0fAkEA0JrhtcBNgUd93tp0jSC6T/qNUOVcJjFZWjamB/X4fPesiNw/azV5
OaGpn9wp7swX56DCcLdIR57T9oRw5DX5JQJAWH4Oh7VsmuuR3Ooxui3wdGoYolON
l1efzgw9CTLFcT2mov/ntnwDlz2TEPKRBAHN8pITp7FBCplO87oqc5xSbQJAfpT9
UaSXY1NWddxpzRmG9PE8v1HuUN6xMaTnqvz/BBXmhEXh1dRk8yu+GlsmttjxyIQs
eOk+2vbt+DD1sAVwYQJAF3kq/lbmROIyAOekpXYFCIWU11mHfxSVuxmYjUYLVRGZ
bmwesS2DFBX5scKK27uMng7nBB9QukZ5kitK4cKelA==
-----END RSA PRIVATE KEY-----
    """
    public = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDhjb/e1alLSQk+2UmXjuYmJ1C
uYHRWkfmKdf5MhNell2PhrTMtT4ljNb7PTi+n8WcwihAxHVNfKvgSQt6q/yuVPj5
t51159XJHov+ySANFsTUxsUwYzHUJ5yeeHbbcWgNwehHMPGSdDuZ/XnXH3VIk50F
IRNjzrrMpHuQso58ewIDAQAB
-----END PUBLIC KEY-----
    """
    assert (
        Chepy("hello")
        .rsa_encrypt(public_key=public, is_file=False, cipher="PKCS")
        .rsa_decrypt(private, False, cipher="PKCS")
        .o
        == b"hello"
    )


def test_rsa_sign():
    assert (
        Chepy("lol").rsa_sign("tests/files/private.pem").to_hex().o
        == b"ae12fa91f12af7e1c04e7893ce43fc76195d30203ad0ab88fac3631feb026ee8832d57584a977fe9f70139d8dd7c74b904643ab11493935c642e563752325c1ecde98a29bfaaa714e513d7c3548e9fbea6f2f2705eec3567f4ba868b3ca16f8ede4155e71b854042810bb836dda031c2e540175f4573103c065311d38b7246a6"
    )


def test_monoalphabetic_substitution():
    assert Chepy("lol").monoalphabetic_substitution({"l": "t", "o": "s"}).o == b"tst"


def test_chacha_decrypt():
    assert (
        Chepy("0d118d5f5807747b085473553146a3c76cf1ef61b976519240")
        .from_hex()
        .chacha_decrypt(
            "4c6561726e696e672069732061206c6966656c6f6e6720656e646561766f722e",
            "48656c6c6f20776f726c642e",
        )
        .o
        == b"4t_lea5t_1ts_n0t_Electr0n"
    )


def test_chacha_encrypt():
    assert (
        Chepy("4t_lea5t_1ts_n0t_Electr0n")
        .chacha_encrypt(
            "4c6561726e696e672069732061206c6966656c6f6e6720656e646561766f722e",
            "48656c6c6f20776f726c642e",
        )
        .to_hex()
        .o
        == b"0d118d5f5807747b085473553146a3c76cf1ef61b976519240"
    )


def test_rsa_private_pem_to_jwk():
    c = Chepy(PRIVATE_KEY).rsa_private_pem_to_jwk().o
    assert (
        c["private"]["p"]
        == "u6hkCKCf3M7u0TCV2c2tgELRIc5Z8zZ2_OR8Y98QCLwJF8XrlgUBuLNna_Wyk1goch8_9dtdeOQCzBHmlCS-oKRRd8nxHQKbbnjX5K6AZF9l5q4BF1PqyMEszN25QMnIbeHxjlXPntcgaOcRxce19pdc0iXVKIKpaCfjAhk23Rs"
    )
    assert c["public"]["e"] == "AQAB"


def test_jwt_genereate_embedded_jwk():
    assert (
        Chepy({"user": "lol"})
        .jwt_token_generate_embedded_jwk(PRIVATE_KEY, headers={"kid": "b"})
        .o
        != ""
    )


def test_rsa_public_key_from_jwk():
    assert (
        Chepy(
            {
                "kty": "RSA",
                "e": "AQAB",
                "use": "sig",
                "kid": "66447ed3-9521-4029-afa3-fae1cdd8434b",
                "alg": "RS256",
                "n": "2bxlRFYk-nczolmssgXIsQo9TTRyLpNKDE0hg4ViZNxOQ63jjCTqSSsmZb_4Pt326n0NzJxEeaJ9I3JwpYFrmjkbB-_mk5CyAEL75cMUDyWO3I9DnYR2tHHI4zhd_VQIaIn48A6AjMFHTiTYxM6B03EWSb7U7FqJmUlxTAjuOkeMSQQrMtD8cptJAKHtiYSRPEfN77q3Hr6zx0pXeQnEG-P_fassID6MeJjMAA9xHc1yG8Oc2hnGSvS9Ao6usIIvuShk7lxHjbPyZ2uuC1eNc7qkGiwq2KTX_Huy4cARHt3g_zdGO9nF-ONaUc7yHgzV6Rwch7li25uc9uYS5rYmOw",
            }
        )
        .rsa_public_key_from_jwk()
        .o
        == b"""-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2bxlRFYk+nczolmssgXI\nsQo9TTRyLpNKDE0hg4ViZNxOQ63jjCTqSSsmZb/4Pt326n0NzJxEeaJ9I3JwpYFr\nmjkbB+/mk5CyAEL75cMUDyWO3I9DnYR2tHHI4zhd/VQIaIn48A6AjMFHTiTYxM6B\n03EWSb7U7FqJmUlxTAjuOkeMSQQrMtD8cptJAKHtiYSRPEfN77q3Hr6zx0pXeQnE\nG+P/fassID6MeJjMAA9xHc1yG8Oc2hnGSvS9Ao6usIIvuShk7lxHjbPyZ2uuC1eN\nc7qkGiwq2KTX/Huy4cARHt3g/zdGO9nF+ONaUc7yHgzV6Rwch7li25uc9uYS5rYm\nOwIDAQAB\n-----END PUBLIC KEY-----"""
    )


def test_from_letter_number_code():
    assert (
        Chepy(
            "T4 l16 _36 510 _27 s26 _11 320 414 {6 }39 C2 T0 m28 317 y35 d31 F1 m22 g19 d38 z34 423 l15 329 c12 ;37 19 h13 _30 F5 t7 C3 325 z33 _21 h8 n18 132 k24"
        )
        .from_letter_number_code()
        .o
        == b"TFCCTF{th15_ch4ll3ng3_m4k3s_m3_d1zzy_;d}"
    )


def test_to_letter_number_code():
    assert len(Chepy("test").to_letter_number_code().o.split()) == 4


def test_ls47_enc_dec():
    assert (
        Chepy("hello").ls47_encrypt("password").ls47_decrypt("password").o
        == b"hello---"
    )
