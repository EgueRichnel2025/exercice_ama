"""Étude des répétitions métier après déduplication exacte."""

from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/raw/athlete_events.csv")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Suppression théorique des doublons strictement identiques.
# Le fichier original reste intact.
df_unique = df.drop_duplicates().copy()

business_key = ["ID", "Games", "Event"]

# Identifier les groupes contenant plusieurs lignes pour une même clé.
repeated = df_unique[
    df_unique.duplicated(subset=business_key, keep=False)
].copy()

print("=" * 65)
print("ANALYSE DES RÉPÉTITIONS MÉTIER APRÈS DÉDUPLICATION")
print("=" * 65)

print(f"\nLignes initiales : {len(df):,}")
print(f"Après déduplication exacte : {len(df_unique):,}")
print(f"Lignes dans les groupes répétés : {len(repeated):,}")

# Examiner les différences dans les groupes répétés.
columns_to_check = [
    "Name", "Sex", "Age", "Height", "Weight",
    "Team", "NOC", "Year", "Season", "City",
    "Sport", "Medal"
]

variation = (
    repeated.groupby(business_key, dropna=False)[columns_to_check]
    .nunique(dropna=False)
)

conflicting_groups = variation[
    (variation > 1).any(axis=1)
]

print(f"\nGroupes présentant au moins une différence : {len(conflicting_groups):,}")

if not conflicting_groups.empty:
    print("\nExemples de groupes présentant des différences :")

    examples = repeated.merge(
        conflicting_groups.reset_index()[business_key],
        on=business_key,
        how="inner"
    )

    print(
        examples.sort_values(business_key)
        .head(30)
        .to_string(index=False)
    )

# Enregistrer les répétitions métier pour étude.
repeated.to_csv(
    REPORT_DIR / "business_repetitions_after_exact_dedup.csv",
    index=False
)

conflicting_groups.to_csv(
    REPORT_DIR / "business_conflicting_groups.csv"
)

print("\nRapports enregistrés dans reports/")
print("=" * 65)
