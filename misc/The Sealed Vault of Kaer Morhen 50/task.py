import os
import stat

BASE_DIR = "Kaer_Morhen_Vault"
FLAG_FILE = "flag.txt"
FLAG_CONTENT = "Securinets{g3r4lt_1s_v3ry_pr0ud_0f_y0u}"

# Decoy files to make the folder feel like a real Witcher vault
DECOYS = {
    "witcher_journal.txt": "Day 102: The vault remains locked tight. Only magic or the right permissions will open it.",
    "silver_sword_schematic.txt": "Diagram for a Mastercrafted Silver Sword.",
    "potion_recipe.txt": "Swallow Potion: Celandine, Drowner Brain, Alcohol."
}

def create_challenge():
    print("Creating Kaer Morhen Vault...")
    
    # 1. Create directory
    os.makedirs(BASE_DIR, exist_ok=True)
    
    # 2. Create decoy files with normal permissions
    for filename, content in DECOYS.items():
        filepath = os.path.join(BASE_DIR, filename)
        with open(filepath, "w") as f:
            f.write(content + "\n")
            
    # 3. Create flag.txt
    flag_path = os.path.join(BASE_DIR, FLAG_FILE)
    with open(flag_path, "w") as f:
        f.write(f"{FLAG_CONTENT}\n")
        
    # 4. Strip ALL permissions from flag.txt (000 = ---------)
    # This causes "Permission denied" when trying to 'cat' it
    os.chmod(flag_path, 0000)
    
    print("\nTask generated successfully!")
    print(f"Directory: {os.path.abspath(BASE_DIR)}")
    print(f"Locked file: {flag_path}")
    print("\n[!] 'flag.txt' is now locked with 0000 (---------) permissions.")

if __name__ == "__main__":
    create_challenge()