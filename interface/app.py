import json
import os

import requests
import streamlit as st

from interface.constants import (
    AGG_OPTIONS,
    ATM_OPTIONS,
    CATR_OPTIONS,
    CIRC_OPTIONS,
    COL_OPTIONS,
    ENV1_OPTIONS,
    INFRA_OPTIONS,
    INT_OPTIONS,
    LUM_OPTIONS,
    MONTHS,
    PLAN_OPTIONS,
    PROF_OPTIONS,
    SITU_OPTIONS,
    SURF_OPTIONS,
    VOSP_OPTIONS,
)
from interface.styles import GLOBAL_CSS

st.set_page_config(
    page_title="Accidents - Prediction Gravite",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown(
    """
<div class="hero">
  <h1>Prediction de gravite - Accidents routiers</h1>
  <p>Interface de saisie pour estimer le risque d accident grave a partir des variables BAAC.</p>
</div>
""",
    unsafe_allow_html=True,
)

DEFAULT_API_URL = os.getenv("API_URL", "http://localhost:8000")
API_URL = st.sidebar.text_input("API URL", DEFAULT_API_URL)

if st.sidebar.button("Health check"):
    try:
        resp = requests.get(f"{API_URL}/health", timeout=5)
        st.sidebar.success(resp.json())
    except Exception as exc:
        st.sidebar.error(f"API indisponible: {exc}")


def select_code(label, options, default=None, help_text=None):
    keys = list(options.keys())
    if default not in keys:
        default = keys[0]
    return st.selectbox(
        label,
        keys,
        index=keys.index(default),
        format_func=lambda x: options[x],
        help=help_text,
    )


with st.form("predict_form"):
    st.markdown("<div class='section-title'>Contexte</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        mois = select_code("Mois", MONTHS, default=1)
        jour = st.number_input("Jour", min_value=1, max_value=31, value=15)
    with c2:
        heure = st.number_input("Heure", min_value=0, max_value=23, value=14)
        lum = select_code("Luminosite", LUM_OPTIONS, default=1)
    with c3:
        atm = select_code("Meteo", ATM_OPTIONS, default=1)
        agg = select_code("Agglomeration", AGG_OPTIONS, default=1)

    st.markdown("<div class='section-title'>Infrastructure et circulation</div>", unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    with c4:
        catr = select_code("Categorie de route", CATR_OPTIONS, default=3)
        circ = select_code("Regime de circulation", CIRC_OPTIONS, default=2)
        nbv = st.number_input("Nombre de voies", min_value=1, max_value=10, value=2)
    with c5:
        vosp = select_code("Voie reservee", VOSP_OPTIONS, default=0)
        prof = select_code("Profil en long", PROF_OPTIONS, default=1)
        plan = select_code("Trace en plan", PLAN_OPTIONS, default=1)
    with c6:
        surf = select_code("Etat de surface", SURF_OPTIONS, default=1)
        infra = select_code("Infrastructure", INFRA_OPTIONS, default=0)
        situ = select_code("Situation", SITU_OPTIONS, default=1)

    st.markdown("<div class='section-title'>Collision et vitesse</div>", unsafe_allow_html=True)
    c7, c8, c9 = st.columns(3)
    with c7:
        intersection = select_code("Intersection", INT_OPTIONS, default=1)
        collision = select_code("Type de collision", COL_OPTIONS, default=1)
    with c8:
        vma = st.number_input("Vitesse max autorisee (km/h)", min_value=10, max_value=130, value=50)
        lartpc = st.number_input("Largeur TPC (m)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    with c9:
        larrout = st.number_input("Largeur chaussee (m)", min_value=0.0, max_value=30.0, value=6.0, step=0.5)
        env1 = select_code("Environnement (env1)", ENV1_OPTIONS, default=0, help_text="Libelles a valider avec votre dictionnaire")

    st.markdown("<div class='section-title'>Exposition</div>", unsafe_allow_html=True)
    c10, c11, c12 = st.columns(3)
    with c10:
        nb_usagers = st.number_input("Nombre d usagers", min_value=1, max_value=50, value=2)
    with c11:
        nb_pietons = st.number_input("Nombre de pietons", min_value=0, max_value=20, value=0)
    with c12:
        pct_pietons = nb_pietons / nb_usagers if nb_usagers else 0.0
        st.metric("Part de pietons", f"{pct_pietons:.1%}")

    anomaly_score = st.number_input(
        "Score d anomalie (si connu)",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.1,
        help="Valeur issue de l Isolation Forest. Laisser a 0 si non disponible.",
    )

    submit = st.form_submit_button("Predire la gravite")

if submit:
    payload = {
        "mois": mois,
        "jour": jour,
        "lum": lum,
        "agg": agg,
        "int": intersection,
        "atm": atm,
        "col": collision,
        "catr": catr,
        "circ": circ,
        "nbv": nbv,
        "vosp": vosp,
        "prof": prof,
        "plan": plan,
        "lartpc": lartpc,
        "larrout": larrout,
        "surf": surf,
        "infra": infra,
        "situ": situ,
        "env1": env1,
        "vma": vma,
        "nb_usagers": nb_usagers,
        "nb_pietons": nb_pietons,
        "pct_pietons": pct_pietons,
        "heure": heure,
        "anomaly_score": anomaly_score,
    }

    try:
        resp = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        if resp.status_code != 200:
            st.error(f"Erreur API: {resp.status_code} - {resp.text}")
        else:
            data = resp.json()
            pred = int(data.get("prediction", 0))
            proba = float(data.get("probability", 0.0))

            label = "Accident grave probable" if pred == 1 else "Accident non grave probable"
            badge_class = "badge-danger" if pred == 1 else "badge-success"
            badge_text = "Risque eleve" if pred == 1 else "Risque faible"

            c_left, c_right = st.columns([1.1, 0.9])
            with c_left:
                st.markdown(
                    f"""
<div class='result-card'>
  <div class='badge {badge_class}'>{badge_text}</div>
  <h2 style='margin: 12px 0 6px 0; color: #0f172a;'>{label}</h2>
  <p style='margin: 0; color: #475569;'>Probabilite estimee pour la classe grave.</p>
  <h3 style='margin-top: 10px; color: #0b4f6c;'>{proba * 100:.1f}%</h3>
</div>
""",
                    unsafe_allow_html=True,
                )
                st.progress(min(max(proba, 0.0), 1.0))

            with c_right:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("Resume technique")
                st.write(f"Prediction binaire: {pred} (1 = grave, 0 = non grave)")
                st.write(f"Probabilite brute: {proba:.4f}")
                model_state = "charge" if data.get("model_loaded") else "mock"
                st.markdown(
                    f"<span class='badge badge-info'>Modele {model_state}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
    except Exception as exc:
        st.error(f"Echec de la requete: {exc}")
        st.code(json.dumps(payload, indent=2))

st.markdown("<p class='small-note'>Astuce: vous pouvez verifier l API via le bouton Health check dans la sidebar.</p>", unsafe_allow_html=True)
