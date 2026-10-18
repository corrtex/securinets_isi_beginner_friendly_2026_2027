import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from scapy.all import wrpcap
from net import tcp_session, stamp
import random

pages = {
    "/": "<h1>Welcome to my blog</h1>",
    "/about": "<p>I like cats and coffee.</p>",
    "/contact": "<p>Email me at admin@blog.local</p>",
    "/secret": "<p>Securinets{http_15_n0t_s0_s3cur3_4m_1_r1ght}</p>",
}

pkts = []
for path in ["/", "/about", "/contact", "/secret", "/"]:
    body = pages[path]
    pkts += tcp_session(f"10.0.0.{random.randint(20, 50)}", "10.0.0.10", random.randint(40000, 60000), 80,
        [("c", f"GET {path} HTTP/1.1\r\nHost: blog.local\r\n\r\n".encode()),
         ("s", f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode())])

wrpcap("capture.pcap", stamp(pkts))

