# ============================================
# Image de base (version de linux et python)
# ============================================

FROM python:3.12-slim

LABEL maintainer="valentinperies007@gmail.com"
LABEL version="1.0"
LABEL description="Dockerfile for a Python 3.12 application"

# ============================================
# Configuration de l'environnement
# ============================================

WORKDIR /app

# ============================================
# Installation des dépendances
# ============================================

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ============================================
# Copie du code source
# ============================================

COPY interface/ ./interface/
COPY model/ ./model/

# ============================================
# Configuration finale
# ============================================

# Les ports 
EXPOSE 8000
EXPOSE 8501

# Commande pour lancer l'application
CMD ["uvicorn", "interface.main:app", "--host", "0.0.0.0", "--port", "8000"]

