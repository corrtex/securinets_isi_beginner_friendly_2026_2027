# Phishing → DNS Exfil — Walkthrough

**Scenario:** A friend clicked a fake "verify your account" link and got hacked. We have the packet capture. Find what the malware stole.

## Step 1 — Follow the web traffic

Open `incident.pcap` in Wireshark and apply the filter:

```
http
```

You see the victim visit the phishing site and load an image:

```
GET /account/verify      → secure-update-verify.net   (fake login page)
GET /static/agent.png    → the attacker's "calling card"
```

## Step 2 — Export the image

*File → Export Objects → HTTP* → select `agent.png` → **Save**.

## Step 3 — Pull the key from the image

The photo hides the malware's key in its metadata:

```bash
zsteg hacked.png
```

```
Comment : c2_xor_key: stress
```

The key is **`stress`**. The `c2` label (command-and-control) hints that it unlocks the attacker's traffic.

## Step 4 — Find the stolen data

The HTTP traffic has nothing left to decode — a dead end. The data actually left over **DNS**. Filter:

```
dns.qry.name contains "exfil"
```

You get a burst of queries like:

```
00.20111110011a1d11.exfil.nexus-c2.net
01.061608074200433a.exfil.nexus-c2.net
02.000701470116162c.exfil.nexus-c2.net
03.0a402d1f16161611.exfil.nexus-c2.net
04.17001616165e5818.exfil.nexus-c2.net
```

Each subdomain carries a hex chunk of the stolen data. The leading number is the **order** to reassemble them (queries can arrive scrambled).

## Step 5 — Reassemble the hex

Sort by sequence number and glue the chunks together:

```bash
tshark -r incident.pcap -Y 'dns.qry.name contains "exfil"' -T fields -e dns.qry.name \
  | sort -u | sed -E 's/^[0-9]+\.([0-9a-f]+)\.exfil.*/\1/' | tr -d '\n'; echo
```

## Step 6 — Decode

The bytes are hex-encoded, then XOR-encrypted with the key.

**CyberChef:** paste the hex → **From Hex** → **XOR** with key `stress` set to **UTF8**.

**Or Python:**

```python
h = "...glued hex..."
key = b"stress"
data = bytes.fromhex(h)
print(bytes(data[i] ^ key[i % len(key)] for i in range(len(data))).decode())
```

## Flag

```
Securinets{...}
```

## Takeaway

Malware rarely exfiltrates in plain sight. **DNS tunneling** slips past firewalls that trust port 53, and the light XOR encoding defeats a lazy `strings`. The solve chains three real IR skills: HTTP object export, metadata analysis, and decoding a covert DNS channel.
