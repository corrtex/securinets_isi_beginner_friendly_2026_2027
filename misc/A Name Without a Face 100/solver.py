import base64
from pathlib import Path

text = Path("johan.txt").read_text(encoding="utf-8")
sections = text.split("=== ")[1:]

streams = []

for section in sections:
    _, body = section.split(" ===", 1)
    chars = [
        line[0]
        for line in body.splitlines()
        if line and not line.startswith("=")
    ]
    streams.append("".join(chars))

encoded = "".join(
    streams[j][i]
    for i in range(max(map(len, streams)))
    for j in range(len(streams))
    if i < len(streams[j])
)

encoded += "=" * (-len(encoded) % 4)
flag = base64.b64decode(encoded).decode()

print(flag)
