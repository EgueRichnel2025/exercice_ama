# AMA PIIA C2 — Nettoyage des données olympiques

## 1. Présentation

Projet réalisé dans le cadre de l'exercice de nettoyage des données
de l'Académie des Mathématiques Appliquées (AMA), PIIA Cohorte 2,
spécialisation Machine Learning.

**Binôme :**
- EGUE Richnel
- AVADRA Martial

**Domaine :** Sport — Jeux olympiques.

Le projet porte sur le jeu de données
*120 years of Olympic history: athletes and results*,
qui couvre les participations aux Jeux olympiques de 1896 à 2016.

## 2. Objectifs

L'objectif est de diagnostiquer la qualité des données, de justifier
les corrections et de produire un fichier nettoyé.

Les analyses portent notamment sur :
- L'âge, la taille et le poids des athlètes.
- Les médailles obtenues.
- Les participations par sport et par pays.
- L'évolution historique des données.

## 3. Source des données

Dataset Kaggle :
https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results

Fichier utilisé : `athlete_events.csv`.

Le fichier original est conservé localement dans `data/raw/`.

## 4. Résultats du nettoyage

| Indicateur | Avant | Après |
|---|---:|---:|
| Nombre de lignes | 271 116 | 269 731 |
| Nombre de colonnes | 15 | 15 |
| Doublons exacts supplémentaires | 1 385 | 0 |
| Valeurs manquantes | 363 853 | 359 615 |
| Répétitions métier supplémentaires | 1 480 | 95 |

### Décisions méthodologiques

- **Doublons exacts :** suppression des 1 385 occurrences
  supplémentaires strictement identiques.
- **Répétitions métier :** conservation lorsqu'elles peuvent
  représenter des résultats sportifs distincts.
- **Âge, taille et poids manquants :** conservation sans
  imputation artificielle.
- **Médaille manquante :** conservation, car cela signifie
  généralement que l'athlète n'a pas remporté de médaille.
- **Valeurs atypiques :** conservation provisoire. Une observation
  statistiquement atypique n'est pas nécessairement une erreur.

### Observations atypiques détectées par IQR

| Variable | Nombre de candidats |
|---|---:|
| Age | 10 317 |
| Height | 1 338 |
| Weight | 3 237 |

Ces nombres correspondent à des lignes de participation,
pas nécessairement à des athlètes distincts.

## 5. Livrables

- Notebook Jupyter documenté en français.
- Dataset nettoyé au format CSV.
- Rapports d'analyse et de comparaison.
- Visualisations des données.
- Scripts Python reproductibles.

## 6. Installation

Créer un environnement virtuel avec `python -m venv .venv`.

Activer l'environnement sous Git Bash avec
`source .venv/Scripts/activate`.

Installer les dépendances avec
`python -m pip install -r requirements.txt`.

Le fichier original doit être placé dans
`data/raw/athlete_events.csv`.

Le script `scripts/download_dataset.sh` permet également de télécharger
le jeu de données lorsque l'environnement Kaggle est configuré.

## 7. Exécution des analyses

Depuis la racine du projet :

**Audit initial :** `python scripts/inspect_dataset.py`

**Analyse des doublons :**
- `python scripts/analyze_duplicates.py`
- `python scripts/inspect_duplicate_conflicts.py`

**Analyse des valeurs manquantes :**
`python scripts/analyze_missing_values.py`

**Nettoyage :** `python scripts/clean_dataset.py`

Le fichier nettoyé est enregistré dans
`data/processed/athlete_events_cleaned.csv`.

## 8. Notebook principal

Lancer JupyterLab avec `jupyter lab`, puis ouvrir :

`notebooks/01_nettoyage_athletes_olympiques.ipynb`

Ce notebook rassemble le diagnostic, les analyses exploratoires,
les décisions de nettoyage et les contrôles de qualité.

## 9. Organisation du projet

- `data/raw/` : données originales non versionnées.
- `data/processed/` : données nettoyées.
- `notebooks/` : notebook d'analyse et de nettoyage.
- `reports/` : rapports et visualisations.
- `scripts/` : scripts Python d'analyse et de nettoyage.

## 10. Conclusion

Le nettoyage a permis de supprimer les doublons strictement identiques
tout en préservant les informations historiques utiles.

La démarche privilégie la traçabilité des transformations,
la justification des décisions et la conservation des observations
qui ne sont pas confirmées comme erronées.
