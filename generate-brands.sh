#!/bin/bash

# ============================================================
# Script de génération des pages single-brand monte-escalier
# Usage : bash generate-brands.sh
# ============================================================

TEMPLATE="monte-escaliers/comparatif/stannah/index.html"
BASE_DIR="monte-escaliers/comparatif"

# Données des marques : "slug|Nom|Pays|Emoji|Fondé|Note|NbAvis|PrixDroit|SiteUrl|TelSAV|TrustpilotUrl|Accroche"
MARQUES=(
  "handicare|Handicare|Suède|🇸🇪|1886|N/D|N/D (Trustpilot FR)|3 500–6 000 €|https://www.handicare-monte-escaliers.fr|Non disponible|https://fr.trustpilot.com/review/handicare.fr|Pionnier suédois fondé en 1886, présent dans 50 pays. Large gamme droit et tournant avec bonne ergonomie."
  "otolift|Otolift|Pays-Bas|🇳🇱|1968|3,9/5|~542 avis|3 200–5 000 €|https://www.otolift.fr|Non disponible|https://fr.trustpilot.com/review/otolift.fr|Fabricant intégré hollandais depuis 1968. Rail monorail le plus fin du marché (57mm). Prix compétitifs avec financement 36 mois sans frais."
  "thyssenkrupp-home-solutions|Thyssenkrupp|Allemagne|🇩🇪|1999|4,8/5|~1 300 avis|3 500–6 000 €|https://homesolutions.tkelevator.com/fr-fr|Non disponible|https://fr.trustpilot.com/review/homesolutions.tkelevator.com|Filiale spécialisée de ThyssenKrupp. Fiabilité industrielle et design soigné. Meilleure note Trustpilot de la catégorie."
  "acorn|Acorn|Royaume-Uni|🇬🇧|1992|3,7/5|~43 avis FR|3 000–4 500 €|https://www.acornmonteescalier.fr|Non disponible|https://fr.trustpilot.com/review/acornmonteescalier.fr|Bon rapport qualité/prix. Note internationale 4,8/5 sur 11 000 avis. Délais d'installation rapides."
  "independance-royale|Indépendance Royale|France|🇫🇷|2003|4,4/5|~2 068 avis|3 000–5 000 €|https://www.independanceroyale.com|Non disponible|https://fr.trustpilot.com/review/www.independanceroyale.com|Marque française fondée à Limoges en 2003. Plus de 100 000 clients équipés. Proximité et réactivité SAV."
  "platinum-stairlifts|Platinum Stairlifts|Royaume-Uni|🇬🇧|2000|N/D|N/D (Trustpilot FR)|4 000–7 000 €|https://www.platinum-stairlifts.fr|Non disponible|https://fr.trustpilot.com/review/platinum-stairlifts.fr|Gamme premium et sur-mesure. Positionnement haut de gamme avec finitions soignées."
  "lehner-lifttechnik|Lehner Lifttechnik|Allemagne|🇩🇪|1950|N/D|N/D (Trustpilot FR)|3 500–6 000 €|https://www.lehner-lifttechnik.de|Non disponible|https://fr.trustpilot.com/review/lehner-lifttechnik.fr|Ingénierie allemande reconnue. Technicité et durabilité. Idéal pour les configurations d'escaliers complexes."
  "mobilae|Mobilae|Pays-Bas|🇳🇱|1990|4,1/5|~1 385 avis|3 200–5 500 €|https://www.mobilae.fr|Non disponible|https://fr.trustpilot.com/review/mobilae.fr|Présence européenne forte. Gamme complète droit, tournant et extérieur avec entretien annuel inclus."
)

echo "🚀 Génération des pages single-brand..."
echo ""

