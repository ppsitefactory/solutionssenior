#!/usr/bin/env python3
"""
Injection Google Analytics dans tous les index.html
Usage : python3 inject-analytics.py
"""

import os
import sys

GA_ID = "G-QWFMHNSKW1"

GA_SNIPPET = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{id}');
  </script>""".format(id=GA_ID)

print(f"🚀 Injection Google Analytics ({GA_ID})...")
print()

count = 0
skipped = 0

for root, dirs, files in os.walk("."):
    # Ignorer .git
    dirs[:] = [d for d in dirs if d != ".git"]

    for filename in files:
        if filename != "index.html":
            continue

        filepath = os.path.join(root, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Déjà présent ?
        if "googletagmanager" in content:
            print(f"⏭  Déjà présent : {filepath}")
            skipped += 1
            continue

        # Insérer juste après <head>
        if "<head>" not in content:
            print(f"⚠️  Pas de <head> trouvé : {filepath}")
            continue

        new_content = content.replace("<head>", f"<head>\n{GA_SNIPPET}", 1)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅  Injecté : {filepath}")
        count += 1

print()
print(f"🎉 Terminé ! {count} fichier(s) modifié(s), {skipped} déjà à jour.")
print()
print("👉 Prochaine étape :")
print(f"   git add . && git commit -m \"Ajout Google Analytics {GA_ID}\" && git push")
