"""
Klipper ut objekt frå Director Task BMP-bilete og lagrar som PNG med gjennomsiktig bakgrunn.
Objekt lagrast i output/objects/ med namn basert på biletfilnamn og celleposisjon.
"""

import os
from PIL import Image

TASK_DIR = os.path.join(os.path.dirname(__file__), "task-files")
OUT_DIR = os.path.join(os.path.dirname(__file__), "output", "objects")
os.makedirs(OUT_DIR, exist_ok=True)

# Cellegrid (x_start, x_end, y_start, y_end) - basert på pikselanalyse
COLS = [(70, 158), (201, 287), (331, 417), (461, 548)]
ROWS = [(83, 173), (193, 283), (304, 394), (415, 504)]

# Bakgrunnsfargar som skal gjerast gjennomsiktige
BG_COLORS = [
    (153, 217, 234),  # open celle (lysblå)
    (178, 178, 178),  # hyllekant (lys grå)
    (128, 128, 128),  # blokkert celle (mørkgrå)
]
BG_TOLERANCE = 25

def is_background(r, g, b):
    """Returner True om pikselen er bakgrunn (ikkje objekt)."""
    # Nøyaktig bakgrunnsfarge-match
    for br, bg_c, bb in BG_COLORS:
        if abs(r - br) < BG_TOLERANCE and abs(g - bg_c) < BG_TOLERANCE and abs(b - bb) < BG_TOLERANCE:
            return True
    # Rein grå (hyllekant i perspektiv, skuggar)
    if abs(int(r) - int(g)) < 15 and abs(int(g) - int(b)) < 15:
        if 80 < r < 220:
            return True
    # Svært mørkt (kantskuggar og -linjer frå hyllerammen)
    if max(r, g, b) < 80:
        return True
    # Mørk teal (antialiasing mot hyllekant)
    if r < 50 and g < 130 and b < 130 and g > r * 1.2:
        return True
    return False

def extract_cell(img_rgba, col, row):
    """
    Klipper ut ein celle, gjer bakgrunn gjennomsiktig,
    og returnerer (trimma bilde, has_content).
    """
    x1, x2 = COLS[col]
    y1, y2 = ROWS[row]

    cell = img_rgba.crop((x1, y1, x2, y2))
    w, h = cell.size
    pixels = cell.load()

    has_content = False
    for x in range(w):
        for y in range(h):
            r, g, b, a = pixels[x, y]
            if is_background(r, g, b):
                pixels[x, y] = (r, g, b, 0)  # gjennomsiktig
            else:
                has_content = True

    # Krev eit minimum av innhaldspikslar for å unngå kantartefaktar
    content_count = sum(1 for x in range(w) for y in range(h) if pixels[x, y][3] > 0)
    if content_count < 80:
        return None, False

    # Trim til innhald
    bbox = cell.getbbox()
    if bbox is None:
        return None, False

    # Legg til litt padding
    pad = 5
    bx1, by1, bx2, by2 = bbox
    bx1 = max(0, bx1 - pad)
    by1 = max(0, by1 - pad)
    bx2 = min(w, bx2 + pad)
    by2 = min(h, by2 + pad)

    trimmed = cell.crop((bx1, by1, bx2, by2))
    return trimmed, True

def process_image(bmp_path):
    name = os.path.splitext(os.path.basename(bmp_path))[0]
    img = Image.open(bmp_path).convert("RGBA")

    extracted = []
    for row in range(4):
        for col in range(4):
            cell_img, has_content = extract_cell(img, col, row)
            if has_content:
                out_name = f"{name}_r{row}c{col}.png"
                out_path = os.path.join(OUT_DIR, out_name)
                cell_img.save(out_path)
                extracted.append(out_name)

    return extracted

def main():
    # Behandle berre "n"-bilete (utan direktør) for reine objekt
    bmp_files = [
        f for f in os.listdir(TASK_DIR)
        if f.endswith(".bmp") and f.startswith("n")
    ]
    bmp_files.sort()

    print(f"Behandlar {len(bmp_files)} bilete...")
    total = 0
    for fname in bmp_files:
        path = os.path.join(TASK_DIR, fname)
        extracted = process_image(path)
        if extracted:
            print(f"  {fname}: {len(extracted)} objekt funne")
            total += len(extracted)

    print(f"\nTotalt {total} celleutklipp lagra i {OUT_DIR}/")

if __name__ == "__main__":
    main()
