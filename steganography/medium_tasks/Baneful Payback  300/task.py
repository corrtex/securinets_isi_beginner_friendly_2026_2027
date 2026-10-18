from PIL import Image
img = Image.open("full.png").convert("RGB")
msg = b"The venom flows after the end.\x00"
bits = "".join(f"{b:08b}" for b in msg)
px, W = img.load(), img.width
for i, bit in enumerate(bits):
    x, y = i % W, i // W
    r, g, b = px[x, y]
    px[x, y] = (r, (g & ~1) | int(bit), b)
img.save("stego.png")
