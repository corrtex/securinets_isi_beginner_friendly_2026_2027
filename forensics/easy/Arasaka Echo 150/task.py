from scapy.all import IP, ICMP, Raw, wrpcap
from net import stamp
import random

flag = "Securinets{p1ng_1s_tr4c4bl3_by_g00d_n3trunn3r5}"
pkts = []
for i, ch in enumerate(flag):
    pkts.append(IP(src="10.0.0.5", dst="45.33.12.9")/ICMP(type=8, id=7, seq=i)/Raw(ch.encode()))
    pkts.append(IP(src="45.33.12.9", dst="10.0.0.5")/ICMP(type=0, id=7, seq=i)/Raw(ch.encode()))
# noise: normal pings with standard payload
for i in range(60):
    h = f"10.0.0.{random.randint(20,50)}"
    pkts.append(IP(src=h, dst="8.8.8.8")/ICMP(type=8, seq=i)/Raw(bytes(range(32))))
    pkts.append(IP(src="8.8.8.8", dst=h)/ICMP(type=0, seq=i)/Raw(bytes(range(32))))
wrpcap("ping.pcap", stamp(pkts))
