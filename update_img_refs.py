"""
update_img_refs.py — Remplace les .png par .webp dans tous les HTML
À lancer depuis la racine du projet APRÈS convert_webp.py
"""
import os
import glob

# Images converties en WebP (exclure celles où WebP était plus lourd)
CONVERTED = [
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
    "marques/acorn.png",
    "marques/handicare.png",
    "marques/independance-royale.png",
    "marques/lehner-lifttechnik.png",
    "marques/otolift.png",
    "marques/stannah.png",
    "marques/thyssenkrupp-home-solutions.png",
]

html_files = glob.glob("**/*.html", recursive=True)
updated_files = 0
updated_refs = 0

for path in html_files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    for img in CONVERTED:
        webp = img.replace(".png", ".webp")
        content = content.replace(img, webp)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        count = sum(original.count(img) for img in CONVERTED)
        print(f"  ✓  {path} ({count} référence(s) mise(s) à jour)")
        updated_files += 1
        updated_refs += count

print(f"\n{'─'*50}")
print(f"  {updated_files} fichiers mis à jour")
print(f"  {updated_refs} références .png → .webp")
