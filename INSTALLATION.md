# 🏘️ Installation - Système de Gestion des Logements

## نظام إدارة المساكن - دليل التثبيت

---

## 📦 Contenu du Package

Votre archive contient les fichiers suivants :

```
gestion_logements_nouakchott/
│
├── app.py                      # Application Streamlit principale (31 KB)
├── database.py                 # Module de gestion de la base de données (16 KB)
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation complète
├── GUIDE_UTILISATION.md        # Guide d'utilisation FR/AR
├── INSTALLATION.md             # Ce fichier
├── run_app.sh                  # Script de lancement (Linux/Mac)
├── test_system.py              # Script de test
└── logements.xlsx              # Fichier de données (635 logements)
```

---

## 🖥️ Configuration Requise

### Système d'exploitation
- ✅ Windows 10/11
- ✅ macOS 10.14 ou supérieur
- ✅ Linux (Ubuntu 20.04+, Debian 10+, etc.)

### Logiciels nécessaires
- **Python 3.8 ou supérieur** (recommandé : Python 3.10+)
- **pip** (gestionnaire de paquets Python)
- **Navigateur Web moderne** (Chrome, Firefox, Edge, Safari)
- **Connexion Internet** (pour la cartographie)

### Espace disque
- **Minimum** : 100 MB
- **Recommandé** : 500 MB (pour les futures données)

### Mémoire RAM
- **Minimum** : 2 GB
- **Recommandé** : 4 GB ou plus

---

## 📥 Installation

### Étape 1 : Installer Python

