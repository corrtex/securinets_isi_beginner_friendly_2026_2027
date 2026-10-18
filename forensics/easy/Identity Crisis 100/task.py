from PIL import Image, ImageDraw, ImageFont

font = ImageFont.load_default(size=40)
small = ImageFont.load_default(size=24)

# Page 1: decoy
p1 = Image.new("RGB", (1240, 1754), "white")   # A4 at 150 dpi
d = ImageDraw.Draw(p1)
d.text((100, 100), "Quarterly Report - Q3", fill="black", font=font)
d.text((100, 200), "Revenue was stable. Nothing interesting here.", fill="black", font=small)

# Page 2: flag
p2 = Image.new("RGB", (1240, 1754), "white")
d = ImageDraw.Draw(p2)
d.text((100, 100), "Appendix", fill="black", font=font)
d.text((100, 800), "Securinets{n3v3r_tru5t_f1l3_3xt3ns1on5}", fill="black", font=font)

p1.convert("P").save("report.pdf", save_all=True, append_images=[p2.convert("P")])
