import csv
import os
import json
from datetime import date

# ── Date du jour ────────────────────────────────────────────────────────────
today = date.today()
date_iso = today.strftime("%Y-%m-%d")
months_fr = {
    1:"janvier", 2:"février", 3:"mars", 4:"avril",
    5:"mai", 6:"juin", 7:"juillet", 8:"août",
    9:"septembre", 10:"octobre", 11:"novembre", 12:"décembre"
}
date_fr = f"{today.day} {months_fr[today.month]} {today.year}"

# ── Prépositions département ─────────────────────────────────────────────────
DEPT_PREP = {
    "Bouches-du-Rhône":      "dans les Bouches-du-Rhône",
    "Haute-Garonne":         "en Haute-Garonne",
    "Alpes-Maritimes":       "dans les Alpes-Maritimes",
    "Loire-Atlantique":      "en Loire-Atlantique",
    "Bas-Rhin":              "dans le Bas-Rhin",
    "Gironde":               "en Gironde",
    "Nord":                  "dans le Nord",
    "Hérault":               "dans l'Hérault",
    "Ille-et-Vilaine":       "en Ille-et-Vilaine",
    "Isère":                 "en Isère",
    "Var":                   "dans le Var",
    "Loire":                 "dans la Loire",
    "Gard":                  "dans le Gard",
    "Côte-d'Or":             "en Côte-d'Or",
    "Maine-et-Loire":        "dans le Maine-et-Loire",
    "Puy-de-Dôme":           "dans le Puy-de-Dôme",
    "Seine-Maritime":        "en Seine-Maritime",
    "Marne":                 "dans la Marne",
    "Finistère":             "dans le Finistère",
    "Haute-Vienne":          "en Haute-Vienne",
    "Indre-et-Loire":        "en Indre-et-Loire",
    "Pyrénées-Orientales":   "dans les Pyrénées-Orientales",
    "Somme":                 "dans la Somme",
    "Moselle":               "en Moselle",
    "Rhône":                 "dans le Rhône",
}

