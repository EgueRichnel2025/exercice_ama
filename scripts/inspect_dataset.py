"""Audit initial du dataset historique des athlètes olympiques."""

from pathlib import Path

import pandas as pd

# Chemins
DATA_PATH = Path("data/raw/athlete_events.csv")
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Vérification du fichier
if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset introuvable : {DATA_PATH}")

# Chargement sans modification du fichier original
df = pd.read_csv(DATA_PATH)

print("=" * 65)
print("       AMA PIIA C2 — AUDIT INITIAL DES DONNÉES OLYMPIQUES")
print("=" * 65)

# 1. Dimensions
print("\n1. DIMENSIONS")
print(f"Nombre de lignes   : {df.shape[0]:,}")
print(f"Nombre de colonnes : {df.shape[1]}")

# 2. Types de données
print("\n2. TYPES DE DONNÉES")
print(df.dtypes)

# 3. Valeurs manquantes
print("\n3. VALEURS MANQUANTES")

missing = pd.DataFrame({
    "Valeurs_manquantes": df.isnull().sum(),
    "Pourcentage": (df.isnull().mean() * 100).round(2),
})

print(missing.to_string())

# 4. Doublons
print("\n4. DOUBLONS")

exact_duplicates = df.duplicated().sum()

print(f"Doublons exacts : {exact_duplicates:,}")

# 5. Statistiques descriptives
print("\n5. STATISTIQUES DESCRIPTIVES")

print(df.describe(include="all").T.to_string())

# 6. Valeurs potentiellement aberrantes
print("\n6. VALEURS POTENTIELLEMENT ABERRANTES")

for column in ["Age", "Height", "Weight"]:
    series = df[column].dropna()

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = series[(series < lower) | (series > upper)]

    print(f"\n{column}")
    print(f"Minimum : {series.min()}")
    print(f"Maximum : {series.max()}")
    print(f"Valeurs potentiellement aberrantes : {len(outliers):,}")
    print(f"Bornes IQR : [{lower:.2f}, {upper:.2f}]")

# 7. Répartition des médailles
print("\n7. RÉPARTITION DES MÉDAILLES")
print(df["Medal"].value_counts(dropna=False))

# 8. Sauvegarde des résultats de l'audit
missing.to_csv(REPORT_DIR / "missing_values_before.csv")

summary = pd.DataFrame({
    "Indicateur": [
        "Nombre de lignes",
        "Nombre de colonnes",
        "Doublons exacts",
        "Valeurs manquantes totales",
    ],
    "Valeur": [
        len(df),
        len(df.columns),
        exact_duplicates,
        int(df.isnull().sum().sum()),
    ],
})

summary.to_csv(REPORT_DIR / "initial_audit_summary.csv", index=False)

print("\n" + "=" * 65)
print("AUDIT TERMINÉ")
print("Rapports enregistrés dans le dossier reports/")
print("=" * 65)
