from collections import ChainMap
import scapy.all as scapy


def full_duplex(p):  # pragma: no cover
    """Create a full duplex stream from packets
    `Reference <https://gist.github.com/MarkBaggett/d8933453f431c111169158ce7f4e2222>`__
    """
    sess = "Other"
    if "Ether" in p:
        if "IP" in p:
            if "TCP" in p:
                sess = str(
                    sorted(
                        [
                            "TCP",
                            p[scapy.IP].src,
                            p[scapy.TCP].sport,
                            p[scapy.IP].dst,
                            p[scapy.TCP].dport,
                        ],
                        key=str,
                    )
                )
            elif "UDP" in p:
                sess = str(
                    sorted(
                        [
                            "UDP",
                            p[scapy.IP].src,
                            p[scapy.UDP].sport,
                            p[scapy.IP].dst,
                            p[scapy.UDP].dport,
                        ],
                        key=str,
                    )
                )
            elif "ICMP" in p:
                sess = str(
                    sorted(
                        [
                            "ICMP",
                            p[scapy.IP].src,
                            p[scapy.IP].dst,
                            p[scapy.ICMP].code,
                            p[scapy.ICMP].type,
                            p[scapy.ICMP].id,
                        ],
                        key=str,
                    )
                )
            else:
                sess = str(
                    sorted(
                        ["IP", p[scapy.IP].src, p[scapy.IP].dst, p[scapy.IP].proto],
                        key=str,
                    )
                )
        elif "ARP" in p:
            sess = str(sorted(["ARP", p[scapy.ARP].psrc, p[scapy.ARP].pdst], key=str))
        # else:
        #     sess = p.sprintf("Ethernet type=%04xr,Ether.type%")
    return sess


def _layer2dict(obj):
    d = {}

    if not getattr(obj, "fields_desc", None):
        return
    for f in obj.fields_desc:
        value = getattr(obj, f.name)
        if value is type(None):  # pragma: no cover
            value = None

        if not isinstance(
            value, (int, float, str, bytes, bool, list, tuple, set, dict, type(None))
        ):
            value = _layer2dict(value)
        d[f.name] = value
    return {obj.name: d}


class Pkt2Dict:
    def __init__(self, pkt):
        self.pkt = pkt

    def to_dict(self):
        """
        Turn every layer to dict, store in ChainMap type.
        `Reference <https://github.com/littlezz/scapy2dict>`__
        """
        d = list()
        count = 0

        while True:
            layer = self.pkt.getlayer(count)
            if not layer:
                break
            d.append(_layer2dict(layer))

            count += 1
        return dict(**ChainMap(*list(filter(lambda x: x is not None, d))))
