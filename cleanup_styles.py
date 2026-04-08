"""
cleanup_styles.py — Deux actions :
1. Remplace le <style> interne des 9 pages comparatif par un <link> vers comparatif.css
2. Supprime le <style> interne des 8 pages article 100% nettoyables

À lancer depuis la racine du projet :
  python3 cleanup_styles.py
"""
import re
import os

# ── 1. Pages comparatif → remplacer style par link ─────────────────────────
COMPARATIF_PAGES = [
    "monte-escaliers/comparatif/acorn/index.html",
    "monte-escaliers/comparatif/handicare/index.html",
    "monte-escaliers/comparatif/independance-royale/index.html",
    "monte-escaliers/comparatif/lehner-lifttechnik/index.html",
    "monte-escaliers/comparatif/mobilae/index.html",
    "monte-escaliers/comparatif/otolift/index.html",
    "monte-escaliers/comparatif/platinum-stairlifts/index.html",
    "monte-escaliers/comparatif/stannah/index.html",
    "monte-escaliers/comparatif/thyssenkrupp-home-solutions/index.html",
]

COMPARATIF_LINK = '  <link rel="stylesheet" href="/assets/comparatif.css">'

# ── 2. Pages article 100% nettoyables ──────────────────────────────────────
CLEANABLE_PAGES = [
    "monte-escaliers/ceinture-de-securite/index.html",
    "monte-escaliers/monte-charge/index.html",
    "monte-escaliers/escalier-colimacon/index.html",
    "monte-escaliers/droit/index.html",
    "monte-escaliers/exterieur/index.html",
    "monte-escaliers/pourquoi-les-monte-escaliers-ont-des-telecommandes/index.html",
    "monte-escaliers/tournant/index.html",
    "monte-escaliers/poids-maximum/index.html",
]

def remove_style_block(content):
    """Supprime le bloc <style>...</style> complet."""
    return re.sub(r'\n?\s*<style>.*?</style>\n?', '\n', content, flags=re.DOTALL)

def replace_style_with_link(content, link):
    """Remplace le bloc <style> par un <link> vers le CSS externe."""
    # Vérifier que le link n'est pas déjà là
    if link.strip() in content:
        return content, False
    content = re.sub(r'\n?\s*<style>.*?</style>\n?', f'\n{link}\n', content, flags=re.DOTALL)
    return content, True

updated_comparatif = 0
updated_clean = 0
errors = []

print("=== 1. Pages comparatif → link vers comparatif.css ===")
for path in COMPARATIF_PAGES:
    if not os.path.exists(path):
        print(f"  ⚠  Non trouvé : {path}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "<style>" not in content:
        print(f"  ✓  Déjà propre : {path}")
        continue
    new_content, changed = replace_style_with_link(content, COMPARATIF_LINK)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  ✓  {path}")
        updated_comparatif += 1

print(f"\n=== 2. Pages article 100% nettoyables ===")
for path in CLEANABLE_PAGES:
    if not os.path.exists(path):
        print(f"  ⚠  Non trouvé : {path}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "<style>" not in content:
        print(f"  ✓  Déjà propre : {path}")
        continue
    new_content = remove_style_block(content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  ✓  {path}")
    updated_clean += 1

print(f"\n{'─'*50}")
print(f"  {updated_comparatif} pages comparatif → comparatif.css")
print(f"  {updated_clean} pages article nettoyées")
print(f"\n⚠  N'oubliez pas de copier comparatif.css dans assets/ avant le git push")
