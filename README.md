# AMA PIIA C2 — Nettoyage des données olympiques

## Présentation

Projet réalisé dans le cadre de l'exercice de nettoyage des données
de l'Académie des Mathématiques Appliquées (AMA), PIIA Cohorte 2,
spécialisation Machine Learning.

## Binôme

- EGUE Richnel
- AVADRA Martial

## Domaine

Sport — Jeux olympiques.

## Objectif

Nettoyer le fichier athlete_events.csv afin de préparer les données
historiques des athlètes ayant participé aux Jeux olympiques.

Les analyses porteront notamment sur :

- L'âge des athlètes.
- La taille et le poids des athlètes.
- La répartition des médailles.
- Les performances par pays.

## Source des données

Kaggle :
https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results

Fichier utilisé : athlete_events.csv.

Période couverte : 1896 à 2016.

## Principes de nettoyage

1. Conserver une copie intacte des données originales.
2. Réaliser un diagnostic avant toute correction.
3. Mesurer les valeurs manquantes et les doublons.
4. Justifier chaque transformation.
5. Comparer les indicateurs avant et après nettoyage.
6. Ne pas supprimer une donnée sans justification.

Attention : une valeur Medal manquante correspond généralement
à un athlète n'ayant remporté aucune médaille. Elle ne doit pas
être automatiquement considérée comme une erreur.

## Structure du projet

- data/raw : données originales.
- data/processed : données nettoyées.
- notebooks : analyse et nettoyage avec Python.
- reports/figures : visualisations et graphiques.

## Installation

Créer un environnement virtuel :

python -m venv .venv

Activer l'environnement :

source .venv/Scripts/activate

Installer les dépendances :

python -m pip install -r requirements.txt

Lancer JupyterLab :

jupyter lab

## Livrables

- Notebook Python commenté en français.
- Fichier CSV nettoyé.
- Comparaison des indicateurs avant et après nettoyage.
