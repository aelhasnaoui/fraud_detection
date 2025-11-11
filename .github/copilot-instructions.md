## But et portée
Ce dépôt héberge un service de détection de fraude entraîné sur le jeu de données Kaggle `mlg-ulb/creditcardfraud`. Ce fichier donne aux agents IA les informations essentielles pour modifier, tester et étendre le projet rapidement.

## Vue d'ensemble (big picture)
- Composants majeurs:
  - `scripts/download_dataset.py` : télécharge le dataset Kaggle (utilise Kaggle API).
  - `scripts/preprocess.py` : nettoie/transforme `data/creditcard.csv` → `data/processed_data.csv` (scale `Amount`, drop `Time`).
  - `scripts/train_model.py` : entraîne un RandomForest, enregistre `models/random_forest_model.pkl` et exporte des visuels dans `results/`.
  - `scripts/app.py` : API Flask exposant `/predict` et charge le modèle depuis `models/random_forest_model.pkl`.
- Déploiement typique : Dockerfile construit une image et lance Gunicorn avec l'application (binding `scripts.app:app`). Le `Procfile` contient une référence différente (`app:app`) — voir note "procfile" ci‑dessous.

## Points de données et flux
- Source raw CSV attendu : `data/creditcard.csv`.
- Préprocessing : `Amount` est standardisé (StandardScaler) et `Time` est supprimé ; la sortie est `data/processed_data.csv` qui contient les colonnes V1..V28, Amount, Class.
- Entraînement : `scripts/train_model.py` sépare X/y, fait `train_test_split`, entraîne RandomForest (n_estimators=100) et sérialise avec `joblib.dump` vers `models/random_forest_model.pkl`.
- Service API : `scripts/app.py` s'attend à un JSON avec toutes les features dans l'ordre attendu; la constante `EXPECTED_FEATURES` précise l'ordre: V1..V28 puis Amount.

## Commandes et workflows locaux (exemples reproductibles)
- Installer dépendances : `pip install -r requirements.txt` (fichier présent à la racine).
- Télécharger dataset (nécessite credentials Kaggle configurés) :
  - `python scripts/download_dataset.py`
- Prétraiter :
  - `python scripts/preprocess.py` (écrit `data/processed_data.csv`)
- Entraîner :
  - `python scripts/train_model.py` (écrit `models/random_forest_model.pkl` et `results/`)
- Lancer le serveur (dev) :
  - `python -m scripts.app` ou `python scripts/app.py` (écoute 0.0.0.0:5000)
- Lancer avec Gunicorn (prod / Dockerfile) :
  - `gunicorn --bind 0.0.0.0:5000 scripts.app:app`

## Attention / pièges connus
- `Procfile` référence `app:app` et le port `10000` ; cela ne concorde pas avec `scripts.app:app` utilisé par le Dockerfile. Si vous déployez sur Heroku ou similaire, mettez à jour `Procfile` pour `web: gunicorn -w 4 -b 0.0.0.0:$PORT scripts.app:app`.
- Le téléchargement Kaggle exige que l'utilisateur ait la configuration Kaggle (`~/.kaggle/kaggle.json`) et permissions.
- L'ordre des features est strict dans l'API `/predict`. Les requêtes doivent fournir V1..V28 et Amount ; sinon la route renvoie une KeyError traitée en 400.

## Conventions de code spécifiques au projet
- Modèles sérialisés : `joblib.dump(model, "models/random_forest_model.pkl")` ; les agents qui modifient la sortie d'entraînement doivent maintenir ce chemin.
- Visualisations : `results/` contient `feature_importance.png`, `confusion_matrix.png`, `class_distribution.png`.
- Pas de suite de tests automatisés présente — ajouter des tests unitaires pour `preprocess_data`, `train_model` et l'endpoint `/predict` est recommandé.

## Points d'intégration externes
- Kaggle API (via `kaggle` package) pour le download.
- Flask + Gunicorn pour l'API.

## Exemples concrets pour l'agent
- Si tu changes les features utilisées pour l'entraînement, mets à jour `scripts/app.py` :
  - modifier `EXPECTED_FEATURES` pour refléter le nouvel ordre/jeu de colonnes.
  - régénérer et committer `models/random_forest_model.pkl` si le format ou l'interface change.
- Si tu modifies le `Procfile` ou la configuration de port, ajoute un commentaire dans `Procfile` expliquant pourquoi (compatibilité Heroku vs Dockerfile).

## Demandes de suivi
- Veux-tu que j'ajoute des tests unitaires basiques pour `preprocess_data` et l'endpoint `/predict` ?
