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
        == 6
    )