#### Windows
1. Télécharger Python depuis [python.org](https://www.python.org/downloads/)
2. **IMPORTANT** : Cocher "Add Python to PATH" lors de l'installation
3. Installer avec les options par défaut
4. Vérifier l'installation :
   ```cmd
   python --version
   ```

#### macOS
```bash
# Avec Homebrew (recommandé)
brew install python3

# Vérifier
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip

# Vérifier
python3 --version
pip3 --version
```

### Étape 2 : Extraire l'archive

#### Windows
1. Clic droit sur `gestion_logements_nouakchott.zip`
2. Sélectionner "Extraire tout..."
3. Choisir un emplacement (ex: `C:\Users\VotreNom\Documents\`)

#### macOS / Linux
```bash
# Extraire
unzip gestion_logements_nouakchott.zip

# Entrer dans le dossier
cd gestion_logements_nouakchott
```

### Étape 3 : Installer les dépendances

#### Windows
```cmd
cd gestion_logements_nouakchott
pip install -r requirements.txt
```

#### macOS / Linux
```bash
cd gestion_logements_nouakchott
pip3 install -r requirements.txt
```

**Attendre la fin de l'installation** (environ 2-5 minutes selon votre connexion)

### Étape 4 : Tester l'installation

```bash
# Windows
python test_system.py

# macOS / Linux
python3 test_system.py
```

Vous devriez voir :
```
🎉 TOUS LES TESTS SONT PASSÉS !
✨ Le système est prêt à être utilisé
```

---

## 🚀 Lancement de l'Application

### Méthode 1 : Script automatique (Linux/Mac uniquement)

```bash
./run_app.sh
```

### Méthode 2 : Commande manuelle (Tous systèmes)

#### Windows
```cmd
streamlit run app.py
```

#### macOS / Linux
```bash
streamlit run app.py
```

### Première utilisation

1. **L'application s'ouvre automatiquement** dans votre navigateur
2. Si ce n'est pas le cas, ouvrez : `http://localhost:8501`
3. **Attendre le chargement initial** (import des 635 logements)
4. L'interface s'affiche avec le tableau de bord

---

## 🌐 Accès à l'Application

### URL locale
```
http://localhost:8501
```

### Accès depuis un autre ordinateur du réseau

1. **Sur l'ordinateur serveur**, trouvez votre adresse IP :
   
   **Windows** :
   ```cmd
   ipconfig
   ```
   Chercher "Adresse IPv4"
   
   **macOS / Linux** :
   ```bash
   ifconfig
   # ou
   ip addr show
   ```

2. **Sur l'autre ordinateur**, ouvrez :
   ```
   http://ADRESSE_IP_SERVEUR:8501
   ```
   Exemple : `http://192.168.1.100:8501`

---

## 🔧 Configuration Avancée

### Changer le port

Si le port 8501 est occupé :

```bash
streamlit run app.py --server.port 8502
```

### Mode headless (sans navigateur)

```bash
streamlit run app.py --server.headless true
```

### Configuration réseau

Créer un fichier `.streamlit/config.toml` :

```toml
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
serverAddress = "0.0.0.0"
serverPort = 8501
```

---

## 🐛 Résolution des Problèmes

### Problème : "Python n'est pas reconnu"

**Solution Windows** :
1. Réinstaller Python en cochant "Add Python to PATH"
2. Ou ajouter manuellement :
   - Panneau de configuration → Système → Paramètres système avancés
   - Variables d'environnement → PATH
   - Ajouter : `C:\Python310\` et `C:\Python310\Scripts\`

**Solution macOS/Linux** :
```bash
# Utiliser python3 au lieu de python
python3 --version
pip3 install -r requirements.txt
```

### Problème : "ModuleNotFoundError: No module named..."

**Solution** :
```bash
pip install --upgrade -r requirements.txt
```

### Problème : "Address already in use"

Le port 8501 est occupé.

**Solution** :
```bash
# Tuer le processus existant
# Windows
taskkill /F /IM streamlit.exe

# macOS/Linux
pkill -f streamlit

# Ou utiliser un autre port
streamlit run app.py --server.port 8502
```

### Problème : La carte GPS ne s'affiche pas

**Causes possibles** :
1. Pas de connexion Internet
2. Bloqueur de publicités actif
3. JavaScript désactivé

**Solution** :
- Vérifier la connexion Internet
- Désactiver les bloqueurs sur localhost
- Activer JavaScript dans le navigateur

### Problème : Le texte arabe ne s'affiche pas correctement

**Solution** :
```bash
# Réinstaller les bibliothèques de support arabe
pip install --upgrade arabic-reshaper python-bidi
```

### Problème : Import Excel échoue

**Vérifications** :
1. Le fichier Excel n'est pas ouvert dans un autre programme
2. Le fichier contient les colonnes attendues
3. Le fichier n'est pas corrompu

**Solution** :
- Fermer Excel/LibreOffice
- Vérifier avec : `python3 test_system.py`

---

## 📊 Vérification de l'Installation

### Checklist complète

- [ ] Python 3.8+ installé
- [ ] pip fonctionnel
- [ ] Toutes les dépendances installées
- [ ] Tests passés avec succès
- [ ] Application démarre sans erreur
- [ ] Page web accessible sur localhost:8501
- [ ] Données importées (635 logements)
- [ ] Carte GPS s'affiche correctement
- [ ] Possibilité de créer/modifier/supprimer

### Commandes de diagnostic

```bash
# Versions
python --version
pip --version

# Dépendances installées
pip list | grep streamlit
pip list | grep pandas
pip list | grep folium

# Test de l'application
python test_system.py
```

---

## 🔄 Mise à Jour

### Mise à jour des dépendances

```bash
pip install --upgrade -r requirements.txt
```

### Mise à jour de l'application

1. Télécharger la nouvelle version
2. Extraire dans un nouveau dossier
3. Copier `logements.db` depuis l'ancienne version
4. Réinstaller les dépendances si nécessaire

---

## 💡 Conseils d'Optimisation

### Performance

1. **Pour de grandes quantités de données** (>5000 logements) :
   - Augmenter la mémoire allouée
   - Utiliser PostgreSQL au lieu de SQLite

2. **Accélération du démarrage** :
   - Garder l'application ouverte
   - Utiliser un SSD

3. **Réseau** :
   - Connexion filaire pour le serveur
   - Utiliser un routeur de qualité

### Sécurité

1. **Sauvegardes régulières** :
   ```bash
   # Copier la base de données
   cp logements.db logements_backup_$(date +%Y%m%d).db
   ```

2. **Accès réseau** :
   - Utiliser un firewall
   - Définir des règles d'accès
   - Ne pas exposer sur Internet sans protection

3. **Données sensibles** :
   - Chiffrer les exports Excel sensibles
   - Limiter les accès physiques au serveur

---

## 📞 Support Technique

### Ressources

- **Documentation** : README.md
- **Guide utilisateur** : GUIDE_UTILISATION.md
- **Tests** : `python test_system.py`

### Logs et Débogage

```bash
# Lancer avec logs détaillés
streamlit run app.py --logger.level=debug
```

### Contact

Pour assistance :
1. Vérifier la documentation
2. Exécuter les tests
3. Contacter l'administrateur système

---

## 🎓 Formation

### Ressources d'apprentissage

**Streamlit** :
- Documentation officielle : [docs.streamlit.io](https://docs.streamlit.io)
- Tutoriels : [streamlit.io/gallery](https://streamlit.io/gallery)

**Python** :
- Guide officiel : [docs.python.org](https://docs.python.org)
- Tutoriels francophones : nombreux disponibles en ligne

**Folium (Cartographie)** :
- Documentation : [python-visualization.github.io/folium](https://python-visualization.github.io/folium)

---

## ✅ Installation Réussie !

Si tous les tests sont passés, votre système est opérationnel !

**Prochaines étapes** :
1. 📖 Lire le GUIDE_UTILISATION.md
2. 🗺️ Explorer la cartographie
3. ➕ Ajouter vos premiers logements
4. 📊 Générer des statistiques

**Bon usage du système ! / استخدام جيد للنظام!**

---

© 2024 - Système de Gestion des Logements - Nouakchott, Mauritanie
