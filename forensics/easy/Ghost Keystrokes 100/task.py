import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from scapy.all import wrpcap
from net import tcp_session, stamp
import random

FLAG = "Securinets{t3ln3t_k33ps_n0_s3cr3ts}"
random.seed(1337)

def typed(text):            # one packet per keystroke
    return [("c", ch.encode()) for ch in text]

ex  = [("s", b"NEXACORP VAULT-07 // LEGACY TERMINAL SERVICE\r\nUnauthorized access will be traced.\r\n\r\nvault-07 login: ")]
ex += typed("sysop\r\n")
ex += [("s", b"Passcode: ")]
ex += typed(FLAG + "\r\n")
ex += [("s", b"\r\nAccess granted. Welcome back, sysop.\r\nsysop@vault-07:~$ ")]
ex += typed("ls /vault\r\n")
ex += [("s", b"blueprints.enc  payroll_q3.enc  project_icarus.enc\r\nsysop@vault-07:~$ ")]
ex += typed("exit\r\n")
ex += [("s", b"Connection closed. Stay chrome.\r\n")]

pkts = tcp_session("10.0.0.15", "10.0.0.2", 51515, 23, ex)

# noise: a couple of unrelated TCP sessions
for _ in range(3):
    pkts += tcp_session(f"10.0.0.{random.randint(20, 40)}", "10.0.0.10", random.randint(40000, 60000), 443,
                        [("c", os.urandom(200)), ("s", os.urandom(800))])

wrpcap("over_the_shoulder.pcap", stamp(pkts))
print("[+] over_the_shoulder.pcap written")
