from fastapi.testclient import TestClient

import interface.main as api

client = TestClient(api.app)

ACCIDENT = {
    "mois": 6, "jour": 14, "lum": 1, "agg": 2, "int": 1, "atm": 1, "col": 3, "catr": 3, "circ": 2,
    "nbv": 2, "vosp": 0, "prof": 1, "plan": 1, "lartpc": 0.0, "larrout": 7.0, "surf": 1, "infra": 0,
    "situ": 1, "env1": 0.0, "vma": 80.0, "nb_usagers": 2, "nb_pietons": 0, "pct_pietons": 0.0,
    "heure": 17, "anomaly_score": 0.1,
}


def test_health_dit_si_le_modele_est_charge():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["model_loaded"] is api.model_loaded


def test_predict_sans_modele_repond_503(monkeypatch):
    monkeypatch.setattr(api, "model_loaded", False)
    r = client.post("/predict", json=ACCIDENT)
    assert r.status_code == 503
    assert "Modèle non chargé" in r.json()["detail"]


def test_predict_refuse_une_entree_invalide():
    r = client.post("/predict", json={**ACCIDENT, "heure": 25})
    assert r.status_code == 422


def test_predict_avec_un_modele(monkeypatch):
    class Modele:
        def predict(self, X):
            return [1]

        def predict_proba(self, X):
            return [[0.2, 0.8]]

    monkeypatch.setattr(api, "model", Modele())
    monkeypatch.setattr(api, "model_loaded", True)
    r = client.post("/predict", json=ACCIDENT)
    assert r.status_code == 200
    assert r.json() == {"prediction": 1, "probability": 0.8, "model_loaded": True}
