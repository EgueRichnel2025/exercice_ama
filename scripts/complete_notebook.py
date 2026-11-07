"""Consolidation du notebook final de nettoyage des données olympiques."""

from pathlib import Path
import nbformat as nbf

NOTEBOOK_PATH = Path(
    "notebooks/01_nettoyage_athletes_olympiques.ipynb"
)

if not NOTEBOOK_PATH.exists():
    raise FileNotFoundError(NOTEBOOK_PATH)

nb = nbf.read(NOTEBOOK_PATH, as_version=4)

# Supprimer les éventuelles cellules vides sans contenu ni résultat.
nb.cells = [
    cell
    for cell in nb.cells
    if not (
        cell.cell_type == "code"
        and not cell.source.strip()
        and not cell.get("outputs", [])
    )
]

# Permettre de relancer le script sans ajouter les sections plusieurs fois.
marker = "<!-- CONSOLIDATION NETTOYAGE FINAL -->"

for index, cell in enumerate(nb.cells):
    if marker in cell.source:
        nb.cells = nb.cells[:index]
        break

cells = []

cells.append(nbf.v4.new_markdown_cell(
"""<!-- CONSOLIDATION NETTOYAGE FINAL -->

# PARTIE II — ANALYSE APPROFONDIE ET NETTOYAGE

Cette deuxième partie approfondit le diagnostic initial, définit
les corrections justifiées et vérifie la qualité du fichier produit.

Le fichier original reste notre référence. Les transformations
sont effectuées sur une copie de travail.
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 15. Analyse des valeurs manquantes selon la période historique

L'analyse globale ne suffit pas toujours à comprendre les absences.

Nous étudions donc les taux de valeurs manquantes de l'âge, de la
taille et du poids selon cinq périodes historiques.

Cette analyse permet de vérifier si la complétude des données
évolue avec le temps.
"""
))

cells.append(nbf.v4.new_code_cell(
"""physical_columns = ["Age", "Height", "Weight"]

period_labels = [
    "1896-1920",
    "1921-1950",
    "1951-1980",
    "1981-2000",
    "2001-2016",
]

# Créer une copie pour ne pas modifier le dataset original.
df_period = df.copy()

df_period["Periode"] = pd.cut(
    df_period["Year"],
    bins=[1890, 1920, 1950, 1980, 2000, 2020],
    labels=period_labels,
    include_lowest=True,
)

missing_by_period = (
    df_period.groupby("Periode", observed=False)[physical_columns]
    .agg(lambda column: column.isna().mean() * 100)
    .round(2)
)

print("Pourcentage de valeurs manquantes par période :")
display(missing_by_period)

missing_by_period.to_csv(
    REPORTS_DIR / "missing_values_by_period.csv"
)
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Visualiser l'évolution des valeurs manquantes selon les périodes.
ax = missing_by_period.plot(
    kind="bar",
    figsize=(12, 6),
    width=0.8
)

ax.set_title("Valeurs manquantes selon les périodes olympiques")
ax.set_xlabel("Période")
ax.set_ylabel("Valeurs manquantes (%)")
ax.legend(title="Variables")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""### Interprétation

Les résultats montrent une forte dépendance entre la période historique
et la disponibilité des informations physiques.

Entre 1896 et 1920 :

- 21,57 % des âges sont manquants ;
- 84,54 % des tailles sont manquantes ;
- 87,90 % des poids sont manquants.

Entre 2001 et 2016, ces taux descendent respectivement à 0 %,
0,82 % et 1,52 %.

Cette évolution suggère que les informations physiques étaient
moins systématiquement recueillies ou documentées dans les premières
éditions olympiques.

Une imputation par moyenne globale risquerait donc de masquer
ces différences historiques.
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 16. Analyse des valeurs manquantes selon le sport

Les caractéristiques physiques des athlètes peuvent également
être documentées différemment selon les disciplines.

Nous calculons le pourcentage de valeurs manquantes pour chaque sport,
ainsi que le nombre de participations correspondant.
"""
))

cells.append(nbf.v4.new_code_cell(
"""missing_by_sport = (
    df.groupby("Sport")[physical_columns]
    .agg(lambda column: column.isna().mean() * 100)
    .round(2)
)

missing_by_sport["Nombre_participations"] = (
    df.groupby("Sport").size()
)

missing_by_sport = missing_by_sport.sort_values(
    by="Nombre_participations",
    ascending=False
)

print("Vingt sports ayant le plus de participations :")
display(missing_by_sport.head(20))

missing_by_sport.to_csv(
    REPORTS_DIR / "missing_values_by_sport.csv"
)
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 17. Évolution annuelle des valeurs manquantes

Nous examinons également l'évolution des absences année par année.

Cette analyse complète la comparaison par grandes périodes et permet
d'identifier les années pour lesquelles les informations sont
particulièrement incomplètes.
"""
))

