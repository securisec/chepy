from chepy import Chepy


def test_pcap_dns():
    assert (
        len(
            Chepy("tests/files/test.pcapng")
            .debug(True)
            .read_pcap()
            .pcap_dns_queries()
            .set()
            .o
        )
        == 3
    )


def test_pcap_http_streams():
    assert len(Chepy("tests/files/test.pcapng").read_pcap().pcap_http_streams().o) == 4


def test_pcap_payload():
    assert Chepy("tests/files/test.pcapng").read_pcap().pcap_payload(
        layer="ICMP"
    ).o == [b"secret", b"message"]


def test_packet_to_dict():
    assert (
        Chepy("tests/files/test.pcapng").read_pcap().pcap_to_dict().o[0]["IP"]["src"]
        == "10.10.10.11"
    )


def test_pcap_layer_stats():
    assert (
        Chepy("tests/files/test.pcapng")
        .read_pcap()
        .pcap_layer_stats()
        .get_by_key("DNS")
        .o
        == 6
    )


def test_pcap_convo():
    assert (
        Chepy("tests/files/test.pcapng")
        .read_pcap()
        .pcap_convos()
        .get_by_key("10.10.10.11")
        .o["ICMP"]
    )


def test_usb_keyboard():
    c = Chepy("tests/files/keyboard.pcap").read_pcap().pcap_usb_keyboard()
    assert "KAIZEN" in c.o


def test_raw_payload_offset():
    assert Chepy("tests/files/test.pcapng").read_pcap().pcap_payload_offset(
        "ICMP", -20
    ).o == [b"secret", b"message"]
