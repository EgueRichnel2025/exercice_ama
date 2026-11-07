"""Nettoyage contrôlé du dataset historique des athlètes olympiques."""

from pathlib import Path
import pandas as pd

RAW_PATH = Path("data/raw/athlete_events.csv")
OUTPUT_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = OUTPUT_DIR / "athlete_events_cleaned.csv"

print("=" * 65)
print("       NETTOYAGE DU DATASET OLYMPIQUE")
print("=" * 65)

# 1. Chargement du fichier original.
df = pd.read_csv(RAW_PATH)

initial_rows = len(df)
initial_columns = len(df.columns)
initial_missing = int(df.isna().sum().sum())
initial_exact_duplicates = int(df.duplicated().sum())

print("\n1. ÉTAT INITIAL")
print(f"Nombre de lignes : {initial_rows:,}")
print(f"Nombre de colonnes : {initial_columns}")
print(f"Doublons exacts : {initial_exact_duplicates:,}")
print(f"Valeurs manquantes : {initial_missing:,}")

# 2. Suppression des doublons strictement identiques.
cleaned_df = df.drop_duplicates().copy()

removed_rows = initial_rows - len(cleaned_df)

print("\n2. DÉDUPLICATION")
print(f"Lignes supprimées : {removed_rows:,}")
print(f"Lignes conservées : {len(cleaned_df):,}")

# 3. Vérification des données manquantes.
final_missing = int(cleaned_df.isna().sum().sum())

print("\n3. CONTRÔLE DES VALEURS MANQUANTES")
print(f"Valeurs manquantes initiales : {initial_missing:,}")
print(f"Valeurs manquantes finales : {final_missing:,}")

# 4. Vérification des répétitions métier.
business_key = ["ID", "Games", "Event"]

remaining_business_duplicates = int(
    cleaned_df.duplicated(subset=business_key).sum()
)

print("\n4. CONTRÔLE DES RÉPÉTITIONS MÉTIER")
print(
    "Occurrences supplémentaires conservées : "
    f"{remaining_business_duplicates:,}"
)

# 5. Export du dataset nettoyé.
cleaned_df.to_csv(OUTPUT_PATH, index=False)

# 6. Bilan comparatif.
summary = pd.DataFrame([
    {
        "Indicateur": "Nombre de lignes",
        "Avant": initial_rows,
        "Après": len(cleaned_df),
    },
    {
        "Indicateur": "Nombre de colonnes",
        "Avant": initial_columns,
        "Après": len(cleaned_df.columns),
    },
    {
        "Indicateur": "Doublons exacts",
        "Avant": initial_exact_duplicates,
        "Après": int(cleaned_df.duplicated().sum()),
    },
    {
        "Indicateur": "Valeurs manquantes",
        "Avant": initial_missing,
        "Après": final_missing,
    },
    {
        "Indicateur": "Répétitions métier supplémentaires",
        "Avant": int(df.duplicated(subset=business_key).sum()),
        "Après": remaining_business_duplicates,
    },
])

summary.to_csv(
    REPORT_DIR / "cleaning_comparison.csv",
    index=False
)

# 7. Vérifications finales.
assert len(cleaned_df) == initial_rows - initial_exact_duplicates
assert cleaned_df.duplicated().sum() == 0
assert cleaned_df.columns.tolist() == df.columns.tolist()

print("\n5. VALIDATION")
print("Aucun doublon exact restant.")
print("Les colonnes originales sont conservées.")
print("Les valeurs manquantes n'ont pas été imputées.")
print("Les répétitions métier ont été conservées.")

print("\n" + "=" * 65)
print("NETTOYAGE TERMINÉ")
print(f"Dataset : {OUTPUT_PATH}")
print(f"Bilan : {REPORT_DIR / 'cleaning_comparison.csv'}")
print("=" * 65)
