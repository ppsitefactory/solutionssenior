import os
import glob

FAVICON_TAGS = """  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">"""

# Trouver tous les fichiers HTML du projet (récursif)
html_files = glob.glob("**/*.html", recursive=True)

updated = 0
skipped = 0

for path in html_files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Déjà traité ?
    if "favicon.svg" in content:
        skipped += 1
        continue

    # Insérer avant </head>
    if "</head>" not in content:
        print(f"  ⚠  Pas de </head> trouvé : {path}")
        continue

    new_content = content.replace("</head>", f"{FAVICON_TAGS}\n</head>", 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  ✓  {path}")
    updated += 1

print(f"\n{'─'*50}")
print(f"  {updated} fichiers mis à jour")
print(f"  {skipped} déjà traités")
