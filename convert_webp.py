"""
convert_webp.py — Convertit les PNG lourdes en WebP
À placer et lancer depuis la racine du projet :
  python3 convert_webp.py
"""
import os
from PIL import Image

# Images à convertir (dans assets/images/)
IMAGES = [
    "monte-escalier-droit.png",
    "monte-escalier-exterieur.png",
    "monte-escalier-hero.png",
    "monte-escalier-tournant.png",
    "monte-escalier-debout.png",
    "monte-escalier-droit-form.png",
    "monte-escalier-exterieur-form.png",
    "monte-escalier-tournant-form.png",
    "monte-escalier-portable.png",
    "plateforme-elevatrice.png",
]

# Images marques
MARQUES = [
    "marques/acorn.png",
    "marques/handicare.png",
    "marques/independance-royale.png",
    "marques/lehner-lifttechnik.png",
    "marques/mobilae.png",
    "marques/otolift.png",
    "marques/platinum-stairlifts.png",
    "marques/stannah.png",
    "marques/thyssenkrupp-home-solutions.png",
]

base = "assets/images"
converted = 0
saved_kb = 0

for filename in IMAGES + MARQUES:
    src = os.path.join(base, filename)
    if not os.path.exists(src):
        print(f"  ⚠  Non trouvé : {src}")
        continue

    dst = src.replace(".png", ".webp").replace(".jpg", ".webp").replace(".jpeg", ".webp")
    
    original_size = os.path.getsize(src)
    
    img = Image.open(src).convert("RGBA" if src.endswith(".png") else "RGB")
    # Conserver transparence pour PNG, sinon RGB
    if img.mode == "RGBA":
        img.save(dst, "WEBP", quality=85, method=6)
    else:
        img = img.convert("RGB")
        img.save(dst, "WEBP", quality=85, method=6)
    
    new_size = os.path.getsize(dst)
    gain = (original_size - new_size) // 1024
    saved_kb += gain
    ratio = int((1 - new_size/original_size) * 100)
    
    print(f"  ✓  {filename}")
    print(f"     {original_size//1024} Ko → {new_size//1024} Ko  (-{ratio}%)")
    converted += 1

print(f"\n{'─'*50}")
print(f"  {converted} images converties")
print(f"  {saved_kb} Ko économisés au total")
print(f"\n⚠  Pensez à mettre à jour les src dans vos HTML (.png → .webp)")
print(f"   puis à supprimer les fichiers .png d'origine.")
