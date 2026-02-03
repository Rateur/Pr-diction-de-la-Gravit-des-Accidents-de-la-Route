<div align="center">

# Prédiction de la Gravité des Accidents de la Route

### Analyse, Modélisation et Déploiement Docker

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-valdevprs-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/valdevprs/accident-app)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

</div>

---

## À Propos

Projet Machine Learning dédié à la prédiction de la gravité des accidents de la route à partir des données BAAC. Le dépôt contient les données, les notebooks d'analyse et de préparation, ainsi qu'une application FastAPI + Streamlit pour l'inférence.

---

## Source des Données

Les données utilisées proviennent de la base BAAC (Bulletins d'Analyse des Accidents Corporels) mise à disposition par le Ministère de l'Intérieur :

**[Bases de données annuelles des accidents corporels (2005-2024)](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)**

### Récupération et emplacement des données

Le dossier `data/` n'est pas versionné et n'est pas présent sur GitHub. Vous devez le créer à la racine du projet, puis y placer les fichiers téléchargés depuis data.gouv avec les noms attendus :

- `data/caracteristiques.csv`
- `data/lieux.csv`
- `data/usagers.csv`

Astuce : vous pouvez télécharger une année spécifique (ex. 2024) puis renommer les fichiers en respectant ces noms.

---

## Stack Technique

<div align="center">

<table>
<tr>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="60" height="60"/><br/>
<b>Python 3.12</b><br/>
<sub>Langage principal</sub>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="60" height="60"/><br/>
<b>Docker & Docker Compose</b><br/>
<sub>Conteneurisation</sub>
</td>
<td align="center" width="25%">
<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="60" height="60"/><br/>
<b>FastAPI, Uvicorn, Pydantic, Requests</b><br/>
<sub>API & client HTTP</sub>
</td>
<td align="center" width="25%">
<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="60" height="60"/><br/>
<b>Streamlit</b><br/>
<sub>Interface web interactive</sub>
</td>
</tr>
<tr>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" width="60" height="60"/><br/>
<b>Pandas & NumPy</b><br/>
<sub>Traitement des données</sub>
</td>
<td align="center" width="25%">
<img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" width="60" height="60"/><br/>
<b>Scikit-learn & Joblib</b><br/>
<sub>Modélisation & sérialisation</sub>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/matplotlib/matplotlib-original.svg" width="60" height="60"/><br/>
<b>Matplotlib, Seaborn, Missingno</b><br/>
<sub>EDA & visualisation</sub>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jupyter/jupyter-original.svg" width="60" height="60"/><br/>
<b>Jupyter & ipykernel</b><br/>
<sub>Notebooks</sub>
</td>
</tr>
</table>

</div>

---

## Notebooks d'Analyse

<div align="center">

| Fichier | Description | Ordre d'exécution |
|---------|-------------|-------------------|
| `01_Exploration_Donnees.ipynb` | Analyse exploratoire des données (EDA) | 1 |
| `02_Nettoyage_Feature_Engineering.ipynb` | Nettoyage et préparation des données | 2 |
| `03_Modelisation_Evaluation.ipynb` | Entraînement et évaluation des modèles | 3 |

</div>

---

## Architecture du Dépôt

```text
accident_dla_route/
├── notebooks/
│   ├── 01_Exploration_Donnees.ipynb
│   ├── 02_Nettoyage_Feature_Engineering.ipynb
│   └── 03_Modelisation_Evaluation.ipynb
├── interface/
│   ├── main.py                 # API FastAPI
│   └── app.py                  # Interface Streamlit
├── model/
│   ├── colonnes_modele.joblib
│   └── modele_gravite_rf.joblib
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

Dossiers locaux non versionnés (à créer) :

```text
data/
├── caracteristiques.csv   # À télécharger
├── lieux.csv              # À télécharger
├── usagers.csv            # À télécharger
├── accidents_clean.csv    # Généré par notebook
└── accidents_scored.csv   # Généré par notebook
```

---

## Installation & Utilisation

<details>
<summary><strong>CAS A - Utilisation via Docker Hub (Recommandé)</strong></summary>

<br/>

Méthode recommandée pour tester rapidement l'application sans cloner le dépôt. L'image Docker contient l'API et l'interface.

**Prérequis :** Docker installé.

### Windows (PowerShell)

Créer un fichier `docker-compose.yml` avec le contenu suivant :

```yaml
version: '3.8'

services:
  api:
    image: valdevprs/accident-app:v1.0
    container_name: accident-api_prod
    environment:
      - ENV=production
    ports:
      - "8000:8000"
    networks:
      - accident-network
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 10s
      timeout: 5s
      retries: 5

  frontend:
    image: valdevprs/accident-app:v1.0
    container_name: accident-front_prod
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://api:8000
    networks:
      - accident-network
    depends_on:
      - api
    command: streamlit run interface/app.py --server.port 8501 --server.address 0.0.0.0

networks:
  accident-network:
    driver: bridge
```

Puis exécuter :

```powershell
docker compose up
```

### Linux / WSL / macOS (Bash)

Créer le même fichier `docker-compose.yml`, puis lancer :

```bash
docker compose up
```

### Accès

- **Interface Streamlit :** [http://localhost:8501](http://localhost:8501)
- **Documentation API :** [http://localhost:8000/docs](http://localhost:8000/docs)

### Arrêter l'application
```bash
docker compose down
```

</details>

<details>
<summary><strong>CAS B - Installation Développement (Via Git)</strong></summary>

<br/>

Méthode destinée aux développeurs souhaitant modifier le code.

### Windows (PowerShell)

```powershell
git clone <URL_DU_REPO>
cd accident_dla_route
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Linux / WSL / macOS (Bash)

```bash
git clone <URL_DU_REPO>
cd accident_dla_route
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Lancer les notebooks

Les notebooks sont dans `notebooks/`.

```bash
pip install jupyter
jupyter lab
```

### Lancer l'API et l'interface sans Docker

**API :**
```bash
python -m uvicorn interface.main:app --reload --port 8000
```

**Front :**
```bash
streamlit run interface/app.py
```

</details>

---

## Détails Techniques

### Colonnes Attendues par le Modèle

<div align="center">

| Catégorie | Features |
|-----------|----------|
| **Temporelles** | `mois`, `jour`, `heure` |
| **Conditions** | `lum`, `atm`, `surf` |
| **Localisation** | `agg`, `int`, `catr`, `circ`, `nbv`, `vosp`, `prof`, `plan`, `infra`, `situ`, `env1` |
| **Infrastructure** | `lartpc`, `larrout`, `vma` |
| **Collision** | `col` |
| **Usagers** | `nb_usagers`, `nb_pietons`, `pct_pietons` |
| **Détection** | `anomaly_score` |

</div>

**Total :** 25 features

### Format d'entrée API

L'API attend un JSON avec les 25 features ci-dessus. Exemple :
```json
{
  "mois": 6,
  "jour": 15,
  "lum": 1,
  ...
}
```

### Sortie du Modèle

Le modèle effectue une classification **binaire** de la gravité des accidents :

- **Classe prédite :** 
  - `0` = Accident non grave (indemne ou blessé léger)
  - `1` = Accident grave (blessé hospitalisé ou tué)
- **Probabilité :** Score de confiance pour la classe positive (grave), valeur entre 0 et 1
- **Remarque :** Si le modèle n'est pas chargé, l'API renvoie un résultat de secours avec `mock: true`
