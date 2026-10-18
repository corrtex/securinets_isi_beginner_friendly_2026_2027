from PIL import Image; import numpy as np
a = np.array(Image.open("dante.png")); b = np.array(Image.open("virgil.png"))
Image.fromarray((((a ^ b) & 1) * 255).astype(np.uint8)).save("out.png")
