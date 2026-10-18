from PIL import Image, ImageDraw, ImageFont
i = Image.open('left_arm.jpg').convert('RGB')
d = ImageDraw.Draw(i)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
except: f = ImageFont.load_default(size=48)
d.text((20, 20), 'x0d14_', fill='black', font=f)
i.save('left_armm.jpg')
# corrupt the header
d = bytearray(open('left_armm.jpg','rb').read())
d[0:4] = b'\x00\x00\x00\x00'        # real PNG magic: 89 50 4E 47
open('left_armm.jpg','wb').write(d)