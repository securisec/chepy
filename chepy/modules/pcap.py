import scapy.all as scapy
import scapy.layers.dns as scapy_dns
import scapy.layers.http as scapy_http
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
        sessions = self._pcap_sessions
        for session in sessions:
            packets = sessions.get(session)
            for packet in packets:
                if not packet.haslayer(scapy.DNSRR):
                    continue
                dns = packet.getlayer("DNS")
                query = packet.getlayer("DNS").qd.qname
                hold.append(query)
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def pcap_http_streams(self):
        """Get a dict of HTTP req/res 

        This method does full fully assemble when data exceeds a 
        certain threshold. 
        
        Returns:
            Chepy: The Chepy object. 
        """
        hold = []
        sessions = self._pcap_sessions
        for session in sessions:
            packets = sessions.get(session)
            req_res = {"request": {}, "response": {}}
            for packet in packets:
                if not packet.haslayer(scapy_http.HTTP):
                    continue
                if packet.haslayer(scapy_http.HTTPRequest):
                    req_res["request"]["headers"] = packet.getlayer(
                        scapy_http.HTTPRequest
                    ).fields
                    if packet.haslayer(scapy_http.Raw):
                        req_res["request"]["payload"] = packet.getlayer(
                            scapy_http.Raw
                        ).load
                    else:
                        req_res["request"]["payload"] = {}
                if packet.haslayer(scapy_http.HTTPResponse):
                    req_res["response"]["headers"] = packet.getlayer(
                        scapy_http.HTTPResponse
                    ).fields
                    if packet.haslayer(scapy_http.Raw):
                        req_res["response"]["payload"] = packet.getlayer(
                            scapy_http.Raw
                        ).load
                    else:  # pragma: no cover
                        req_res["response"]["payload"] = {}
            if len(req_res.get("request")):
                hold.append(req_res)

        self.state = hold
        return self
