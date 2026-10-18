from scapy.all import IP, TCP, Raw
import time

def tcp_session(cip, sip, cport, sport, exchanges):
    """exchanges: list of ('c'|'s', bytes) — client or server sends data"""
    cs, ss = 1000, 5000
    def pkt(frm, flags, data=b""):
        if frm == "c":
            p = IP(src=cip, dst=sip)/TCP(sport=cport, dport=sport, flags=flags, seq=cs, ack=ss)
        else:
            p = IP(src=sip, dst=cip)/TCP(sport=sport, dport=cport, flags=flags, seq=ss, ack=cs)
        return p/Raw(data) if data else p
    pkts = [pkt("c", "S")]; cs += 1
    pkts.append(pkt("s", "SA")); ss += 1
    pkts.append(pkt("c", "A"))
    for frm, data in exchanges:
        pkts.append(pkt(frm, "PA", data))
        if frm == "c": cs += len(data)
        else: ss += len(data)
    pkts.append(pkt("c", "FA")); cs += 1
    pkts.append(pkt("s", "FA")); ss += 1
    pkts.append(pkt("c", "A"))
    return pkts

def stamp(pkts, start=None, gap=0.05):
    t = start or time.time()
    for i, p in enumerate(pkts):
        p.time = t + i * gap
    return pkts
