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
