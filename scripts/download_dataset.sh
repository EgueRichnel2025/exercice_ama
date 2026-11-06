#!/usr/bin/env bash

set -euo pipefail

# Configuration du dataset
DATASET="heesoo37/120-years-of-olympic-history-athletes-and-results"
FILENAME="athlete_events.csv"
DESTINATION="data/raw"

# Se placer à la racine du projet
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=========================================="
echo " AMA PIIA C2 - Téléchargement des données"
echo "=========================================="

# Vérifier le CLI Kaggle
if ! command -v kaggle >/dev/null 2>&1; then
    echo "Installation du CLI Kaggle..."
    python -m pip install kaggle
fi

# Créer le dossier de destination
mkdir -p "$DESTINATION"

# Éviter un téléchargement inutile
if [[ -s "$DESTINATION/$FILENAME" ]]; then
    echo "Le fichier existe déjà : $DESTINATION/$FILENAME"
    exit 0
fi

# Télécharger uniquement le fichier demandé
echo "Téléchargement de $FILENAME depuis Kaggle..."

kaggle datasets download "$DATASET" \
    --file "$FILENAME" \
    --path "$DESTINATION" \
    --unzip

# Vérifier le résultat
if [[ ! -s "$DESTINATION/$FILENAME" ]]; then
    echo "ERREUR : le fichier CSV est introuvable après téléchargement."
    exit 1
fi

echo ""
echo "Téléchargement terminé avec succès !"
echo "Fichier : $DESTINATION/$FILENAME"
echo "Taille : $(du -h "$DESTINATION/$FILENAME" | cut -f1)"
echo ""