for MARQUE in "${MARQUES[@]}"; do
  IFS='|' read -r SLUG NOM PAYS EMOJI FONDE NOTE NB_AVIS PRIX_DROIT SITE_URL TEL_SAV TRUSTPILOT_URL ACCROCHE <<< "$MARQUE"

  DEST="$BASE_DIR/$SLUG/index.html"

  # Vérifier que le dossier existe
  if [ ! -d "$BASE_DIR/$SLUG" ]; then
    echo "⚠️  Dossier manquant : $BASE_DIR/$SLUG — création automatique..."
    mkdir -p "$BASE_DIR/$SLUG"
  fi

  # Copier le template
  cp "$TEMPLATE" "$DEST"

  # Remplacer les valeurs — Slug/Logo
  sed -i '' "s|/assets/images/marques/stannah.png|/assets/images/marques/$SLUG.png|g" "$DEST"
  sed -i '' "s|alt=\"Logo Stannah\"|alt=\"Logo $NOM\"|g" "$DEST"

  # Title et meta
  sed -i '' "s|Stannah monte-escalier : avis, prix et gamme complète 2026|$NOM monte-escalier : avis, prix et gamme complète 2026|g" "$DEST"
  sed -i '' "s|Tout savoir sur Stannah|Tout savoir sur $NOM|g" "$DEST"

  # Breadcrumb
  sed -i '' "s|<span>Stannah</span>|<span>$NOM</span>|g" "$DEST"

  # H1
  sed -i '' "s|Monte-escalier Stannah : avis, prix et gamme 2026|Monte-escalier $NOM : avis, prix et gamme 2026|g" "$DEST"

  # Accroche hero
  sed -i '' "s|Pionnier britannique fondé en 1867, Stannah est la marque de référence du monte-escalier en Europe avec plus de 750 000 installations réalisées.|$ACCROCHE|g" "$DEST"

  # Note et avis
  sed -i '' "s|4,6/5</span>|$NOTE</span>|g" "$DEST"
  sed -i '' "s|1 600 avis</span>|$NB_AVIS</span>|g" "$DEST"

  # Site officiel
  sed -i '' "s|https://www.stannah.fr|$SITE_URL|g" "$DEST"
  sed -i '' "s|🌐 Site officiel|🌐 Site officiel|g" "$DEST"
  sed -i '' "s|stannah.fr</a>|$SITE_URL</a>|g" "$DEST"

  # Quick info bar
  sed -i '' "s|🇬🇧 <strong>Origine</strong> : Royaume-Uni|$EMOJI <strong>Origine</strong> : $PAYS|g" "$DEST"
  sed -i '' "s|<strong>Fondé en</strong> : 1867|<strong>Fondé en</strong> : $FONDE|g" "$DEST"
  sed -i '' "s|href=\"tel:0800304050\">0800 30 40 50|href=\"tel:\">$TEL_SAV|g" "$DEST"

  # Trustpilot
  sed -i '' "s|https://fr.trustpilot.com/review/stannah.fr|$TRUSTPILOT_URL|g" "$DEST"
  sed -i '' "s|Stannah sur Trustpilot|$NOM sur Trustpilot|g" "$DEST"

  # H2 présentation
  sed -i '' "s|Qui est Stannah ?|Qui est $NOM ?|g" "$DEST"

  # CTA bas de page
  sed -i '' "s|Vous intéresse par Stannah ?|Intéressé par $NOM ?|g" "$DEST"
  sed -i '' "s|Obtenez un devis gratuit et comparez avec d'autres installateurs agréés.|Obtenez un devis gratuit et comparez $NOM avec d'autres marques.|g" "$DEST"

  # Sidebar devis
  sed -i '' "s|Comparez Stannah avec d'autres marques|Comparez $NOM avec d'autres marques|g" "$DEST"

  # Prix indicatif droit
  sed -i '' "s|3 500 – 5 500 €|$PRIX_DROIT|g" "$DEST"

  # Fiche technique — Pays d'origine
  sed -i '' "s|🇬🇧 Royaume-Uni</span>|$EMOJI $PAYS</span>|g" "$DEST"

  # Année de fondation
  sed -i '' "s|<span class=\"critere-value\">1867</span>|<span class=\"critere-value\">$FONDE</span>|g" "$DEST"

  echo "✅  $NOM → $DEST"
done

echo ""
echo "🎉 Terminé ! $(echo "${#MARQUES[@]}") pages générées."
echo ""
echo "👉 Prochaine étape :"
echo "   git add . && git commit -m \"Ajout pages marques monte-escaliers\" && git push"