# ── Génération d'une page ────────────────────────────────────────────────────
def generate_page(row):
    ville      = row["ville"]
    slug       = row["slug"]
    dept       = row["dept"]
    dept_num   = row["dept_num"]
    habitants  = row["habitants_approx"]
    contexte   = row["contexte_local"].strip()
    dp         = DEPT_PREP.get(dept, f"dans le {dept}")
    url        = f"https://solutionssenior.fr/monte-escaliers/{slug}/"

    title      = f"Monte-escalier à {ville} — Devis gratuit, installateurs agréés {dp} | Solutions Senior"
    h1         = f"Monte-escalier à {ville}\u00a0: devis gratuit, prix et aides 2026"
    meta_desc  = (f"Trouvez un installateur de monte-escalier agréé à {ville} ({dept}). "
                  f"Devis gratuit sous 24h, aides financières jusqu'à 70\u00a0%, "
                  f"professionnels vérifiés. Guide complet 2026.")

    # ── FAQ ──────────────────────────────────────────────────────────────────
    faqs = [
        {
            "q": f"Quel est le prix d'un monte-escalier à {ville} ?",
            "a": (f"Le prix varie de 3\u00a0000\u00a0€ à 9\u00a0000\u00a0€ selon le type "
                  f"(droit ou tournant), la marque et les options choisies. "
                  f"Plusieurs aides peuvent réduire significativement ce montant selon votre situation.")
        },
        {
            "q": f"Comment trouver un installateur agréé à {ville} ?",
            "a": (f"Solutions Senior vous met en relation gratuitement avec des installateurs "
                  f"certifiés intervenant à {ville} et {dp}. "
                  f"Remplissez le formulaire et un professionnel vous rappelle sous 24h.")
        },
        {
            "q": f"Quelles aides pour un monte-escalier {dp} ?",
            "a": (f"MaPrimeAdapt' (jusqu'à 70\u00a0% des travaux HT, plafond 22\u00a0000\u00a0€ HT), "
                  f"APA, CARSAT (jusqu'à 3\u00a0500\u00a0€) et TVA réduite à 5,5\u00a0%. "
                  f"Le guichet MaPrimeAdapt' est actuellement suspendu, la réouverture est attendue.")
        },
        {
            "q": f"Faut-il faire des travaux pour installer un monte-escalier à {ville} ?",
            "a": (f"Non. L'installation est non-invasive et entièrement réversible. "
                  f"Le rail se fixe sur les marches ou contre le mur, sans percement porteur. "
                  f"C'est particulièrement adapté aux immeubles anciens soumis à des règles de copropriété.")
        },
        {
            "q": f"Mon escalier à {ville} est-il compatible avec un monte-escalier ?",
            "a": (f"Dans la très grande majorité des cas, oui. "
                  f"Même les escaliers étroits et raides peuvent accueillir des modèles compacts "
                  f"à partir de 60\u00a0cm de largeur libre. "
                  f"Un technicien évalue la faisabilité gratuitement lors d'une visite à domicile.")
        },
    ]

    # JSON-LD FAQ entities
    faq_entities = []
    for f in faqs:
        faq_entities.append({
            "@type": "Question",
            "name": f["q"],
            "acceptedAnswer": {"@type": "Answer", "text": f["a"]}
        })

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": f"Monte-escalier à {ville} — Guide complet 2026",
                "description": f"Trouver un installateur de monte-escalier agréé à {ville} ({dept}) : prix, aides financières et mise en relation gratuite.",
                "dateModified": date_iso,
                "author": {"@type": "Organization", "name": "Solutions Senior"},
                "publisher": {"@type": "Organization", "name": "Solutions Senior", "url": "https://solutionssenior.fr"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": url}
            },
            {
                "@type": "FAQPage",
                "mainEntity": faq_entities
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Accueil",        "item": "https://solutionssenior.fr/"},
                    {"@type": "ListItem", "position": 2, "name": "Monte-escalier", "item": "https://solutionssenior.fr/monte-escaliers/"},
                    {"@type": "ListItem", "position": 3, "name": f"Monte-escalier {ville}", "item": url}
                ]
            }
        ]
    }
    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)

    # FAQ HTML
    faq_html = ""
    for f in faqs:
        faq_html += f"""
      <div class="faq-open-item">
        <h3>{f['q']}</h3>
        <p>{f['a']}</p>
      </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <meta property="og:title" content="Monte-escalier à {ville} — Devis gratuit, installateurs agréés | Solutions Senior">
  <meta property="og:description" content="Mise en relation gratuite avec des installateurs de monte-escaliers agréés à {ville}. Réponse sous 24h, aides MaPrimeAdapt' jusqu'à 70\u00a0%.">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="Solutions Senior">
  <link rel="canonical" href="{url}">

  <script type="application/ld+json">
{schema_json}
  </script>

  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/style.css">
</head>

<body
  data-service="monte-escaliers"
  data-ville="{ville}"
  data-dept="{dept}"
  data-dept-num="{dept_num}"
  data-date-maj="{date_fr}"
  data-h1="Monte-escalier à {ville}&nbsp;: devis gratuit, prix et aides 2026">

<div id="site-header"></div>

<div id="hero-local">
  <h1 class="hero-local-h1" style="position:absolute;left:-9999px;visibility:hidden;">Monte-escalier à {ville}&nbsp;: devis gratuit, prix et aides 2026</h1></div>

<div id="bandeau-rea"></div>
<div class="article-layout">

  <aside class="toc">
    <div class="toc-title">📋 Sommaire</div>
    <ul>
      <li><a href="#contexte">{ville} et les monte-escaliers</a></li>
      <li><a href="#types">Types disponibles à {ville}</a></li>
      <li><a href="#prix">Prix à {ville}</a></li>
      <li><a href="#aides">Aides financières</a></li>
      <li><a href="#comment">Comment obtenir un devis</a></li>
      <li><a href="#faq">FAQ</a></li>
    </ul>
  </aside>

  <main>

    <div class="toc-mobile">
      <button class="toc-mobile-toggle">📋 Sommaire <span class="arrow">▼</span></button>
      <div class="toc-mobile-content">
        <ul>
          <li><a href="#contexte">{ville} et les monte-escaliers</a></li>
          <li><a href="#types">Types disponibles</a></li>
          <li><a href="#prix">Prix à {ville}</a></li>
          <li><a href="#aides">Aides financières</a></li>
          <li><a href="#comment">Obtenir un devis</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </div>
    </div>

    <div class="article-content">

      <p>Vous habitez à <strong>{ville}</strong> et souhaitez installer un monte-escalier pour rester chez vous en toute autonomie ? Solutions Senior vous met en relation gratuitement avec des installateurs agréés intervenant à {ville} et {dp} ({dept_num}).</p>

      <div class="highlight-green">
        <div class="highlight-label">💡 En résumé</div>
        <p>Prix à {ville} : <strong>3&nbsp;000&nbsp;€ à 9&nbsp;000&nbsp;€</strong> selon le type. Plusieurs aides peuvent réduire significativement le coût. Mise en relation gratuite, un installateur agréé {dp} vous rappelle sous 24h.</p>
      </div>

      <h2 id="contexte">Monte-escalier à {ville}&nbsp;: le contexte local</h2>

      <div class="visuel-local">
        <img src="/assets/images/{slug}-ville.webp" alt="Vue de {ville}" loading="lazy" width="900" height="450">
      </div>

      <p>{contexte}</p>

      <p>Avec <strong>{habitants} habitants</strong> et une proportion significative de seniors souhaitant rester à domicile, {ville} concentre une forte demande pour l'adaptation du logement. Que votre escalier soit droit, tournant ou extérieur, des solutions existent et un technicien se déplace gratuitement pour évaluer la faisabilité.</p>

      <div class="cta-inline">
        <div class="cta-inline-text">
          <strong>Un projet de monte-escalier à {ville} ?</strong>
          <span>Un installateur agréé {dp} vous rappelle sous 24h, gratuitement.</span>
        </div>
        <button class="btn-cta open-formulaire">Je veux être rappelé →</button>
      </div>

      <h2 id="types">Types de monte-escaliers disponibles à {ville}</h2>

      <p>Tous les types de monte-escaliers sont disponibles et installables à {ville}. Le choix dépend avant tout de la configuration de votre escalier :</p>

      <div class="types-grid">
        <a href="/monte-escaliers/droit/" class="type-card">
          <img src="/assets/images/monte-escalier-droit.png" alt="Monte-escalier droit installé à {ville}">
          <div class="type-card-body">
            <div class="type-card-title">Monte-escalier droit</div>
            <div class="type-card-desc">Escalier sans virage — installation en ½ journée</div>
          </div>
        </a>
        <a href="/monte-escaliers/tournant/" class="type-card">
          <img src="/assets/images/monte-escalier-tournant.png" alt="Monte-escalier tournant installé à {ville}">
          <div class="type-card-body">
            <div class="type-card-title">Monte-escalier tournant</div>
            <div class="type-card-desc">Escalier avec virage(s) — fabriqué sur mesure</div>
          </div>
        </a>
        <a href="/monte-escaliers/exterieur/" class="type-card">
          <img src="/assets/images/monte-escalier-exterieur.png" alt="Monte-escalier extérieur installé à {ville}">
          <div class="type-card-body">
            <div class="type-card-title">Monte-escalier extérieur</div>
            <div class="type-card-desc">Accès extérieur, terrasse, jardin en pente</div>
          </div>
        </a>
      </div>

      <h2 id="prix">Prix d'un monte-escalier à {ville}</h2>

      <p>Les prix à {ville} sont alignés sur les tarifs nationaux. L'installation ne génère pas de surcoût lié à la localisation.</p>

      <table>
        <thead><tr><th>Type</th><th>Prix tout compris (fourniture + pose)</th></tr></thead>
        <tbody>
          <tr><td><a href="/monte-escaliers/droit/">Monte-escalier droit</a></td><td>3&nbsp;000&nbsp;€ – 5&nbsp;000&nbsp;€</td></tr>
          <tr><td><a href="/monte-escaliers/tournant/">Monte-escalier tournant</a></td><td>5&nbsp;000&nbsp;€ – 9&nbsp;000&nbsp;€</td></tr>
          <tr><td><a href="/monte-escaliers/exterieur/">Monte-escalier extérieur</a></td><td>4&nbsp;000&nbsp;€ – 8&nbsp;000&nbsp;€</td></tr>
        </tbody>
      </table>
      <p style="font-size:0.82rem; color:var(--text-light);">Prix indicatifs fourniture + installation. <a href="/monte-escaliers/prix/">Voir le guide complet des prix →</a></p>

      <h2 id="aides">Aides financières pour un monte-escalier à {ville}</h2>

      <p>Les habitants de {ville} peuvent cumuler plusieurs aides pour financer leur monte-escalier. Le montant dépend de votre situation : revenus, type de logement, aides cumulables.</p>

      <div class="cta-inline">
        <div class="cta-inline-text">
          <strong>Quelles aides pour votre situation ?</strong>
          <span>MaPrimeAdapt', CARSAT, APA, TVA 5,5 % — notre guide détaille toutes les aides disponibles en 2026.</span>
        </div>
        <a href="/monte-escaliers/aides/" class="btn-cta">Voir les aides →</a>
      </div>

      <div class="cta-banner">
        <div class="cta-banner-title">Vous avez des questions sur les aides à {ville} ?</div>
        <div class="cta-banner-sub">Un conseiller vous rappelle gratuitement pour faire le point sur votre situation et les financements auxquels vous avez droit.</div>
        <div class="cta-banner-badges">
          <span class="badge">✓ Gratuit</span>
          <span class="badge">✓ Professionnel agréé</span>
          <span class="badge">✓ Réponse sous 24h</span>
        </div>
        <button class="btn-cta-white open-formulaire">Je veux être rappelé gratuitement →</button>
      </div>

      <h2 id="comment">Comment obtenir un devis à {ville} ?</h2>

      <p>Le processus est simple, rapide et entièrement gratuit. Aucune obligation à aucune étape.</p>

      <div class="etapes-grid">
        <div class="etape-item">
          <div class="etape-num">1</div>
          <div class="etape-titre">Décrivez votre projet</div>
          <div class="etape-desc">Remplissez le formulaire en 2 minutes : type d'escalier, code postal, votre situation.</div>
        </div>
        <div class="etape-item">
          <div class="etape-num">2</div>
          <div class="etape-titre">On trouve le bon pro</div>
          <div class="etape-desc">Nous sélectionnons un installateur agréé intervenant à {ville} et {dp} ({dept_num}).</div>
        </div>
        <div class="etape-item">
          <div class="etape-num">3</div>
          <div class="etape-titre">Rappel sous 24h</div>
          <div class="etape-desc">Le professionnel vous contacte pour convenir d'une visite à domicile et établir un devis gratuit.</div>
        </div>
      </div>

      <div class="cta-banner">
        <div class="cta-banner-title">Demandez votre devis gratuit à {ville}</div>
        <div class="cta-banner-sub">Un installateur agréé {dp} vous rappelle sous 24h</div>
        <div class="cta-banner-badges">
          <span class="badge">✓ Gratuit</span>
          <span class="badge">✓ Professionnel agréé</span>
          <span class="badge">✓ Réponse sous 24h</span>
        </div>
        <button class="btn-cta-white open-formulaire">Je veux être rappelé gratuitement →</button>
      </div>

      <h2 id="faq">Questions fréquentes — Monte-escalier à {ville}</h2>
{faq_html}
    </div>
  </main>
</div>

<div id="site-cta"></div>
<div id="site-footer"></div>
<div id="formulaire-modal"></div>
<div id="bandeau-sticky" data-titre="Devis gratuit à {ville}"></div>
<script src="/assets/components.js"></script>

</body>
</html>"""

    return html


# ── Sitemap ──────────────────────────────────────────────────────────────────
def generate_sitemap(villes):
    urls = ""
    for row in villes:
        urls += f"""  <url>
    <loc>https://solutionssenior.fr/monte-escaliers/{row['slug']}/</loc>
    <lastmod>{date_iso}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    villes = []
    with open("villes.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            villes.append(row)

    generated = 0
    errors = []

    for row in villes:
        slug = row["slug"]
        dir_path = os.path.join("monte-escaliers", slug)
        os.makedirs(dir_path, exist_ok=True)
        try:
            html = generate_page(row)
            file_path = os.path.join(dir_path, "index.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  ✓  {row['ville']:20s} → {file_path}")
            generated += 1
        except Exception as e:
            msg = f"  ✗  {row['ville']} : {e}"
            errors.append(msg)
            print(msg)

    sitemap = generate_sitemap(villes)
    with open("sitemap_villes.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)

    print(f"\n{'─'*50}")
    print(f"  {generated}/{len(villes)} pages générées")
    print(f"  sitemap_villes.xml créé")
    if errors:
        print(f"\nErreurs :")
        for e in errors:
            print(e)
