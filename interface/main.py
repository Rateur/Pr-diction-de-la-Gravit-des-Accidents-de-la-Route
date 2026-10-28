from pathlib import Path
from typing import List

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict

from interface.constants import FEATURE_COLUMNS

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "modele_gravite_rf.joblib"
COLS_PATH = BASE_DIR / "model" / "colonnes_modele.joblib"


class AccidentFeatures(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    mois: int = Field(..., ge=1, le=12, description="Mois de l accident")
    jour: int = Field(..., ge=1, le=31, description="Jour de l accident")
    lum: int = Field(..., description="Luminosite")
    agg: int = Field(..., description="Agglomeration")
    int_: int = Field(..., alias="int", description="Intersection")
    atm: int = Field(..., description="Conditions atmospheriques")
    col: int = Field(..., description="Type de collision")
    catr: int = Field(..., description="Categorie de route")
    circ: int = Field(..., description="Regime de circulation")
    nbv: int = Field(..., description="Nombre de voies")
    vosp: int = Field(..., description="Voie reservee")
    prof: int = Field(..., description="Profil en long")
    plan: int = Field(..., description="Trace en plan")
    lartpc: float = Field(..., description="Largeur TPC")
    larrout: float = Field(..., description="Largeur chaussee")
    surf: int = Field(..., description="Etat de surface")
    infra: int = Field(..., description="Infrastructure")
    situ: int = Field(..., description="Situation")
    env1: float = Field(..., description="Environnement")
    vma: float = Field(..., description="Vitesse max autorisee")
    nb_usagers: int = Field(..., ge=0, description="Nombre d usagers")
    nb_pietons: int = Field(..., ge=0, description="Nombre de pietons")
    pct_pietons: float = Field(..., ge=0.0, le=1.0, description="Part de pietons")
    heure: int = Field(..., ge=0, le=23, description="Heure (0-23)")
    anomaly_score: float = Field(..., description="Score d anomalie")


app = FastAPI(title="Accidents API", version="1.0")


model = None
columns = FEATURE_COLUMNS
model_loaded = False

try:
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        model_loaded = True
    if COLS_PATH.exists():
        columns = joblib.load(COLS_PATH)
except Exception:
    model = None
    model_loaded = False


def to_dataframe(payload: AccidentFeatures, cols: List[str]) -> pd.DataFrame:
    data = payload.model_dump(by_alias=True)
    row = {col: data.get(col) for col in cols}
    return pd.DataFrame([row], columns=cols)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model_loaded,
        "columns": columns,
    }


@app.post("/predict")
def predict(payload: AccidentFeatures):
    X = to_dataframe(payload, columns)

    # Sans modèle, pas de réponse inventée : le client doit savoir que la prédiction n'existe pas.
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Modèle non chargé : exécutez notebooks/03_Modelisation_Evaluation.ipynb pour créer model/.")

    try:
        pred = int(model.predict(X)[0])
    except Exception as exc:
        raise HTTPException(status_code=500, detail="La prédiction a échoué.") from exc

    if model is not None and hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(X)[0][1])
    else:
        proba = float(pred)

    return {
        "prediction": pred,
        "probability": proba,
        "model_loaded": True,
    }
