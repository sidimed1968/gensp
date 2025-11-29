# Dockerfile pour déployer l'application Streamlit
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Installer les dépendances système requises
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier requirements et installer
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier l'application
COPY . /app

# Créer un répertoire pour stocker les données et définir HOME pour le fichier Excel
RUN mkdir -p /app/data
ENV HOME=/app/data

EXPOSE 8501

# Port configurable via variable d'environnement PORT
ENV PORT=8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
