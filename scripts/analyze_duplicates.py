"""Analyse approfondie des doublons du dataset olympique."""

from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/raw/athlete_events.csv")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("=" * 65)
print("       ANALYSE APPROFONDIE DES DOUBLONS")
print("=" * 65)

# 1. Doublons strictement identiques
exact_duplicates = df[df.duplicated(keep=False)]

print("\n1. DOUBLONS EXACTS")
print(f"Lignes concernées : {len(exact_duplicates):,}")
print(f"Occurrences supplémentaires : {df.duplicated().sum():,}")

if not exact_duplicates.empty:
    print("\nExemples :")
    print(exact_duplicates.sort_values(
        by=["ID", "Games", "Event"]
    ).head(10).to_string(index=False))

# 2. Répétitions selon une clé métier
business_key = ["ID", "Games", "Event"]

business_duplicates = df[
    df.duplicated(subset=business_key, keep=False)
]

print("\n2. RÉPÉTITIONS SUR LA CLÉ ID + GAMES + EVENT")
print(f"Lignes concernées : {len(business_duplicates):,}")
print(
    "Occurrences supplémentaires : "
    f"{df.duplicated(subset=business_key).sum():,}"
)

if not business_duplicates.empty:
    print("\nExemples :")
    print(
        business_duplicates.sort_values(business_key)
        .head(20)
        .to_string(index=False)
    )

# 3. Vérification des différences entre les lignes répétées
if not business_duplicates.empty:
    group_sizes = (
        business_duplicates.groupby(business_key, dropna=False)
        .size()
        .sort_values(ascending=False)
    )

    print("\n3. TAILLE DES GROUPES DE RÉPÉTITIONS")
    print(group_sizes.head(15).to_string())

# 4. Enregistrement des résultats
exact_duplicates.to_csv(
    REPORT_DIR / "exact_duplicates.csv",
    index=False
)

business_duplicates.to_csv(
    REPORT_DIR / "business_key_duplicates.csv",
    index=False
)

print("\n" + "=" * 65)
print("ANALYSE TERMINÉE")
print("Fichiers enregistrés dans reports/")
print("=" * 65)
