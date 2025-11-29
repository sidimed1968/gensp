# Déploiement de l'application `gensp`

Ce document explique comment déployer l'application Streamlit localement (Docker) et sur des plateformes comme Heroku / Render.

---

## Prérequis
- Docker & Docker Compose (si vous utilisez Docker)
- Python 3.8+ & pip (si vous déployez directement)

---

## Option 1 — Docker (recommandée)

1. Construire l'image Docker :

```bash
docker build -t gensp:latest .
```

2. Lancer avec Docker Compose (crée un volume local `./data` pour la DB et le fichier Excel) :

```bash
docker-compose up -d --build
```

3. Accéder à l'application via :
```
http://localhost:8501
```

4. Contenu persistant :
- Les fichiers SQLite et Excel sont stockés dans `./data` (montage dans le container)

5. Pour arrêter :

```bash
docker-compose down
```

---

## Option 2 — Déployer sur Heroku (ou autres PaaS compatibles)

- Assurez-vous d'avoir :
  - Un `Procfile` (déjà présent)
  - `requirements.txt` à jour

Étapes rapides :

```bash
# Installer l'outil heroku si nécessaire
heroku login
heroku create nom-de-votre-app
heroku buildpacks:set heroku/python
# Push du repo
git push heroku main
```

Heroku démarre l'application via le `Procfile`. Assurez-vous que la variable d'environnement `PORT` est utilisée (Heroku la définit automatiquement).

Notes : Heroku impose des contraintes d'espace disque (filesystem éphémère). Pour la persistance, utilisez un addon (S3, ou un service de BD comme PostgreSQL) ou stockez SQLite dans un bucket externe, mais ce n'est pas recommandé pour la production.

---

## Option 3 — Render / Railway / Fly.io

Ces plateformes acceptent des apps Docker ou Python. Le `Dockerfile` fourni marche directement sur Render.

- Sur Render : créer un service Web -> déployer à partir du repo -> sélectionner Dockerfile -> configurer les variables d'environnement si nécessaire (LOGEMENTS_DB_PATH, LOGEMENTS_EXCEL_PATH).

---

## Option 4 — Déploiement sur un serveur Linux (systemd)

1. Créer un utilisateur `gensp` :

```bash
sudo useradd -m -s /bin/bash gensp
sudo mkdir -p /var/gensp/data
sudo chown -R gensp:gensp /var/gensp/data
```

2. Copier les fichiers dans `/var/gensp` et installer les dépendances :

```bash
python3 -m venv /var/gensp/venv
source /var/gensp/venv/bin/activate
pip install -r requirements.txt
```

3. Créer un service systemd `/etc/systemd/system/gensp.service` :

```
[Unit]
Description=Gensp Streamlit App
After=network.target

[Service]
User=gensp
Group=gensp
WorkingDirectory=/var/gensp
Environment="LOGEMENTS_DB_PATH=/var/gensp/data/logements.db"
Environment="LOGEMENTS_EXCEL_PATH=/var/gensp/data/logements.xlsx"
ExecStart=/var/gensp/venv/bin/streamlit run /var/gensp/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

4. Activer et démarrer :

```bash
sudo systemctl daemon-reload
sudo systemctl enable gensp
sudo systemctl start gensp
```

---

## Conseils et bonnes pratiques
- Garder `requirements.txt` propre et à jour
- Préférer l'usage de PostgreSQL pour production si les données sont importantes
- Stocker les fichiers Excel dans un stockage persistant (S3, NFS, etc.)
- Ajouter HTTPS et un reverse proxy (nginx) si nécessaire

---

## Restauration / Sauvegarde
- Pour sauvegarder les données SQLite : archivez le fichier `logements.db`
- Pour sauvegarder Excel : sauvegardez `logements.xlsx`

```bash
tar czf gensp_backup_$(date +%Y%m%d).tar.gz ./data
```

---

Si vous voulez que je prépare un déploiement vers une cible précise (Docker Hub, Render, Fly, Heroku, Digital Ocean, AWS, etc.), dites-moi quelle plateforme vous préférez et je ferai les étapes nécessaires (incluant CI/CD si vous le souhaitez).
