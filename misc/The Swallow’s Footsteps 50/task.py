import os
import random

# Base task folder
BASE_DIR = "Where is Ciri?"

# Witcher 3 locations structure: Realm -> Region -> Location
LORE_TREE = {
    "Velen": {
        "Crow_Perch": ["Barons_Quarters", "Armory", "Stables", "Garden", "Dungeons"],
        "Crookback_Bog": ["Orphanage", "Whispering_Hillock", "Tapestry_Shrine", "Muddy_Hut"],
        "Lornruk": ["Lighthouse", "Underwater_Cave", "Drawbridge_Mechanism"],
        "Fyke_Isle": ["Tower_Floor_1", "Tower_Floor_2", "Laboratory", "Catacombs"],
        "Midcopse": ["Keira_Hut", "Merchant_Stall", "Notice_Board"]
    },
    "Novigrad": {
        "Hierarch_Square": ["Bank_Vivaldi", "Bookstore", "Alchemist_Shop", "Public_Gallows"],
        "Bits": ["Cripple_Kate", "Rosemary_and_Thyme", "Beggars_Alley", "Sewers_Entrance"],
        "Temple_Isle": ["Great_Temple", "Witch_Hunter_Barracks", "Cliffs", "Secret_Tunnel"],
        "Oxenfurt": ["Academy_Library", "Alchemy_Lab", "Docks", "Oxenfurt_Tavern"]
    },
    "Skellige": {
        "Kaer_Trolde": ["Keep_Hall", "Armory", "Port_Docks", "Yennefer_Room"],
        "Fyresdal": ["Old_Watchtower", "Mead_Hall", "Forest_Clearing"],
        "Spikeroog": ["Arena", "Svanrige_Camp", "Ruined_Keep"],
        "Undvik": ["Abandoned_Village", "Forge", "Giant_Cave", "Shipwreck_Bay"]
    },
    "Toussaint": {
        "Beauclair": ["Palace_Gardens", "Wine_Cellars", "Geralt_Estate", "Tournament_Grounds"],
        "Corvo_Bianco": ["Vineyard_Rows", "Main_House", "Underground_Vault", "Stables"],
        "Dun_Tynne": ["Castle_Courtyard", "Guard_Tower", "Hidden_Passage"]
    },
    "Kaer_Morhen": {
        "Main_Keep": ["Great_Hall", "Training_Yard", "Lab_Equipment", "Bedrooms"],
        "Surrounding_Valleys": ["Witcher_Forge", "Lake_Hut", "Bastion_Ruins", "Signal_Tower"]
    }
}

# Sub-subfolders to create dense nesting (depth level 4 & 5)
SUB_PATHWAYS = ["Chests", "Barrels", "Loose_Bricks", "Hidden_Compartments", "Corpse_Pockets", "Sacks", "Under_Bed"]

# Decoy items to fill the directories
DECOY_FILES = [
    ("rumor.txt", "Tavern keeper says a girl with ash-grey hair passed by two days ago... turned out to be a merchant's daughter."),
    ("note.txt", "Wild Hunt riders spotted nearby! Clear the village!"),
    ("contract.txt", "Witcher Contract: Drowners near the riverbank. Reward: 50 crowns."),
    ("letter.txt", "Dear Geralt, if you are reading this, I have already moved on towards Novigrad. — Triss"),
    ("journal.txt", "Day 4: Still no sign of Ciri. The tracks end near the swamp.")
]

# Real Flag Location
FLAG_REALM = "Skellige"
FLAG_REGION = "Undvik"
FLAG_LOCATION = "Shipwreck_Bay"
FLAG_SUB = "Hidden_Compartments"
FLAG_CONTENT = "Securinets{C1r1_1s_S4f3_1n_K43r_M0rh3n}"

def generate_task():
    print("Creating the Witcher 3 world directories...")
    total_folders = 0
    
    # Generate deep folder paths
    for realm, regions in LORE_TREE.items():
        for region, locations in regions.items():
            for loc in locations:
                for sub in SUB_PATHWAYS:
                    folder_path = os.path.join(BASE_DIR, realm, region, loc, sub)
                    os.makedirs(folder_path, exist_ok=True)
                    total_folders += 1
                    
                    # Add random decoy files into ~40% of folders
                    if random.random() < 0.4:
                        decoy_name, decoy_content = random.choice(DECOY_FILES)
                        with open(os.path.join(folder_path, decoy_name), "w") as f:
                            f.write(decoy_content + "\n")

    # Place the actual flag in the designated hidden path
    flag_dir = os.path.join(BASE_DIR, FLAG_REALM, FLAG_REGION, FLAG_LOCATION, FLAG_SUB)
    os.makedirs(flag_dir, exist_ok=True)
    
    flag_file_path = os.path.join(flag_dir, "flag.txt")
    with open(flag_file_path, "w") as f:
        f.write(f"{FLAG_CONTENT}\n")

    print(f"Task generation complete!")
    print(f"Total directories created: {total_folders}")
    print(f"Flag hidden at: {os.path.relpath(flag_file_path)}")

if __name__ == "__main__":
    generate_task()