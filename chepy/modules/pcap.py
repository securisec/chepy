import binascii
import collections

import regex as re
from scapy.utils import PcapReader, rdpcap
from scapy.layers.dns import DNSQR
from scapy.layers.inet import IP
from scapy.packet import Raw
from scapy.layers.http import HTTPRequest, HTTPResponse, HTTP
from scapy.utils import PcapNgReader, PcapReader

from ..core import ChepyCore, ChepyDecorators
from .internal.functions import Pkt2Dict, full_duplex
from .internal.constants import PcapUSB


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
        pcap = rdpcap(self._pcap_filepath)
        sessions = pcap.sessions(full_duplex)
        for session in sessions:
            packets = sessions.get(session)
            for packet in packets:
                if not DNSQR in packet:
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
        pcap = rdpcap(self._pcap_filepath)
        sessions = pcap.sessions(full_duplex)
        for session in sessions:
            packets = sessions.get(session)
            req_res = {"request": {}, "response": {}}
            for packet in packets:
                if not HTTP in packet:
                    continue
                if HTTPRequest in packet:
                    req_res["request"]["headers"] = packet.getlayer(HTTPRequest).fields
                    if Raw in packet:
                        req_res["request"]["payload"] = packet.getlayer(Raw).load
                    else:
                        req_res["request"]["payload"] = {}
                if HTTPResponse in packet:
                    req_res["response"]["headers"] = packet.getlayer(
                        HTTPResponse
                    ).fields
                    if Raw in packet:
                        req_res["response"]["payload"] = packet.getlayer(Raw).load
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
        hold = []
        for packet in PcapReader(self._pcap_filepath):
            if not layer in packet:
                continue
            check_raw = Raw in packet
            if check_raw:
                hold.append(packet.getlayer(Raw).load)
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def pcap_payload_offset(self, layer: str, start: int, end: int = None):
        """Dump the raw payload by offset. 
        
        Args:
            layer (str): The layer to get the data from. 
            start (int): The starting offset of the data to be extracted. 
                This could be a negative index number.
            end (int, optional): The end index of the offset.
        
        Returns:
            Chepy: The Chepy object. 

        Examples:
            In this example, we are extracting all the payloads from the last 20 bytes on 
            on the ICMP layer. 
            
            >>> Chepy('tests/files/test.pcapng').read_pcap().pcap_payload_offset('ICMP', -20)
            [b'secret', b'message']
        """
        packets = PcapReader(self._pcap_filepath)
        hold = []

        for packet in packets:
            if not layer in packet:
                continue
            if not Raw in packet:  # pragma: no cover
                continue
            load = packet.getlayer("Raw").load
            hold.append(load[start:end])
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def pcap_to_dict(self):
        """Convert a pcap to a dict
        
        Returns:
            Chepy: The Chepy object. 
        """
        hold = []
        for packet in PcapReader(self._pcap_filepath):
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
        for packet in PcapReader(self._pcap_filepath):
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
        for packet in PcapReader(self._pcap_filepath):
            if not IP in packet:  # pragma: no cover
                continue
            ip_layer = packet.getlayer(IP)
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

    @ChepyDecorators.call_stack
    def pcap_usb_keyboard(self, layout: str = "qwerty"):
        """Decode usb keyboard pcap
        
        Args:
            layout (str, optional): Layout of the keyboard. Defaults to "qwerty".
        
        Raises:
            TypeError: If layout is not qwerty or dvorak
        
        Returns:
            Chepy: The Chepy object. 
        """
        if layout == "qwerty":
            key_map = PcapUSB.qwerty_map
            shift_modifier = PcapUSB.qwerty_modifier
        elif layout == "dvorak":  # pragma: no cover
            key_map = PcapUSB.dvorak
            shift_modifier = PcapUSB.dvorak_modifier
        else:  # pragma: no cover
            raise TypeError("Valid layouts are qwerty and dvorak")

        packets = PcapReader(self._pcap_filepath)
        hold = []

        for packet in packets:
            if not Raw in packet:  # pragma: no cover
                continue
            load = packet.getlayer("Raw").load
            key_press = binascii.hexlify(load)[-16:]
            if key_press == "0000000000000000":  # pragma: no cover
                continue
            shift, _, key = re.findall(b".{2}", key_press)[0:3]
            shift_pressed = bool(shift == b"02")
            pressed = key_map.get(key.decode())
            if shift_pressed:
                special = shift_modifier.get(key.decode())
                if special:
                    hold.append(special)
                elif pressed:
                    hold.append(pressed.upper())
            elif pressed:
                hold.append(pressed)
        self.state = "".join(hold)
        return self
