
import base64
from pathlib import Path

FLAG = "Securinets{y0u_h4v3_f0und_th3_fl4g_but_y0u_h4v3_l0st_y0urs3lf}"

# Three voices. Each receives every third Base64 character.
VOICES = [
    "THE BOY",
    "THE WITNESS",
    "THE MONSTER",
]

LINES = [
    "remembered a face that nobody else could recall.",
    "believed the truth was buried long ago.",
    "watched as another identity disappeared.",
    "heard a name whispered in an empty room.",
    "wondered whether a monster was ever born.",
    "kept the secret locked behind closed doors.",
    "saw the same smile in every photograph.",
    "found a story with its ending removed.",
]

def generate():
    encoded = base64.b64encode(FLAG.encode()).decode().rstrip("=")

    streams = [encoded[i::3] for i in range(3)]

    output = [
        "A NAME WITHOUT A FACE",
        "",
        "Three accounts survived the investigation.",
        "None tells the whole story.",
        "Read each testimony from beginning to end.",
        "The truth emerges when the voices speak together.",
        "",
    ]

    for voice_index, (voice, stream) in enumerate(zip(VOICES, streams)):
        output.append(f"=== {voice} ===")

        for i, char in enumerate(stream):
            # The first character of each line carries evidence.
            sentence = LINES[(i + voice_index) % len(LINES)]
            output.append(f"{char}{sentence}")

        output.append("")

    Path("johan.txt").write_text(
        "\n".join(output),
        encoding="utf-8"
    )

    print("Created johan.txt")
    print(f"Encoded payload length: {len(encoded)}")

if __name__ == "__main__":
    generate()