cells.append(nbf.v4.new_code_cell(
"""missing_by_year = (
    df.groupby("Year")[physical_columns]
    .agg(lambda column: column.isna().mean() * 100)
    .round(2)
)

print("Premières années :")
display(missing_by_year.head(10))

print("Dernières années :")
display(missing_by_year.tail(10))

missing_by_year.to_csv(
    REPORTS_DIR / "missing_values_by_year.csv"
)
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 18. Analyse approfondie des répétitions métier

Une même combinaison `ID + Games + Event` peut apparaître plusieurs
fois sans que les lignes soient strictement identiques.

Nous examinons ces répétitions après suppression théorique des
doublons exacts.

Cette vérification est importante, car une même participation peut
présenter des résultats différents, notamment dans certaines
épreuves historiques.
"""
))

cells.append(nbf.v4.new_code_cell(
"""business_key = ["ID", "Games", "Event"]

# Copie dédupliquée utilisée uniquement pour l'analyse.
df_without_exact_duplicates = df.drop_duplicates().copy()

repeated_business = df_without_exact_duplicates[
    df_without_exact_duplicates.duplicated(
        subset=business_key,
        keep=False
    )
].copy()

print("Lignes initiales :", f"{len(df):,}")
print(
    "Après déduplication exacte :",
    f"{len(df_without_exact_duplicates):,}"
)
print(
    "Lignes appartenant à des groupes métier répétés :",
    f"{len(repeated_business):,}"
)

# Identifier les groupes dont certaines informations diffèrent.
columns_to_check = [
    "Name", "Sex", "Age", "Height", "Weight",
    "Team", "NOC", "Year", "Season", "City",
    "Sport", "Medal"
]

business_variation = (
    repeated_business
    .groupby(business_key, dropna=False)[columns_to_check]
    .nunique(dropna=False)
)

conflicting_groups = business_variation[
    (business_variation > 1).any(axis=1)
]

print(
    "Groupes présentant au moins une différence :",
    f"{len(conflicting_groups):,}"
)

display(conflicting_groups.head(15))
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""### Interprétation des répétitions métier

Après suppression des doublons exacts, 184 lignes appartiennent
à des groupes répétés selon la clé `ID + Games + Event`.

Parmi ces groupes, 89 présentent au moins une différence
dans les autres informations.

Certains athlètes apparaissent avec des équipes ou des résultats
différents. Par exemple, un même participant peut avoir obtenu
plusieurs résultats lors d'une épreuve historique.

Il serait donc incorrect de supprimer automatiquement toutes
les lignes partageant cette clé.

**Décision : seules les lignes strictement identiques seront supprimées.**
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 19. Stratégie et justification du nettoyage

Les analyses précédentes nous permettent de définir les règles suivantes.

| Problème identifié | Décision | Justification |
|---|---|---|
| Doublons strictement identiques | Suppression | Aucune information supplémentaire |
| Répétitions métier | Conservation | Résultats ou informations potentiellement distincts |
| Âge manquant | Conservation | Pas d'imputation artificielle |
| Taille manquante | Conservation | Forte dépendance à la période historique |
| Poids manquant | Conservation | Forte dépendance à la période historique |
| Médaille manquante | Conservation | Absence généralement significative de médaille |
| Valeurs atypiques | Conservation provisoire | Une atypie statistique ne prouve pas une erreur |

### Limites du diagnostic IQR

La méthode IQR identifie des valeurs éloignées de la distribution
centrale, sans tenir compte du sexe, du sport ou du contexte historique.

Les nombres d'observations atypiques précédemment obtenus correspondent
à des lignes de participation. Un même athlète peut apparaître
plusieurs fois.

Nous ne supprimons donc aucune observation sur la seule base
de ce diagnostic statistique.
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 20. Application du nettoyage

La seule transformation appliquée est la suppression des doublons
strictement identiques.

Nous conservons les 15 colonnes et les autres observations,
y compris celles qui contiennent des valeurs manquantes.
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Réaliser la déduplication sur une copie du dataset original.
df_clean_expected = df.drop_duplicates().copy()

# Définir le chemin du fichier final.
CLEAN_DATA_PATH = (
    ROOT_DIR / "data" / "processed" / "athlete_events_cleaned.csv"
)

CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

# Exporter le dataset nettoyé.
df_clean_expected.to_csv(
    CLEAN_DATA_PATH,
    index=False
)

# Recharger le fichier exporté pour vérifier le livrable.
df_clean = pd.read_csv(
    CLEAN_DATA_PATH,
    low_memory=False
)

print("Nettoyage terminé.")
print("Fichier :", CLEAN_DATA_PATH)
print("Dimensions :", df_clean.shape)
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 21. Contrôles de qualité après nettoyage

Nous vérifions que :

- Le nombre de lignes correspond à la suppression des seuls doublons exacts.
- Les 15 colonnes originales sont conservées.
- Aucun doublon exact ne subsiste.
- Les répétitions métier restantes sont conservées.
- Aucune imputation n'a été effectuée.
"""
))

