import json
import os

import requests
import streamlit as st

st.set_page_config(
    page_title="Accidents - Prediction Gravite",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600&family=Spectral:wght@400;600&display=swap');

:root {
    --ink: #0f172a;
    --accent: #0b4f6c;
    --accent-2: #1985a1;
    --paper: #f7f9fc;
    --gold: #f2d492;
}

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.main {
    background: radial-gradient(1200px 600px at 10% -10%, #eef5ff 0%, transparent 60%),
                radial-gradient(800px 400px at 90% 10%, #f7f1e1 0%, transparent 55%),
                var(--paper);
}

.block-container {
    padding-top: 2.5rem;
}

.hero {
    background: linear-gradient(120deg, #ffffff 0%, #f2f7ff 100%);
    border-radius: 18px;
    padding: 24px 28px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    margin-bottom: 20px;
}

.hero h1 {
    font-family: 'Spectral', serif;
    margin: 0 0 6px 0;
    color: var(--ink);
}

.hero p {
    margin: 0;
    color: #475569;
}

.section-title {
    font-family: 'Spectral', serif;
    font-weight: 600;
    margin-top: 8px;
    color: var(--ink);
}

.stButton > button {
    background: var(--accent);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    border: none;
    font-weight: 600;
}

.stButton > button:hover {
    background: var(--accent-2);
    color: white;
}

.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

.result-card {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid #dbe7f3;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
}

.badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.85rem;
}

.badge-success {
    background: #e8f5e9;
    color: #1b5e20;
    border: 1px solid #c8e6c9;
}

.badge-danger {
    background: #ffebee;
    color: #b71c1c;
    border: 1px solid #ffcdd2;
}

.badge-info {
    background: #eef2ff;
    color: #1e3a8a;
    border: 1px solid #c7d2fe;
}

.small-note {
    color: #64748b;
    font-size: 0.9rem;
}
</style>
""",
    unsafe_allow_html=True,
)

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

MONTHS = {
    1: "Janvier",
    2: "Fevrier",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Aout",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Decembre",
}

LUM_OPTIONS = {
    1: "Plein jour",
    2: "Crepuscule ou aube",
    3: "Nuit sans eclairage public",
    4: "Nuit avec eclairage public non allume",
    5: "Nuit avec eclairage public allume",
}

AGG_OPTIONS = {
    1: "Hors agglomeration",
    2: "En agglomeration",
}

INT_OPTIONS = {
    1: "Hors intersection",
    2: "Intersection en X",
    3: "Intersection en T",
    4: "Intersection en Y",
    5: "Intersection > 4 branches",
    6: "Giratoire",
    7: "Place",
    8: "Passage a niveau",
    9: "Autre intersection",
}

ATM_OPTIONS = {
    -1: "Non renseigne",
    1: "Normale",
    2: "Pluie legere",
    3: "Pluie forte",
    4: "Neige / grele",
    5: "Brouillard / fumee",
    6: "Vent fort / tempete",
    7: "Temps eblouissant",
    8: "Temps couvert",
    9: "Autre",
}

COL_OPTIONS = {
    -1: "Non renseigne",
    1: "Deux vehicules - frontale",
    2: "Deux vehicules - arriere",
    3: "Deux vehicules - cote",
    4: "Trois vehicules+ - en chaine",
    5: "Trois vehicules+ - collisions multiples",
    6: "Autre collision",
    7: "Sans collision",
}

CATR_OPTIONS = {
    1: "Autoroute",
    2: "Route nationale",
    3: "Route departementale",
    4: "Voie communale",
    5: "Hors reseau public",
    6: "Parc de stationnement",
    7: "Routes de metropole urbaine",
    9: "Autre",
}

CIRC_OPTIONS = {
    -1: "Non renseigne",
    1: "A sens unique",
    2: "Bidirectionnelle",
    3: "A chaussees separees",
    4: "Voies d affectation variable",
}

VOSP_OPTIONS = {
    -1: "Non renseigne",
    0: "Sans objet",
    1: "Piste cyclable",
    2: "Bande cyclable",
    3: "Voie reservee",
}

PROF_OPTIONS = {
    -1: "Non renseigne",
    1: "Plat",
    2: "Pente",
    3: "Sommet de cote",
    4: "Bas de cote",
}

PLAN_OPTIONS = {
    -1: "Non renseigne",
    1: "Partie rectiligne",
    2: "Courbe a gauche",
    3: "Courbe a droite",
    4: "En S",
}

SURF_OPTIONS = {
    -1: "Non renseigne",
    1: "Normale",
    2: "Mouillee",
    3: "Flaques",
    4: "Inondee",
    5: "Enneigee",
    6: "Boue",
    7: "Verglacee",
    8: "Corps gras / huile",
    9: "Autre",
}

INFRA_OPTIONS = {
    -1: "Non renseigne",
    0: "Aucun",
    1: "Tunnel",
    2: "Pont",
    3: "Bretelle",
    4: "Voie ferree",
    5: "Carrefour amenage",
    6: "Zone pietonne",
    7: "Zone de peage",
    8: "Chantier",
    9: "Autres",
}

SITU_OPTIONS = {
    -1: "Non renseigne",
    0: "Aucun",
    1: "Sur chaussee",
    2: "Bande d arret d urgence",
    3: "Accotement",
    4: "Trottoir",
    5: "Piste cyclable",
    6: "Autre voie speciale",
    8: "Autres",
}

ENV1_OPTIONS = {
    0: "Code 0",
    3: "Code 3",
    99: "Code 99",
}


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
