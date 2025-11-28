"""
Module de gestion de la base de données pour les logements
Gère le CRUD complet avec SQLite et synchronisation Excel
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os
from typing import List, Dict, Optional, Tuple
import json


class LogementDatabase:
    """Classe pour gérer la base de données des logements"""
    
    def __init__(self, db_path: str = "logements.db", excel_path: str = "logements.xlsx"):
        self.db_path = db_path
        self.excel_path = excel_path
        self.conn = None
        self.init_database()
        
    def init_database(self):
        """Initialise la base de données et crée les tables"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ilot TEXT,
                logement TEXT,
                decision TEXT,
                date_decision TEXT,
                nom_affectaire TEXT,
                matricule TEXT,
                nni TEXT,
                profession TEXT,
                fonction TEXT,
                departement TEXT,
                telephone TEXT,
                en_activite TEXT,
                a_la_retraite TEXT,
                decede TEXT,
                nom_repondant TEXT,
                lien_parente TEXT,
                tel_repondant TEXT,
                pour_etat TEXT,
                reforme TEXT,
                decision2 TEXT,
                date_decision2 TEXT,
                observation TEXT,
                latitude REAL,
                longitude REAL,
                adresse TEXT,
                statut TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table pour l'historique des modifications
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historique (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                logement_id INTEGER,
                action TEXT,
                details TEXT,
                utilisateur TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (logement_id) REFERENCES logements(id)
            )
        """)
        
        self.conn.commit()
        
    def importer_depuis_excel(self) -> Tuple[int, str]:
        """Importe les données depuis le fichier Excel"""
        try:
            if not os.path.exists(self.excel_path):
                return 0, f"Fichier {self.excel_path} introuvable"
            
            # Lire le fichier Excel
            df = pd.read_excel(self.excel_path)
            
            # Nettoyer les noms de colonnes
            df.columns = df.columns.str.strip()
            
            # Mapper les colonnes
            column_mapping = {
                'Ilot': 'ilot',
                'Logement': 'logement',
                'Décision': 'decision',
                'Date Décision': 'date_decision',
                'Nom de l\'Affectaire': 'nom_affectaire',
                'Matricule': 'matricule',
                'NNI': 'nni',
                'Profession': 'profession',
                'Fonction': 'fonction',
                'Departement': 'departement',
                'Téléphone': 'telephone',
                'En Activité': 'en_activite',
                'A la Retraite': 'a_la_retraite',
                'Décédé': 'decede',
                'Nom du repondant': 'nom_repondant',
                'Lien de Parenté': 'lien_parente',
                'N° Téléphone': 'tel_repondant',
                'Pour l\'Etat': 'pour_etat',
                'Reformé': 'reforme',
            }
            
            # Générer des coordonnées GPS fictives pour Nouakchott
            # Centre de Nouakchott: 18.0735° N, 15.9582° W
            base_lat = 18.0735
            base_lon = -15.9582
            
            # Ajouter des coordonnées variées selon l'îlot
            ilots_coords = {
                'A': (18.08, -15.96),
                'B': (18.09, -15.95),
                'C': (18.07, -15.97),
                'D': (18.06, -15.96),
                'E': (18.08, -15.94),
                'F': (18.09, -15.97),
                'G': (18.07, -15.95),
                'H': (18.06, -15.94),
            }
            
            # Effacer les données existantes
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM logements")
            
            # Insérer les nouvelles données
            count = 0
            for idx, row in df.iterrows():
                ilot = str(row.get('Ilot', '')).strip()
                base_coords = ilots_coords.get(ilot, (base_lat, base_lon))
                
                # Variation aléatoire pour chaque logement
                import random
                lat = base_coords[0] + random.uniform(-0.01, 0.01)
                lon = base_coords[1] + random.uniform(-0.01, 0.01)
                
                cursor.execute("""
                    INSERT INTO logements (
                        ilot, logement, decision, date_decision, nom_affectaire,
                        matricule, nni, profession, fonction, departement,
                        telephone, en_activite, a_la_retraite, decede,
                        nom_repondant, lien_parente, tel_repondant,
                        pour_etat, reforme, latitude, longitude, statut
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row.get('Ilot', '')),
                    str(row.get('Logement', '')),
                    str(row.get('Décision', '')),
                    str(row.get('Date Décision', '')),
                    str(row.get('Nom de l\'Affectaire', '')),
                    str(row.get('Matricule', '')),
                    str(row.get('NNI', '')),
                    str(row.get('Profession', '')),
                    str(row.get('Fonction', '')),
                    str(row.get('Departement', '')),
                    str(row.get('Téléphone', '')),
                    str(row.get('En Activité', '')),
                    str(row.get('A la Retraite', '')),
                    str(row.get('Décédé', '')),
                    str(row.get('Nom du repondant', '')),
                    str(row.get('Lien de Parenté', '')),
                    str(row.get('N° Téléphone', '')),
                    str(row.get('Pour l\'Etat', '')),
                    str(row.get('Reformé', '')),
                    lat,
                    lon,
                    'Actif'
                ))
                count += 1
            
            self.conn.commit()
            self.ajouter_historique(None, "IMPORT", f"{count} logements importés depuis Excel", "Système")
            
            return count, f"✓ {count} logements importés avec succès"
            
        except Exception as e:
            return 0, f"✗ Erreur lors de l'importation: {str(e)}"
    
    def exporter_vers_excel(self, output_path: str = None) -> Tuple[bool, str]:
        """Exporte les données vers un fichier Excel"""
        try:
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"logements_export_{timestamp}.xlsx"
            
            df = self.lire_tous()
            
            # Retirer les colonnes techniques
            cols_to_remove = ['id', 'created_at', 'updated_at']
            df = df.drop(columns=[col for col in cols_to_remove if col in df.columns])
            
            # Écrire dans Excel
            df.to_excel(output_path, index=False, engine='openpyxl')
            
            self.ajouter_historique(None, "EXPORT", f"Données exportées vers {output_path}", "Système")
            
            return True, f"✓ Données exportées vers {output_path}"
            
        except Exception as e:
            return False, f"✗ Erreur lors de l'exportation: {str(e)}"
    
    # CRUD - Create
    def creer_logement(self, data: Dict) -> Tuple[int, str]:
        """Crée un nouveau logement"""
        try:
            cursor = self.conn.cursor()
            
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = tuple(data.values())
            
            cursor.execute(f"""
                INSERT INTO logements ({columns})
                VALUES ({placeholders})
            """, values)
            
            logement_id = cursor.lastrowid
            self.conn.commit()
            
            self.ajouter_historique(logement_id, "CREATE", json.dumps(data, ensure_ascii=False), "Utilisateur")
            
            return logement_id, "✓ Logement créé avec succès"
            
        except Exception as e:
            return 0, f"✗ Erreur lors de la création: {str(e)}"
    
    # CRUD - Read
    def lire_logement(self, logement_id: int) -> Optional[Dict]:
        """Lit un logement par son ID"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM logements WHERE id = ?", (logement_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            print(f"Erreur lecture: {e}")
            return None
    
    def lire_tous(self, filtre: Dict = None) -> pd.DataFrame:
        """Lit tous les logements avec filtres optionnels"""
        try:
            query = "SELECT * FROM logements WHERE 1=1"
            params = []
            
            if filtre:
                for key, value in filtre.items():
                    if value and value != "Tous":
                        query += f" AND {key} = ?"
                        params.append(value)
            
            query += " ORDER BY ilot, logement"
            
            df = pd.read_sql_query(query, self.conn, params=params)
            return df
            
        except Exception as e:
            print(f"Erreur lecture tous: {e}")
            return pd.DataFrame()
    
    # CRUD - Update
    def modifier_logement(self, logement_id: int, data: Dict) -> Tuple[bool, str]:
        """Modifie un logement existant"""
        try:
            cursor = self.conn.cursor()
            
            # Construire la requête UPDATE
            set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
            set_clause += ", updated_at = CURRENT_TIMESTAMP"
            values = tuple(data.values()) + (logement_id,)
            
            cursor.execute(f"""
                UPDATE logements 
                SET {set_clause}
                WHERE id = ?
            """, values)
            
            self.conn.commit()
            
            self.ajouter_historique(logement_id, "UPDATE", json.dumps(data, ensure_ascii=False), "Utilisateur")
            
            return True, "✓ Logement modifié avec succès"
            
        except Exception as e:
            return False, f"✗ Erreur lors de la modification: {str(e)}"
    
    # CRUD - Delete
    def supprimer_logement(self, logement_id: int) -> Tuple[bool, str]:
        """Supprime un logement"""
        try:
            cursor = self.conn.cursor()
            
            # Lire les données avant suppression pour l'historique
            logement = self.lire_logement(logement_id)
            
            cursor.execute("DELETE FROM logements WHERE id = ?", (logement_id,))
            self.conn.commit()
            
            if logement:
                self.ajouter_historique(
                    logement_id, 
                    "DELETE", 
                    f"Logement {logement.get('ilot')}-{logement.get('logement')} supprimé",
                    "Utilisateur"
                )
            
            return True, "✓ Logement supprimé avec succès"
            
        except Exception as e:
            return False, f"✗ Erreur lors de la suppression: {str(e)}"
    
    # Recherche et filtres
    def rechercher(self, terme: str) -> pd.DataFrame:
        """Recherche dans tous les champs texte"""
        try:
            query = """
                SELECT * FROM logements 
                WHERE ilot LIKE ? OR logement LIKE ? OR nom_affectaire LIKE ?
                OR nni LIKE ? OR profession LIKE ? OR departement LIKE ?
                ORDER BY ilot, logement
            """
            
            search_term = f"%{terme}%"
            params = [search_term] * 6
            
            df = pd.read_sql_query(query, self.conn, params=params)
            return df
            
        except Exception as e:
            print(f"Erreur recherche: {e}")
            return pd.DataFrame()
    
    def obtenir_valeurs_uniques(self, colonne: str) -> List[str]:
        """Obtient les valeurs uniques d'une colonne"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT DISTINCT {colonne} FROM logements WHERE {colonne} IS NOT NULL AND {colonne} != '' ORDER BY {colonne}")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            print(f"Erreur valeurs uniques: {e}")
            return []
    
    def obtenir_statistiques(self) -> Dict:
        """Calcule des statistiques sur les logements"""
        try:
            cursor = self.conn.cursor()
            
            stats = {}
            
            # Total
            cursor.execute("SELECT COUNT(*) FROM logements")
            stats['total'] = cursor.fetchone()[0]
            
            # Par îlot
            cursor.execute("SELECT ilot, COUNT(*) FROM logements GROUP BY ilot ORDER BY ilot")
            stats['par_ilot'] = dict(cursor.fetchall())
            
            # Par département
            cursor.execute("SELECT departement, COUNT(*) FROM logements WHERE departement != '' GROUP BY departement ORDER BY COUNT(*) DESC LIMIT 10")
            stats['par_departement'] = dict(cursor.fetchall())
            
            # Par statut
            cursor.execute("SELECT en_activite, COUNT(*) FROM logements GROUP BY en_activite")
            stats['par_activite'] = dict(cursor.fetchall())
            
            return stats
            
        except Exception as e:
            print(f"Erreur statistiques: {e}")
            return {}
    
    def ajouter_historique(self, logement_id: Optional[int], action: str, details: str, utilisateur: str):
        """Ajoute une entrée dans l'historique"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO historique (logement_id, action, details, utilisateur)
                VALUES (?, ?, ?, ?)
            """, (logement_id, action, details, utilisateur))
            self.conn.commit()
        except Exception as e:
            print(f"Erreur historique: {e}")
    
    def obtenir_historique(self, logement_id: int = None, limit: int = 50) -> pd.DataFrame:
        """Récupère l'historique des modifications"""
        try:
            if logement_id:
                query = "SELECT * FROM historique WHERE logement_id = ? ORDER BY timestamp DESC LIMIT ?"
                params = (logement_id, limit)
            else:
                query = "SELECT * FROM historique ORDER BY timestamp DESC LIMIT ?"
                params = (limit,)
            
            df = pd.read_sql_query(query, self.conn, params=params)
            return df
        except Exception as e:
            print(f"Erreur lecture historique: {e}")
            return pd.DataFrame()
    
    def fermer(self):
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destructeur pour fermer proprement la connexion"""
        self.fermer()
