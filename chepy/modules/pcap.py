import collections

import scapy.all as scapy
import scapy.layers.dns as scapy_dns
import scapy.layers.http as scapy_http
from scapy.utils import PcapNgReader, PcapReader

from ..core import ChepyCore, ChepyDecorators
from .internal.functions import Pkt2Dict


class Pcap(ChepyCore):
    @ChepyDecorators.call_stack
    def pcap_dns_queries(self):
        """Get DNS queries and their frame numbers
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            >>> Chepy("tests/files/test.pcapng").read_pcap().pcap_dns_queries().o
            [
                b'fcmconnection.googleapis.com.',
                ...
                b'google.com.'
            ]
        """
        hold = []
        sessions = self._pcap_sessions
        for session in sessions:
            packets = sessions.get(session)
            for packet in packets:
                if not scapy.DNSQR in packet:
                    continue
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
                if not scapy_http.HTTP in packet:
                    continue
                if scapy_http.HTTPRequest in packet:
                    req_res["request"]["headers"] = packet.getlayer(
                        scapy_http.HTTPRequest
                    ).fields
                    if scapy_http.Raw in packet:
                        req_res["request"]["payload"] = packet.getlayer(
                            scapy_http.Raw
                        ).load
                    else:
                        req_res["request"]["payload"] = {}
                if scapy_http.HTTPResponse in packet:
                    req_res["response"]["headers"] = packet.getlayer(
                        scapy_http.HTTPResponse
                    ).fields
                    if scapy_http.Raw in packet:
                        req_res["response"]["payload"] = packet.getlayer(
                            scapy_http.Raw
                        ).load
                    else:  # pragma: no cover
                        req_res["response"]["payload"] = {}
            if len(req_res.get("request")):
                hold.append(req_res)

        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def pcap_payload(self, layer: str):
        """Get an array of payloads based on provided layer
        
        Args:
            layer (str): Required. A valid Scapy layer. 
        
        Returns:
            Chepy: The Chepy object. 
        """
        assert hasattr(scapy, layer), "Not a valid Scapy layer"
        hold = []
        for packet in self._pcap_read:
            if not layer in packet:
                continue
            check_raw = scapy.Raw in packet
            if check_raw:
                hold.append(packet.getlayer(scapy.Raw).load)
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def pcap_to_dict(self):
        """Convert a pcap to a dict
        
        Returns:
            Chepy: The Chepy object. 
        """
        hold = []
        for packet in self._pcap_read:
            hold.append(Pkt2Dict(packet).to_dict())
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def pcap_layer_stats(self):
        """Get a count of all layers in the pcap
        
        Returns:
            Chepy: The Chepy object. 
        """

        def get_layers(pkt):
            yield pkt.name
            while pkt.payload:
                pkt = pkt.payload
                yield pkt.name

        layer_dict = collections.OrderedDict()
        for packet in self._pcap_read:
            for key in list(get_layers(packet)):
                if layer_dict.get(key):
                    layer_dict[key] += 1
                else:
                    layer_dict[key] = 1

        self.state = dict(layer_dict)
        return self

    def pcap_convos(self):
        """Get layer 3 conversation states
        
        Returns:
            Chepy: The Chepy object. 
        """
        convo = collections.OrderedDict()
        for packet in self._pcap_read:
            if not scapy.IP in packet:  # pragma: no cover
                continue
            ip_layer = packet.getlayer(scapy.IP)
            src = ip_layer.src
            dst = ip_layer.dst
            layer_3 = packet.getlayer(2).name
            if not convo.get(src):
                convo[src] = {}
            if convo[src].get(layer_3):
                if dst not in convo[src][layer_3]:
                    convo[src][layer_3].append(dst)
            else:
                convo[src][layer_3] = [dst]
        self.state = dict(convo)
        return self
