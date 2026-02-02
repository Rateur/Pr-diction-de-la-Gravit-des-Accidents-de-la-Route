# Accident de la route - Analyse & Prediction

Projet d'analyse des accidents routiers (BAAC) avec pipeline complet :
- Exploration et visualisation des donnees
- Nettoyage et feature engineering
- Detection d anomalies (Isolation Forest)
- Modelisation de la gravite (Random Forest)
- API FastAPI + Interface Streamlit

## Structure
- `01_Exploration_Donnees.ipynb` : EDA, qualite des donnees, premiers constats
- `02_Nettoyage_Feature_Engineering.ipynb` : nettoyage, features, export datasets propres
- `03_Modelisation_Evaluation.ipynb` : entrainement, evaluation, sauvegarde modele
- `interface/main.py` : API FastAPI (`/health`, `/predict`)
- `interface/app.py` : UI Streamlit (formulaire + prediction)

## Prerequis
- Python 3.10+ (recommande 3.12)
- Un environnement virtuel (venv)

## Installation
```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Execution des notebooks
Lancer Jupyter et executer dans l'ordre :
1. `01_Exploration_Donnees.ipynb`
2. `02_Nettoyage_Feature_Engineering.ipynb`
3. `03_Modelisation_Evaluation.ipynb`

## Lancer l'API (FastAPI)
```bash
python -m uvicorn interface.main:app --reload --port 8000
```

Docs API :
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Lancer l'interface (Streamlit)
Dans un autre terminal :
```bash
streamlit run interface/app.py
```
L'URL s'affiche dans le terminal (souvent `http://localhost:8501`).

## A noter
- Les jeux de donnees bruts/transformes sont volumineux et exclus du repo.
- Le modele est regenere via le notebook `03_Modelisation_Evaluation.ipynb`.

## Colonnes attendues par le modele
```
['mois', 'jour', 'lum', 'agg', 'int', 'atm', 'col', 'catr', 'circ', 'nbv', 'vosp', 'prof',
 'plan', 'lartpc', 'larrout', 'surf', 'infra', 'situ', 'env1', 'vma', 'nb_usagers',
 'nb_pietons', 'pct_pietons', 'heure', 'anomaly_score']
```
