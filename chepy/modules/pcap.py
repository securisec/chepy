import scapy.layers.dns as scapy_dns
from scapy.utils import PcapNgReader, PcapReader

from ..core import ChepyCore, ChepyDecorators


class Pcap(ChepyCore):
    @ChepyDecorators.call_stack
    def pcap_dns_queries(self):
        """Get DNS queries and their frame numbers
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("tests/files/test.pcapng").read_pcap().pcap_dns_queries().o
            [
                {'frame': 1, 'query': b'fcmconnection.googleapis.com.'},
                ...
                {'frame': 9, 'query': b'google.com.'}
            ]
        """
        hold = []
        for index, packet in enumerate(self._pcap_file):
            try:
                hold.append(
                    {"frame": index + 1, "query": packet[scapy_dns.DNS].qd.qname}
                )
            except:
                continue
        self.state = hold
        return self
