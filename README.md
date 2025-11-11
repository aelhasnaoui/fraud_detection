# Fraud Detection

This repository contains a demonstration service implementing a full fraud-detection pipeline.

## Main components
- `scripts/download_dataset.py` : helper script to download the raw CSV into `data/` (requires a configured credentials file; see script docstring).
- `scripts/preprocess.py` : reads `data/creditcard.csv` and writes `data/processed_data.csv`. It applies a StandardScaler to `Amount` and drops `Time`.
- `scripts/train_model.py` : trains a RandomForestClassifier (n_estimators=100), saves the trained model to `models/random_forest_model.pkl` using `joblib.dump`, and writes visual artifacts to `results/` (`feature_importance.png`, `confusion_matrix.png`, `class_distribution.png`).
- `scripts/app.py` : Flask API exposing POST `/predict`. Loads the model from `models/random_forest_model.pkl` and expects a JSON with features in the order `V1..V28, Amount`.
- `Dockerfile` : builds a Python 3.11 image, installs dependencies, and starts Gunicorn targeting `scripts.app:app`.
- `Procfile` : example process file (see "Important notes" below for a recommended change before platform deploy).

## Installation
Install project dependencies:

```bash
pip install -r requirements.txt
```

## Typical local workflows
- Download raw data (if applicable and configured):

```bash
python scripts/download_dataset.py
```

- Preprocess raw CSV into a training-ready CSV:

```bash
python scripts/preprocess.py
```

- Train the model and generate results:

```bash
python scripts/train_model.py
```

- Run the Flask server for development:

```bash
python -m scripts.app
```

- Run production-like server with Gunicorn (same command used in `Dockerfile`):

```bash
gunicorn --bind 0.0.0.0:5000 scripts.app:app
```

## `/predict` API
- Endpoint: POST `/predict`
- Input: a JSON object containing all numeric features. The server enforces the following feature ordering: `V1, V2, ..., V28, Amount` (see `EXPECTED_FEATURES` in `scripts/app.py`).
- Output: JSON with `{"prediction": 0}` or `{"prediction": 1}`. If a feature is missing the API returns a 400 with the missing key.

Minimal example (curl):

```bash
curl -X POST http://localhost:5000/predict \
	-H "Content-Type: application/json" \
	-d '{"V1":0.1, "V2":-0.2, "V3":0.0, "V4":..., "Amount":1.23}'
```

Note: `scripts/app.py` explicitly reorders columns with `df = df[EXPECTED_FEATURES]` before prediction.

## Important notes / gotchas
- `Procfile` currently contains `web: gunicorn -w 4 -b 0.0.0.0:10000 app:app`, which does not match the `Dockerfile` (which runs `scripts.app:app` on port 5000). For Heroku or similar, use:

```text
web: gunicorn -w 4 -b 0.0.0.0:$PORT scripts.app:app
```

- The download helper expects a credentials file when running external downloads; ensure any required credentials are present on the host.
- There are no automated tests in the repository. Adding at least unit tests for `preprocess.py` and an integration test for `/predict` is recommended.

## Contributor suggestions
- If you change feature columns or their order during preprocessing/training, update `EXPECTED_FEATURES` in `scripts/app.py` and regenerate `models/random_forest_model.pkl`.
- Keep model artifacts under `models/` and visual outputs under `results/`. If the model interface changes, include a migration or versioning note in the repo.

## FAQ
- Where is the model stored? `models/random_forest_model.pkl`.
- How to run the app locally? See "Typical local workflows" above.

---

