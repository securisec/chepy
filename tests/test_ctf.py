from chepy import Chepy

"""
general tests for CTF solvers
"""


def test_csaw_23_breakthevault():
    assert (
        Chepy(
            "5346815611816381158830026000575759913046890410767282609674124748425112753245783703275530777684185849448083"
        )
        .to_base(16)
        .from_hex()
        .rotate_right(4)
        .from_base64()
        .o
        == b"csawctf{w@11_ST_1s_n0t_n3ce$$@ry}"
    )


def test_hero_v5_heap():
    key = "c45c60232c9847e2"
    payload = "kSDIsBFTYa3+aLqEpVLXtspdLse8WclEhbqGLiqvM6k="

    c = (
        Chepy(payload)
        .from_base64()
        .aes_decrypt(key=key, key_format="utf-8", mode="ECB")
    )
    assert c.o == b"Hero{D1G_1NT0_J4V4_H34P}"


def test_africe_23_own_reality():
    k = ".__..._..__...._.___._...___._...__.__...__.._._._....__._._._..._...__..____.__._._._._.__.___..__._.__.__.___..__.____.___.___.__.___.._._____.__..._..__._.._.___._...___..__._._____..__..__..___.....__._...__.._._.__.._._.__...._..__._....___.._.__..._...__._....__..._..__.___.__.._._.__.._._..__.._..__..__..__..__...__._._.__...._..__..._..__..__.__..__..__..._..__.._...__...__.__...__.__...._..__.__..__..__...__..__..__.._...__.___._____._"
    c = Chepy(k).find_replace("\\.", "0").find_replace("_", "1").from_binary()
    assert c.o == b"battleCTF{Unknown_bits_384eea49b417ee2ff5a13fbdcca6f327}"


def test_springforward_23_hours_behind():
    c = Chepy("vqkk{0vtg_b1um_e1tt_b3tt}")
    c.rotate_bruteforce().dict_get_items().filter_list("nicc")
    assert c.o == b"nicc{0nly_t1me_w1ll_t3ll}"
