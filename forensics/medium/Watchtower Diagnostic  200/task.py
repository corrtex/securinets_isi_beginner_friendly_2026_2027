from scapy.all import wrpcap, Raw
from scapy.all import PcapWriter
import struct

FLAG = "Securinets{w4tcht0w3r_d14gn0st1c_p4ss3d_succ3ssfully}"

KEYMAP = {}
for i, c in enumerate("abcdefghijklmnopqrstuvwxyz"): KEYMAP[c] = 0x04 + i
for i, c in enumerate("1234567890"):                 KEYMAP[c] = 0x1e + i
KEYMAP.update({'_': 0x2d, '-': 0x2d, '{': 0x2f, '}': 0x30})
SHIFTED = set("{}_") | set(c.upper() for c in "abcdefghijklmnopqrstuvwxyz")

def urb(hid8):
    # 64-byte Linux usbmon header (DLT 220) + 8-byte HID report
    hdr = bytearray(64)
    hdr[8] = 0x43          # 'C' = Complete
    hdr[9] = 0x01          # URB_SUBMIT type
    hdr[10] = 0x01         # transfer type: interrupt
    hdr[11] = 0x81         # endpoint 0x81 (IN)
    struct.pack_into("<i", hdr, 36, 8)   # data length = 8
    return bytes(hdr) + hid8

import struct

def report(mod, key):
    return bytes([mod, 0x00, key, 0, 0, 0, 0, 0])

packets = []
for ch in FLAG:
    low = ch.lower() if ch.isalpha() else ch
    key = KEYMAP.get(low, 0)
    mod = 0x02 if ch in SHIFTED else 0x00
    packets.append(urb(report(mod, key)))   # press
    packets.append(urb(report(0, 0)))       # release

with open("usb.pcap", "wb") as f:
    # global header: magic, v2.4, tz, sigfigs, snaplen, linktype=220
    f.write(struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 220))
    for i, p in enumerate(packets):
        f.write(struct.pack("<IIII", i, i * 1000, len(p), len(p)))  # ts_sec, ts_usec, caplen, len
        f.write(p)

print("[+] usb.pcap written")
