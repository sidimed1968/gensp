# 🏘️ Système de Gestion des Logements - Nouakchott, Mauritanie

## 📋 Description

Application complète de gestion des logements administratifs de Nouakchott avec :
- ✅ CRUD complet (Create, Read, Update, Delete)
- 🗺️ Cartographie GPS interactive avec Folium
- 🌐 Interface bilingue (Français/Arabe)
- 📊 Statistiques et tableaux de bord
- 💾 Import/Export Excel
- 🖨️ Impression de rapports
- 📜 Historique des modifications
- 🔍 Recherche et filtres avancés

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

### Déploiement (Docker)

Vous pouvez exécuter l'application dans un conteneur Docker :

```bash
# Construire l'image
docker build -t gensp:latest .

# Démarrer avec Docker Compose
docker-compose up -d --build

# L'application sera disponible sur http://localhost:8501
```


2. **Préparer les données :**
   - Placer le fichier `logements.xlsx` dans le même répertoire que les scripts
   - L'application créera automatiquement la base de données SQLite

## 📂 Structure du projet

```
logements-nouakchott/
│
├── app.py                  # Application Streamlit principale
├── database.py             # Module de gestion de la base de données
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
│
├── logements.xlsx         # Fichier Excel source (à fournir)
├── logements.db           # Base de données SQLite (créée automatiquement)
│
└── exports/               # Dossier pour les exports (créé automatiquement)
```

## 🎯 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse :
`http://localhost:8501`

### Fonctionnalités principales

#### 1. 📊 Tableau de Bord
- Vue d'ensemble des statistiques
- Graphiques de répartition par îlot et département
- Carte générale de tous les logements

#### 2. 📋 Liste des Logements
- Affichage tabulaire avec filtres multiples
- Recherche par nom, NNI, profession
- Sélection des colonnes à afficher
- Actions sur chaque logement (modifier, supprimer, voir sur carte)

#### 3. ➕ Ajouter un Logement
- Formulaire complet avec tous les champs
- Validation des données
- Ajout de coordonnées GPS

#### 4. ✏️ Modifier un Logement
- Édition de tous les champs
- Mise à jour des coordonnées GPS
- Historique des modifications

#### 5. 🗺️ Cartographie GPS
- Carte interactive avec Folium
- Marqueurs colorés par îlot
- Pop-ups détaillés pour chaque logement
- Filtres dynamiques (îlot, département, profession)
- Légende interactive

#### 6. 💾 Import/Export
- **Import** : Charger des données depuis Excel
- **Export** : Exporter vers Excel avec horodatage
- Sauvegarde complète de la base de données

#### 7. 📜 Historique
- Journal de toutes les modifications
- Suivi des actions CREATE, UPDATE, DELETE
- Horodatage de chaque opération

## 🗺️ Cartographie

### Fonctionnalités GPS

La carte interactive offre :
- **Marqueurs colorés** : Un code couleur par îlot
- **Pop-ups informatifs** : Toutes les données du logement
- **Filtres dynamiques** : Affichage sélectif par critères
- **Tooltips** : Aperçu rapide au survol
- **Légende** : Identification des îlots par couleur

### Couleurs des îlots

| Îlot | Couleur |
|------|---------|
| A    | Rouge   |
| B    | Bleu    |
| C    | Vert    |
| D    | Violet  |
| E    | Orange  |
| F    | Rouge foncé |
| G    | Rouge clair |
| H    | Beige   |

## 📊 Structure de la Base de Données

### Table : logements

| Champ | Type | Description |
|-------|------|-------------|
| id | INTEGER | Identifiant unique (auto-incrémenté) |
| ilot | TEXT | Îlot (A, B, C, etc.) |
| logement | TEXT | Numéro du logement |
| decision | TEXT | Numéro de décision |
| date_decision | TEXT | Date de la décision |
| nom_affectaire | TEXT | Nom de l'affectaire |
| matricule | TEXT | Matricule |
| nni | TEXT | Numéro National d'Identification |
| profession | TEXT | Profession |
| fonction | TEXT | Fonction |
| departement | TEXT | Département |
| telephone | TEXT | Téléphone |
| en_activite | TEXT | En activité (Oui/Non) |
| a_la_retraite | TEXT | À la retraite (Oui/Non) |
| decede | TEXT | Décédé (Oui/Non) |
| nom_repondant | TEXT | Nom du répondant |
| lien_parente | TEXT | Lien de parenté |
| tel_repondant | TEXT | Téléphone du répondant |
| pour_etat | TEXT | Pour l'État |
| reforme | TEXT | Réformé |
| latitude | REAL | Latitude GPS |
| longitude | REAL | Longitude GPS |
| adresse | TEXT | Adresse complète |
| statut | TEXT | Statut (Actif/Inactif) |
| observation | TEXT | Observations |
| created_at | TIMESTAMP | Date de création |
| updated_at | TIMESTAMP | Date de modification |

