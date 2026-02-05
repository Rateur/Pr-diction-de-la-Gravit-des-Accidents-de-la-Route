from typing import List, Dict

# Colonnes utilisées par le modèle
FEATURE_COLUMNS: List[str] = [
    "mois", "jour", "lum", "agg", "int", "atm", "col", "catr", "circ", "nbv",
    "vosp", "prof", "plan", "lartpc", "larrout", "surf", "infra", "situ",
    "env1", "vma", "nb_usagers", "nb_pietons", "pct_pietons", "heure",
    "anomaly_score",
]

# Options pour l'interface utilisateur (Streamlit)
MONTHS: Dict[int, str] = {
    1: "Janvier", 2: "Fevrier", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
    7: "Juillet", 8: "Aout", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Decembre",
}

LUM_OPTIONS: Dict[int, str] = {
    1: "Plein jour",
    2: "Crepuscule ou aube",
    3: "Nuit sans eclairage public",
    4: "Nuit avec eclairage public non allume",
    5: "Nuit avec eclairage public allume",
}

AGG_OPTIONS: Dict[int, str] = {
    1: "Hors agglomeration",
    2: "En agglomeration",
}

INT_OPTIONS: Dict[int, str] = {
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

ATM_OPTIONS: Dict[int, str] = {
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

COL_OPTIONS: Dict[int, str] = {
    -1: "Non renseigne",
    1: "Deux vehicules - frontale",
    2: "Deux vehicules - arriere",
    3: "Deux vehicules - cote",
    4: "Trois vehicules+ - en chaine",
    5: "Trois vehicules+ - collisions multiples",
    6: "Autre collision",
    7: "Sans collision",
}

CATR_OPTIONS: Dict[int, str] = {
    1: "Autoroute",
    2: "Route nationale",
    3: "Route departementale",
    4: "Voie communale",
    5: "Hors reseau public",
    6: "Parc de stationnement",
    7: "Routes de metropole urbaine",
    9: "Autre",
}

CIRC_OPTIONS: Dict[int, str] = {
    -1: "Non renseigne",
    1: "A sens unique",
    2: "Bidirectionnelle",
    3: "A chaussees separees",
    4: "Voies d affectation variable",
}

VOSP_OPTIONS: Dict[int, str] = {
    -1: "Non renseigne",
    0: "Sans objet",
    1: "Piste cyclable",
    2: "Bande cyclable",
    3: "Voie reservee",
}

PROF_OPTIONS: Dict[int, str] = {
    -1: "Non renseigne",
    1: "Plat",
    2: "Pente",
    3: "Sommet de cote",
    4: "Bas de cote",
}

PLAN_OPTIONS: Dict[int, str] = {
    -1: "Non renseigne",
    1: "Partie rectiligne",
    2: "Courbe a gauche",
    3: "Courbe a droite",
    4: "En S",
}

SURF_OPTIONS: Dict[int, str] = {
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

INFRA_OPTIONS: Dict[int, str] = {
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

SITU_OPTIONS: Dict[int, str] = {
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

ENV1_OPTIONS: Dict[int, str] = {
    0: "Code 0",
    3: "Code 3",
    99: "Code 99",
}
