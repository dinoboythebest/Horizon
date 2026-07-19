"""Split Ethan HGSS trainer sheet using exact sprite bounding boxes (no grid)."""
from PIL import Image
from pathlib import Path
import csv
import shutil

SRC = Path("/Users/Tamilore/.cursor/projects/Users-Tamilore-Desktop-code-horizon/assets/pokemon_trainer_ethan_hgss_sprite_sheet__by_robloxmaster376_de3lhu7-1a4fb7ff-cb7e-4ec9-b5ae-d12d2cb2a8b1.png")

OUT = Path(__file__).resolve().parent / "trainer_ethan_hgss"
SOURCES = Path(__file__).resolve().parent / "sources"

# (filename, x0, y0, x1, y1) — tight boxes from connected-component scan of 368x189 sheet
# Walk top row: down(4) → up(4) → left(4) → right(4), left to right
SPRITES = [
    # walk down ↓
    ("overworld_walk_down_01.png", 4, 1, 18, 15),
    ("overworld_walk_down_02.png", 19, 11, 33, 18),
    ("overworld_walk_down_03.png", 36, 8, 47, 18),
    ("overworld_walk_down_04.png", 50, 1, 64, 18),
    # walk up ↑
    ("overworld_walk_up_01.png", 67, 9, 80, 18),
    ("overworld_walk_up_02.png", 83, 9, 94, 18),
    ("overworld_walk_up_03.png", 100, 9, 111, 17),
    ("overworld_walk_up_04.png", 137, 10, 151, 18),
    # walk left ←
    ("overworld_walk_left_01.png", 154, 9, 166, 18),
    ("overworld_walk_left_02.png", 172, 9, 182, 18),
    ("overworld_walk_left_03.png", 202, 9, 214, 18),
    ("overworld_walk_left_04.png", 218, 9, 231, 17),
    # walk right →
    ("overworld_walk_right_01.png", 250, 1, 260, 15),
    ("overworld_walk_right_02.png", 264, 10, 276, 16),
    ("overworld_walk_right_03.png", 281, 8, 292, 19),
    ("overworld_walk_right_04.png", 298, 2, 309, 17),
    # run (12) — left block, 4×3
    ("overworld_run_01.png", 5, 34, 16, 50),
    ("overworld_run_02.png", 25, 35, 37, 52),
    ("overworld_run_03.png", 47, 35, 58, 51),
    ("overworld_run_04.png", 68, 35, 78, 62),
    ("overworld_run_05.png", 6, 74, 16, 80),
    ("overworld_run_06.png", 26, 74, 36, 80),
    ("overworld_run_07.png", 49, 74, 59, 80),
    ("overworld_run_08.png", 68, 75, 78, 81),
    ("overworld_run_09.png", 2, 114, 12, 123),
    ("overworld_run_10.png", 24, 114, 35, 124),
    ("overworld_run_11.png", 50, 115, 62, 125),
    ("overworld_run_12.png", 76, 114, 90, 122),
    # swim (6) — 2×3 center
    ("overworld_swim_01.png", 103, 36, 119, 59),
    ("overworld_swim_02.png", 132, 37, 154, 59),
    ("overworld_swim_03.png", 103, 78, 119, 91),
    ("overworld_swim_04.png", 132, 79, 154, 93),
    ("overworld_swim_05.png", 176, 90, 194, 115),
    ("overworld_swim_06.png", 133, 108, 155, 123),
    # fly (2) — right of swim
    ("overworld_fly_01.png", 331, 9, 342, 18),
    ("overworld_fly_02.png", 353, 9, 365, 20),
    # character base — above last throw frame
    ("character_base.png", 307, 48, 342, 110),
    # throw (5) — full frames only
    ("battle_throw_01.png", 26, 146, 56, 189),
    ("battle_throw_02.png", 98, 160, 127, 189),
    ("battle_throw_03.png", 142, 145, 190, 189),
    ("battle_throw_04.png", 217, 143, 283, 189),
    ("battle_throw_05.png", 285, 163, 317, 189),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC, SOURCES / SRC.name)

    im = Image.open(SRC).convert("RGBA")
    w, h = im.size

    for p in OUT.glob("*.png"):
        p.unlink()

    rows = []
    for i, (name, x0, y0, x1, y1) in enumerate(SPRITES, start=1):
        pad = 1
        crop = im.crop((
            max(0, x0 - pad), max(0, y0 - pad),
            min(w, x1 + pad), min(h, y1 + pad),
        ))
        bb = crop.getbbox()
        if not bb:
            print("SKIP empty", name)
            continue
        out = crop.crop(bb)
        out.save(OUT / name)
        action = name.split("_")[0] if name.startswith("battle") else name.replace(".png", "").split("_")[1]
        direction = ""
        if "walk_" in name:
            direction = name.split("walk_")[1].split("_")[0]
        rows.append({
            "index": i,
            "file": name,
            "x": x0, "y": y0,
            "width": x1 - x0, "height": y1 - y0,
            "action": action,
            "direction": direction,
        })

    with open(OUT / "sprites_map.csv", "w", newline="") as f:
        cw = csv.DictWriter(f, fieldnames=["index", "action", "direction", "file", "x", "y", "width", "height"])
        cw.writeheader()
        cw.writerows(rows)

    print(f"Saved {len(rows)} sprites to {OUT}")


if __name__ == "__main__":
    main()