### Table : historique

| Champ | Type | Description |
|-------|------|-------------|
| id | INTEGER | Identifiant unique |
| logement_id | INTEGER | ID du logement concerné |
| action | TEXT | Type d'action (CREATE/UPDATE/DELETE/IMPORT/EXPORT) |
| details | TEXT | Détails de l'action (JSON) |
| utilisateur | TEXT | Utilisateur ayant effectué l'action |
| timestamp | TIMESTAMP | Date et heure de l'action |

## 🌐 Support Multilingue

L'application supporte deux langues :
- **Français** (fr) : Langue par défaut
- **Arabe** (ar) : Support complet avec gestion RTL

### Changement de langue

Utiliser le sélecteur de langue dans la barre latérale.

## 🔧 Configuration

### Coordonnées GPS par défaut

- **Centre de Nouakchott** : 18.0735° N, 15.9582° W
- Les logements sont répartis automatiquement autour de leur îlot respectif
- Variation aléatoire de ±0.01° pour éviter les superpositions

### Personnalisation des couleurs

Modifier le dictionnaire `couleurs_ilot` dans `app.py` :

```python
couleurs_ilot = {
    'A': 'red',
    'B': 'blue',
    # Ajouter d'autres îlots...
}
```

## 📤 Export des Données

Les exports sont générés au format Excel (.xlsx) avec :
- Horodatage dans le nom du fichier
- Toutes les colonnes de données
- Format compatible avec Microsoft Excel et LibreOffice

Format du nom : `logements_export_YYYYMMDD_HHMMSS.xlsx`

## 🔍 Recherche et Filtres

### Champs de recherche

La recherche s'effectue sur :
- Îlot
- Numéro de logement
- Nom de l'affectaire
- NNI
- Profession
- Département

### Filtres disponibles

- Par îlot
- Par département
- Par profession
- Par statut d'activité

Les filtres sont cumulatifs.

## 🖨️ Impression

Pour imprimer les données :

1. Afficher la liste filtrée souhaitée
2. Sélectionner les colonnes à imprimer
3. Cliquer sur "Préparer impression"
4. Utiliser Ctrl+P (Cmd+P sur Mac)

## 🛠️ API de la Base de Données

### Classe LogementDatabase

```python
from database import LogementDatabase

# Initialisation
db = LogementDatabase()

# Import depuis Excel
count, message = db.importer_depuis_excel()

# CRUD
logement_id, message = db.creer_logement(data)
logement = db.lire_logement(logement_id)
success, message = db.modifier_logement(logement_id, data)
success, message = db.supprimer_logement(logement_id)

# Lecture et recherche
df = db.lire_tous(filtre={'ilot': 'A'})
df = db.rechercher('terme de recherche')

# Statistiques
stats = db.obtenir_statistiques()

# Export
success, message = db.exporter_vers_excel('output.xlsx')

# Fermer la connexion
db.fermer()
```

## 📊 Statistiques Disponibles

- **Total des logements**
- **Répartition par îlot**
- **Répartition par département**
- **Statut d'activité des affectaires**
- **Logements vacants**

## 🐛 Dépannage

### Problème : La base de données ne se crée pas

**Solution** : Vérifier les permissions d'écriture dans le répertoire

### Problème : L'import Excel échoue

**Solution** : Vérifier que le fichier Excel contient les colonnes attendues

### Problème : La carte ne s'affiche pas

**Solution** : 
- Vérifier la connexion Internet
- Vérifier que les coordonnées GPS sont valides

### Problème : Le texte arabe ne s'affiche pas correctement

**Solution** : 
- Installer les polices arabes système
- Vérifier que `arabic-reshaper` et `python-bidi` sont installés

## 🔒 Sécurité

- Base de données SQLite locale (pas d'exposition réseau)
- Validation des entrées utilisateur
- Historique complet des modifications
- Sauvegarde automatique

## 📝 Notes Importantes

1. **Sauvegarde régulière** : Exporter régulièrement les données en Excel
2. **Coordonnées GPS** : Les coordonnées sont générées automatiquement mais peuvent être modifiées manuellement
3. **Performance** : Pour de grandes quantités de données (>10 000 logements), envisager PostgreSQL
4. **Navigateur** : Meilleure expérience avec Chrome ou Firefox

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le repository
2. Créer une branche pour votre fonctionnalité
3. Commit vos changements
4. Push vers la branche
5. Créer une Pull Request

## 📧 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Contacter l'administrateur système

## 📜 Licence

Ce projet est sous licence MIT.

## 🙏 Remerciements

- Streamlit pour le framework web
- Folium pour la cartographie
- Plotly pour les graphiques
- La communauté open-source

---

**Développé avec ❤️ pour la gestion des logements de Nouakchott, Mauritanie**
"# gensp"  
