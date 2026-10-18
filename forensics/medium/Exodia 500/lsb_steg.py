from PIL import Image

def text_to_bin(text):
    """Convert string to binary with an end-of-message marker."""
    text += "<<<END>>>"  # Sentinel to mark end of hidden text
    return ''.join(format(ord(c), '08b') for c in text)

def hide_text(image_path, secret_text, output_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    binary_text = text_to_bin(secret_text)
    
    width, height = img.size
    max_bytes = (width * height * 3) // 8
    
    if len(binary_text) > width * height * 3:
        raise ValueError(f"Text too long! Image can only hold {max_bytes} bytes.")

    data_idx = 0
    total_bits = len(binary_text)

    for y in range(height):
        for x in range(width):
            if data_idx >= total_bits:
                break
            
            r, g, b = pixels[x, y]
            
            # Modify LSB for R, G, B channels
            channels = [r, g, b]
            for i in range(3):
                if data_idx < total_bits:
                    channels[i] = (channels[i] & ~1) | int(binary_text[data_idx])
                    data_idx += 1
            
            pixels[x, y] = tuple(channels)
            
        if data_idx >= total_bits:
            break

    img.save(output_path, format="PNG")
    print(f"[+] Text hidden successfully in '{output_path}'!")

def extract_text(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    
    width, height = img.size
    binary_bits = []

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_bits.extend([str(r & 1), str(g & 1), str(b & 1)])

    # Convert bits back to characters
    bit_str = ''.join(binary_bits)
    bytes_list = [bit_str[i:i+8] for i in range(0, len(bit_str), 8)]
    
    decoded_text = ""
    for b in bytes_list:
        char = chr(int(b, 2))
        decoded_text += char
        if decoded_text.endswith("<<<END>>>"):
            return decoded_text[:-9]  # Strip delimiter

    return "[!] Sentinel marker not found."

# Example Usage
if __name__ == "__main__":
    # Hide
    hide_text("right_arm.png", "Securinets{3", "right_armm.png")
    
    # Extract
    revealed = extract_text("right_armm.png")
    print(f"[+] Extracted Message: {revealed}")