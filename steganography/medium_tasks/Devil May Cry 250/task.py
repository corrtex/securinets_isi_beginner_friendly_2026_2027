from PIL import Image
import numpy as np

dante  = np.array(Image.open("dante_src.png").convert("RGB"))
virgil = np.array(Image.open("virgil_src.png").convert("RGB"))
mask   = (np.array(Image.open("mask.png").convert("L")) > 127).astype(np.uint8)[:, :, None]

virgil = (virgil & 0xFE) | ((dante & 1) ^ mask)

Image.fromarray(dante).save("dante.png")
Image.fromarray(virgil.astype(np.uint8)).save("virgil.png")
print("done")
