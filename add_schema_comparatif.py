"""
add_schema_comparatif.py — Ajoute schema.org sur les 9 pages comparatif
À lancer depuis la racine du projet :
  python3 add_schema_comparatif.py
"""
import os
import json
from datetime import date

today = date.today().strftime("%Y-%m-%d")

PAGES = [
    {
        "path": "monte-escaliers/comparatif/acorn/index.html",
        "url": "https://solutionssenior.fr/monte-escaliers/comparatif/acorn/",
        "headline": "Monte-escalier Acorn : avis, prix et gamme complète 2026",
        "description": "Tout savoir sur Acorn Stairlifts : modèles, prix, avis clients et SAV en France.",
        "brand": "Acorn",
    },
    {
        "path": "monte-escaliers/comparatif/handicare/index.html",
        "url": "https://solutionssenior.fr/monte-escaliers/comparatif/handicare/",
        "headline": "Monte-escalier Handicare : avis, prix et gamme complète 2026",
        "description": "Tout savoir sur Handicare : modèles, prix, avis clients et SAV en France.",
        "brand": "Handicare",
    },
    {
        "path": "monte-escaliers/comparatif/independance-royale/index.html",
        "url": "https://solutionssenior.fr/monte-escaliers/comparatif/independance-royale/",
        "headline": "Monte-escalier Indépendance Royale : avis, prix et gamme 2026",
        "description": "Tout savoir sur Indépendance Royale : modèles, prix, avis clients et SAV en France.",
        "brand": "Indépendance Royale",
    },
    {
        "path": "monte-escaliers/comparatif/lehner-lifttechnik/index.html",
        "url": "https://solutionssenior.fr/monte-escaliers/comparatif/lehner-lifttechnik/",
        "headline": "Monte-escalier Lehner Lifttechnik : avis, prix et gamme 2026",
        "description": "Tout savoir sur Lehner Lifttechnik : modèles, prix, avis clients et SAV en France.",
        "brand": "Lehner Lifttechnik",
    },
    {
        "path": "monte-escaliers/comparatif/mobilae/index.html",
        "url": "https://solutionssenior.fr/monte-escaliers/comparatif/mobilae/",
        "headline": "Monte-escalier Mobilae : avis, prix et gamme 2026",
        "description": "Tout savoir sur Mobilae : modèles, prix, avis clients et SAV en France.",
        "brand": "Mobilae",
    },
    {
        "path": "monte-escaliers/comparatif/otolift/index.html",
        "url": "https://solutionssenior.fr/monte-escaliers/comparatif/otolift/",
        "headline": "Monte-escalier Otolift : avis, prix et gamme 2026",
        "description": "Tout savoir sur Otolift : modèles, prix, avis clients et SAV en France.",
        "brand": "Otolift",
    },
    {
        "path": "monte-escaliers/comparatif/platinum-stairlifts/index.html",
        "url": "https://solutionssenior.fr/monte-escaliers/comparatif/platinum-stairlifts/",
        "headline": "Monte-escalier Platinum Stairlifts : avis, prix et gamme 2026",
        "description": "Tout savoir sur Platinum Stairlifts : modèles, prix, avis clients et SAV en France.",
        "brand": "Platinum Stairlifts",
    },
    {
        "path": "monte-escaliers/comparatif/stannah/index.html",
        "url": "https://solutionssenior.fr/monte-escaliers/comparatif/stannah/",
        "headline": "Stannah monte-escalier : avis, prix et gamme complète 2026",
        "description": "Tout savoir sur Stannah : modèles, prix, avis clients et SAV en France.",
        "brand": "Stannah",
    },
    {
        "path": "monte-escaliers/comparatif/thyssenkrupp-home-solutions/index.html",
        "url": "https://solutionssenior.fr/monte-escaliers/comparatif/thyssenkrupp-home-solutions/",
        "headline": "Monte-escalier Thyssenkrupp TK Home Solutions : avis, prix et gamme 2026",
        "description": "Tout savoir sur Thyssenkrupp TK Home Solutions : modèles, prix, avis clients et SAV en France.",
        "brand": "Thyssenkrupp",
    },
]

def build_schema(page):
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": page["headline"],
                "description": page["description"],
                "dateModified": today,
                "author": {"@type": "Organization", "name": "Solutions Senior"},
                "publisher": {
                    "@type": "Organization",
                    "name": "Solutions Senior",
                    "url": "https://solutionssenior.fr"
                },
                "mainEntityOfPage": {"@type": "WebPage", "@id": page["url"]}
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://solutionssenior.fr/"},
                    {"@type": "ListItem", "position": 2, "name": "Monte-escalier", "item": "https://solutionssenior.fr/monte-escaliers/"},
                    {"@type": "ListItem", "position": 3, "name": "Comparatif marques", "item": "https://solutionssenior.fr/monte-escaliers/comparatif/"},
                    {"@type": "ListItem", "position": 4, "name": page["brand"], "item": page["url"]}
                ]
            }
        ]
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)

updated = 0

for page in PAGES:
    path = page["path"]

    if not os.path.exists(path):
        print(f"  ⚠  Non trouvé : {path}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "application/ld+json" in content:
        print(f"  ✓  Déjà présent : {path}")
        continue

    schema_block = f'  <script type="application/ld+json">\n{build_schema(page)}\n  </script>\n'
    content = content.replace("</head>", schema_block + "</head>", 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✓  {path}")
    updated += 1

print(f"\n{'─'*50}")
print(f"  {updated} pages mises à jour")
