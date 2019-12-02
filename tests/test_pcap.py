from chepy import Chepy


def test_pcap_dns():
    assert (
        len(
            Chepy("tests/files/test.pcapng")
            .debug(True)
            .read_pcap()
            .pcap_dns_queries()
            .o
        )
        == 3
    )

def test_pcap_http_streams():
    assert (
        len(
            Chepy("tests/files/test.pcapng")
            .read_pcap()
            .pcap_http_streams()
            .o
        )
        == 4
    )

