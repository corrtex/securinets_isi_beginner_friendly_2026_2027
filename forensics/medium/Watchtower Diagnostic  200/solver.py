import subprocess

M = {0x04:'a',0x05:'b',0x06:'c',0x07:'d',0x08:'e',0x09:'f',0x0a:'g',0x0b:'h',
0x0c:'i',0x0d:'j',0x0e:'k',0x0f:'l',0x10:'m',0x11:'n',0x12:'o',0x13:'p',0x14:'q',
0x15:'r',0x16:'s',0x17:'t',0x18:'u',0x19:'v',0x1a:'w',0x1b:'x',0x1c:'y',0x1d:'z',
0x1e:'1',0x1f:'2',0x20:'3',0x21:'4',0x22:'5',0x23:'6',0x24:'7',0x25:'8',0x26:'9',
0x27:'0',0x2d:'-',0x2f:'[',0x30:']'}
SHIFT = {'-':'_','[':'{',']':'}'}

out = subprocess.check_output(
    ["tshark","-r","usb.pcap","-T","fields","-e","usb.capdata"], text=True)

flag = ""
for line in out.splitlines():
    b = line.strip().replace(":", "")
    if len(b) < 6:
        continue
    mod, key = int(b[0:2],16), int(b[4:6],16)
    if key == 0:
        continue
    c = M.get(key, "")
    if mod & 0x22:                       # left or right shift
        c = SHIFT.get(c, c.upper())
    flag += c
print(flag)
