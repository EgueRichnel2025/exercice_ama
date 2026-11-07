"""Analyse détaillée des valeurs manquantes du dataset olympique."""

from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/raw/athlete_events.csv")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Les variables physiques et démographiques à étudier.
columns = ["Age", "Height", "Weight"]

print("=" * 65)
print("       ANALYSE APPROFONDIE DES VALEURS MANQUANTES")
print("=" * 65)

# 1. Taux de valeurs manquantes par variable.
print("\n1. TAUX GLOBAL DE VALEURS MANQUANTES")

missing_global = pd.DataFrame({
    "Valeurs_manquantes": df[columns].isna().sum(),
    "Pourcentage": (df[columns].isna().mean() * 100).round(2),
})

print(missing_global.to_string())

# 2. Valeurs manquantes selon les périodes olympiques.
print("\n2. VALEURS MANQUANTES PAR PÉRIODE")

df["Periode"] = pd.cut(
    df["Year"],
    bins=[1890, 1920, 1950, 1980, 2000, 2020],
    labels=[
        "1896-1920",
        "1921-1950",
        "1951-1980",
        "1981-2000",
        "2001-2016",
    ],
    include_lowest=True,
)

missing_by_period = (
    df.groupby("Periode", observed=False)[columns]
    .agg(lambda group: group.isna().mean() * 100)
    .round(2)
)

print(missing_by_period.to_string())

# 3. Valeurs manquantes selon les sports.
print("\n3. SPORTS AVEC LE PLUS DE DONNÉES PHYSIQUES MANQUANTES")

missing_by_sport = (
    df.groupby("Sport")[columns]
    .agg(lambda group: group.isna().mean() * 100)
    .round(2)
)

missing_by_sport["Nombre_participations"] = (
    df.groupby("Sport").size()
)

missing_by_sport = missing_by_sport.sort_values(
    by="Nombre_participations",
    ascending=False,
)

print(missing_by_sport.head(20).to_string())

# 4. Évolution des données manquantes par année.
print("\n4. TAUX DE DONNÉES MANQUANTES PAR ANNÉE")

missing_by_year = (
    df.groupby("Year")[columns]
    .agg(lambda group: group.isna().mean() * 100)
    .round(2)
)

print(missing_by_year.head(10).to_string())
print("...")
print(missing_by_year.tail(10).to_string())

# 5. Exporter les résultats.
missing_global.to_csv(
    REPORT_DIR / "missing_values_global.csv"
)

missing_by_period.to_csv(
    REPORT_DIR / "missing_values_by_period.csv"
)

missing_by_sport.to_csv(
    REPORT_DIR / "missing_values_by_sport.csv"
)

missing_by_year.to_csv(
    REPORT_DIR / "missing_values_by_year.csv"
)

print("\n" + "=" * 65)
print("ANALYSE TERMINÉE")
print("Rapports enregistrés dans reports/")
print("=" * 65)