cells.append(nbf.v4.new_code_cell(
"""initial_rows = len(df)
final_rows = len(df_clean)

initial_exact_duplicates = int(df.duplicated().sum())
final_exact_duplicates = int(df_clean.duplicated().sum())

initial_missing = int(df.isna().sum().sum())
final_missing = int(df_clean.isna().sum().sum())

initial_business_duplicates = int(
    df.duplicated(subset=business_key).sum()
)

final_business_duplicates = int(
    df_clean.duplicated(subset=business_key).sum()
)

# Vérifications automatisées.
assert df.columns.tolist() == df_clean.columns.tolist()
assert final_rows == initial_rows - initial_exact_duplicates
assert final_exact_duplicates == 0
assert final_business_duplicates == 95

print("Toutes les vérifications sont réussies.")
print("Colonnes conservées :", len(df_clean.columns))
print("Doublons exacts restants :", final_exact_duplicates)
print("Valeurs manquantes finales :", f"{final_missing:,}")
print("Répétitions métier conservées :", final_business_duplicates)
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 22. Comparaison avant et après nettoyage

Nous comparons plusieurs indicateurs afin de mesurer précisément
l'effet de notre intervention.

La diminution des valeurs manquantes résulte de la suppression
de lignes qui contenaient elles-mêmes des valeurs absentes.
Elle ne correspond pas à une imputation.

La diminution des répétitions métier résulte également de la
suppression de certaines lignes strictement identiques.
"""
))

cells.append(nbf.v4.new_code_cell(
"""comparison = pd.DataFrame({
    "Avant nettoyage": [
        initial_rows,
        len(df.columns),
        initial_exact_duplicates,
        initial_missing,
        initial_business_duplicates,
    ],
    "Après nettoyage": [
        final_rows,
        len(df_clean.columns),
        final_exact_duplicates,
        final_missing,
        final_business_duplicates,
    ],
}, index=[
    "Nombre de lignes",
    "Nombre de colonnes",
    "Doublons exacts supplémentaires",
    "Valeurs manquantes",
    "Répétitions métier supplémentaires",
])

display(comparison)

comparison.to_csv(
    REPORTS_DIR / "cleaning_comparison.csv"
)
"""
))

cells.append(nbf.v4.new_code_cell(
"""# Visualisation comparative des dimensions du dataset.
fig, ax = plt.subplots(figsize=(9, 5))

comparison.loc[
    ["Nombre de lignes", "Nombre de colonnes"]
].plot(
    kind="bar",
    ax=ax
)

ax.set_title("Dimensions du dataset avant et après nettoyage")
ax.set_ylabel("Nombre")
ax.set_xlabel("Indicateur")
ax.tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.show()
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 23. Conclusion générale

Le diagnostic et le nettoyage ont permis d'améliorer la qualité
du jeu de données tout en préservant son contenu historique.

Le fichier initial contenait 271 116 lignes et 15 colonnes.

La suppression des 1 385 occurrences supplémentaires correspondant
à des doublons strictement identiques a produit un dataset final
de **269 731 lignes et 15 colonnes**.

Les valeurs manquantes d'âge, de taille et de poids ont été conservées,
car leur remplacement aurait nécessité des hypothèses non suffisamment
justifiées.

Les valeurs absentes de `Medal` ont également été conservées,
car elles indiquent généralement l'absence de médaille.

Les répétitions métier ont été conservées lorsqu'elles correspondaient
à des informations ou résultats distincts. Enfin, les observations
statistiquement atypiques n'ont pas été supprimées automatiquement.

### Résultat final

Le fichier `data/processed/athlete_events_cleaned.csv` constitue
la version nettoyée du jeu de données.

Cette démarche privilégie la traçabilité des transformations,
la justification des décisions et la préservation des informations
historiques.
"""
))

nb.cells.extend(cells)

# Conserver les métadonnées du notebook.
nb.metadata["kernelspec"] = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}
nb.metadata["language_info"] = {
    "name": "python",
}

nbf.write(nb, NOTEBOOK_PATH)

print("Notebook consolidé avec succès.")
print("Fichier :", NOTEBOOK_PATH)
print("Nombre total de cellules :", len(nb.cells))
print("Cellules ajoutées :", len(cells))
