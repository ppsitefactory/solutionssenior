"""
add_canonical.py — Ajoute le canonical manquant sur les pages comparatif
À placer et lancer depuis la racine du projet :
  python3 add_canonical.py
"""
import os

PAGES = {
    "monte-escaliers/comparatif/acorn/index.html":
        "https://solutionssenior.fr/monte-escaliers/comparatif/acorn/",
    "monte-escaliers/comparatif/handicare/index.html":
        "https://solutionssenior.fr/monte-escaliers/comparatif/handicare/",
    "monte-escaliers/comparatif/independance-royale/index.html":
        "https://solutionssenior.fr/monte-escaliers/comparatif/independance-royale/",
    "monte-escaliers/comparatif/lehner-lifttechnik/index.html":
        "https://solutionssenior.fr/monte-escaliers/comparatif/lehner-lifttechnik/",
    "monte-escaliers/comparatif/mobilae/index.html":
        "https://solutionssenior.fr/monte-escaliers/comparatif/mobilae/",
    "monte-escaliers/comparatif/otolift/index.html":
        "https://solutionssenior.fr/monte-escaliers/comparatif/otolift/",
    "monte-escaliers/comparatif/platinum-stairlifts/index.html":
        "https://solutionssenior.fr/monte-escaliers/comparatif/platinum-stairlifts/",
    "monte-escaliers/comparatif/stannah/index.html":
        "https://solutionssenior.fr/monte-escaliers/comparatif/stannah/",
    "monte-escaliers/comparatif/thyssenkrupp-home-solutions/index.html":
        "https://solutionssenior.fr/monte-escaliers/comparatif/thyssenkrupp-home-solutions/",
}

updated = 0

for path, url in PAGES.items():
    if not os.path.exists(path):
        print(f"  ⚠  Non trouvé : {path}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'rel="canonical"' in content:
        print(f"  ✓  Déjà présent : {path}")
        continue

    canonical = f'  <link rel="canonical" href="{url}">\n'
    content = content.replace("</head>", canonical + "</head>", 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✓  {path}")
    updated += 1

print(f"\n{'─'*50}")
print(f"  {updated} pages mises à jour")
