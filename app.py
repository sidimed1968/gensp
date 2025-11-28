"""
Application Streamlit pour la gestion des logements de Nouakchott
Système complet avec CRUD, cartographie GPS, et support FR/AR
"""

import streamlit as st
import pandas as pd
import tempfile
import os
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from database import LogementDatabase
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
import json


# ============================================
# CONFIGURATION INITIALE
# ============================================

# Configuration de la page (DOIT ÊTRE LA PREMIÈRE COMMANDE STREAMLIT)
st.set_page_config(
    page_title="Gestion des Logements - Nouakchott",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de la session AVANT toute utilisation
if 'lang' not in st.session_state:
    st.session_state.lang = 'fr'

if 'db' not in st.session_state:
    # Créer le chemin du fichier Excel dans le dossier de l'utilisateur
    excel_path = os.path.join(os.path.expanduser("~"), "logements.xlsx")
    st.session_state.db = LogementDatabase(excel_path=excel_path)
    st.session_state.data_loaded = False

if 'selected_logements' not in st.session_state:
    st.session_state.selected_logements = []

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'


# ============================================
# STYLES CSS AMÉLIORÉS
# ============================================

def apply_custom_css():
    """Applique les styles CSS personnalisés selon la langue"""
    lang = st.session_state.lang
    
    direction = "rtl" if lang == 'ar' else "ltr"
    text_align = "right" if lang == 'ar' else "left"
    font_family = "'Arial', 'Tahoma', 'Traditional Arabic', sans-serif" if lang == 'ar' else "'Segoe UI', 'Arial', sans-serif"
    
    st.markdown(f"""
    <style>
        /* Direction et alignement selon la langue */
        .stApp {{
            direction: {direction};
            text-align: {text_align};
        }}
        
        * {{
            font-family: {font_family} !important;
        }}
        
        /* Header principal */
        .main-header {{
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #1f77b4;
            padding: 1rem;
            background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
            border-radius: 10px;
            margin-bottom: 2rem;
        }}
        
        /* Boîtes de statistiques */
        .stat-box {{
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #1f77b4;
        }}
        
        /* Boutons */
        .stButton>button {{
            width: 100%;
            border-radius: 5px;
            font-weight: 500;
        }}
        
        /* Inputs et selects */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {{
            direction: {direction};
            text-align: {text_align};
        }}
        
        /* Tableaux */
        .dataframe {{
            direction: {direction};
        }}
        
        /* Sidebar */
        .css-1d391kg {{
            padding-top: 1rem;
        }}
        
        /* Métriques */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: bold;
        }}
        
        /* Amélioration de l'impression */
        @media print {{
            .no-print, .stSidebar, .stButton {{ 
                display: none !important; 
            }}
            .main-header {{
                background: white !important;
                color: black !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


# ============================================
# TRADUCTIONS COMPLÈTES
# ============================================

TRANSLATIONS = {
    'fr': {
        # Navigation
        'title': '🏘️ Système de Gestion des Logements - Nouakchott, Mauritanie',
        'language': 'Langue',
        'menu': 'Menu',
        'dashboard': '📊 Tableau de Bord',
        'list': '📋 Liste des Logements',
        'add': '➕ Ajouter un Logement',
        'edit': '✏️ Modifier un Logement',
        'search': '🔍 Recherche & Filtres',
        'map': '🗺️ Cartographie GPS',
        'import_export': '💾 Import/Export',
        'statistics': '📈 Statistiques',
        'history': '📜 Historique',
        
        # Statistiques
        'total': 'Total des logements',
        'by_ilot': 'Par îlot',
        'by_dept': 'Par département',
        'active': 'En activité',
        'retired': 'À la retraite',
        'deceased': 'Décédés',
        
        # Filtres et recherche
        'filters': 'Filtres',
        'ilot': 'Îlot',
        'logement': 'Logement',
        'affectaire': 'Affectaire',
        'profession': 'Profession',
        'departement': 'Département',
        'telephone': 'Téléphone',
        'nni': 'NNI',
        'all': 'Tous',
        'search_placeholder': 'Rechercher par nom, NNI, profession...',
        'search_button': 'Rechercher',
        
        # Actions
        'export': 'Exporter les données',
        'import': 'Importer depuis Excel',
        'save': 'Enregistrer',
        'cancel': 'Annuler',
        'delete': 'Supprimer',
        'edit_action': 'Modifier',
        'view_map': 'Voir sur la carte',
        'select': 'Sélectionner',
        'showing': 'Affichage de',
        'results': 'résultats',
        'loading': 'Chargement des données...',
        
        # Champs de formulaire
        'decision': 'Décision',
        'date_decision': 'Date Décision',
        'matricule': 'Matricule',
        'fonction': 'Fonction',
        'en_activite': 'En Activité',
        'a_la_retraite': 'À la Retraite',
        'decede': 'Décédé',
        'nom_repondant': 'Nom du Répondant',
        'lien_parente': 'Lien de Parenté',
        'tel_repondant': 'Téléphone Répondant',
        'latitude': 'Latitude',
        'longitude': 'Longitude',
        'observation': 'Observation',
        'statut': 'Statut',
        
        # Messages
        'yes': 'Oui',
        'no': 'Non',
        'required_fields': 'Les champs marqués * sont obligatoires',
        'success_add': 'Logement ajouté avec succès',
        'success_edit': 'Logement modifié avec succès',
        'success_delete': 'Logement supprimé avec succès',
        'error': 'Erreur',
        'no_data': 'Aucune donnée disponible',
        'no_housing': 'Aucun logement trouvé',
        'select_housing': 'Sélectionner un logement (ID)',
        'no_selection': 'Aucun logement sélectionné pour modification',
        'not_found': 'Logement introuvable',
        'file_saved': 'Fichier sauvegardé dans',
        'import_success': 'Import réussi',
        'export_success': 'Export réussi',
    },
    'ar': {
        # Navigation
        'title': '🏘️ نظام إدارة المساكن - نواكشوط، موريتانيا',
        'language': 'اللغة',
        'menu': 'القائمة',
        'dashboard': '📊 لوحة المعلومات',
        'list': '📋 قائمة المساكن',
        'add': '➕ إضافة مسكن',
        'edit': '✏️ تعديل مسكن',
        'search': '🔍 البحث والفلاتر',
        'map': '🗺️ الخريطة',
        'import_export': '💾 استيراد/تصدير',
        'statistics': '📈 الإحصائيات',
        'history': '📜 السجل',
        
        # Statistiques
        'total': 'إجمالي المساكن',
        'by_ilot': 'حسب الجزيرة',
        'by_dept': 'حسب القسم',
        'active': 'نشط',
        'retired': 'متقاعد',
        'deceased': 'متوفى',
        
        # Filtres et recherche
        'filters': 'الفلاتر',
        'ilot': 'الجزيرة',
        'logement': 'المسكن',
        'affectaire': 'المستفيد',
        'profession': 'المهنة',
        'departement': 'القسم',
        'telephone': 'الهاتف',
        'nni': 'رقم التعريف الوطني',
        'all': 'الكل',
        'search_placeholder': 'البحث بالاسم، رقم التعريف، المهنة...',
        'search_button': 'بحث',
        
        # Actions
        'export': 'تصدير البيانات',
        'import': 'استيراد من Excel',
        'save': 'حفظ',
        'cancel': 'إلغاء',
        'delete': 'حذف',
        'edit_action': 'تعديل',
        'view_map': 'عرض على الخريطة',
        'select': 'اختيار',
        'showing': 'عرض',
        'results': 'نتيجة',
        'loading': 'جاري تحميل البيانات...',
        
        # Champs de formulaire
        'decision': 'القرار',
        'date_decision': 'تاريخ القرار',
        'matricule': 'الرقم المسلسل',
        'fonction': 'الوظيفة',
        'en_activite': 'نشط',
        'a_la_retraite': 'متقاعد',
        'decede': 'متوفى',
        'nom_repondant': 'اسم المجيب',
        'lien_parente': 'صلة القرابة',
        'tel_repondant': 'هاتف المجيب',
        'latitude': 'خط العرض',
        'longitude': 'خط الطول',
        'observation': 'ملاحظة',
        'statut': 'الحالة',
        
        # Messages
        'yes': 'نعم',
        'no': 'لا',
        'required_fields': 'الحقول المميزة بـ * إلزامية',
        'success_add': 'تمت إضافة المسكن بنجاح',
        'success_edit': 'تم تعديل المسكن بنجاح',
        'success_delete': 'تم حذف المسكن بنجاح',
        'error': 'خطأ',
        'no_data': 'لا توجد بيانات متاحة',
        'no_housing': 'لم يتم العثور على مساكن',
        'select_housing': 'اختر مسكن (المعرف)',
        'no_selection': 'لم يتم اختيار مسكن للتعديل',
        'not_found': 'المسكن غير موجود',
        'file_saved': 'تم حفظ الملف في',
        'import_success': 'نجح الاستيراد',
        'export_success': 'نجح التصدير',
    }
}


def t(key, lang='fr'):
    """Fonction de traduction robuste"""
    try:
        return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)
    except Exception:
        return key


def format_arabic_text(text):
    """Formate le texte arabe pour un affichage correct"""
    try:
        if text and st.session_state.lang == 'ar':
            reshaped_text = arabic_reshaper.reshape(str(text))
            return get_display(reshaped_text)
        return text
    except Exception:
        return text


# ============================================
# FONCTIONS UTILITAIRES
# ============================================

def afficher_valeur_activite(valeur, lang='fr'):
    """Affiche correctement le statut d'activité (gère les NaN)"""
    if pd.isna(valeur) or valeur is None or valeur == '':
        return t('no', lang)
    
    # Convertir en booléen de manière robuste
    if isinstance(valeur, bool):
        return t('yes', lang) if valeur else t('no', lang)
    
    if isinstance(valeur, str):
        valeur_lower = str(valeur).lower().strip()
        if valeur_lower in ['oui', 'yes', 'true', '1', 'actif', 'نعم']:
            return t('yes', lang)
        else:
            return t('no', lang)
    
    if isinstance(valeur, (int, float)):
        return t('yes', lang) if valeur == 1 else t('no', lang)
    
    return t('no', lang)


def nettoyer_dataframe(df, lang='fr'):
    """Nettoie le DataFrame pour l'affichage (remplace NaN, traduit)"""
    if df.empty:
        return df
    
    df_clean = df.copy()
    
    # Remplacer les NaN
    for col in df_clean.columns:
        # Colonnes booléennes
        if col in ['en_activite', 'a_la_retraite', 'decede']:
            df_clean[col] = df_clean[col].apply(lambda x: afficher_valeur_activite(x, lang))
        # Colonnes texte
        elif df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].fillna('-').replace('', '-')
        # Colonnes numériques
        elif df_clean[col].dtype in ['float64', 'int64']:
            df_clean[col] = df_clean[col].fillna(0)
    
    return df_clean


def get_safe_value(data_dict, key, default=''):
    """Récupère une valeur de manière sécurisée depuis un dictionnaire"""
    try:
        value = data_dict.get(key, default)
        if pd.isna(value):
            return default
        return str(value) if value is not None else default
    except Exception:
        return default


# ============================================
# PAGES DE L'APPLICATION
# ============================================

def page_dashboard():
    """Page du tableau de bord avec statistiques"""
    lang = st.session_state.lang
    
    st.markdown(f"<div class='main-header'>{t('dashboard', lang)}</div>", unsafe_allow_html=True)
    
    # Charger les données si nécessaire
    if not st.session_state.data_loaded:
        with st.spinner(t('loading', lang)):
            try:
                count, message = st.session_state.db.importer_depuis_excel()
                if count > 0:
                    st.session_state.data_loaded = True
                    st.success(message)
                elif count == 0:
                    st.info("Aucune donnée à importer. Ajoutez des logements manuellement.")
            except Exception as e:
                st.warning(f"Impossible de charger depuis Excel: {str(e)}")
    
    # Statistiques
    stats = st.session_state.db.obtenir_statistiques()
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(t('total', lang), stats.get('total', 0))
    
    with col2:
        st.metric(t('by_ilot', lang), len(stats.get('par_ilot', {})))
    
    with col3:
        st.metric(t('by_dept', lang), len(stats.get('par_departement', {})))
    
    with col4:
        actifs = stats.get('par_activite', {}).get('Oui', 0)
        st.metric(t('active', lang), actifs)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 " + t('by_ilot', lang))
        if stats.get('par_ilot'):
            df_ilot = pd.DataFrame(list(stats['par_ilot'].items()), columns=['Îlot', 'Nombre'])
            df_ilot = df_ilot.sort_values('Îlot')
            fig = px.bar(df_ilot, x='Îlot', y='Nombre', color='Nombre', 
                        color_continuous_scale='Blues',
                        title=t('by_ilot', lang))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t('no_data', lang))
    
    with col2:
        st.subheader("📊 " + t('by_dept', lang))
        if stats.get('par_departement'):
            df_dept = pd.DataFrame(list(stats['par_departement'].items()), 
                                  columns=['Département', 'Nombre'])
            fig = px.pie(df_dept, values='Nombre', names='Département', 
                        hole=0.4, title=t('by_dept', lang))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t('no_data', lang))
    
    # Carte de tous les logements
    st.subheader("🗺️ " + t('map', lang))
    afficher_carte_generale()


def page_liste():
    """Page de liste des logements avec filtres"""
    lang = st.session_state.lang
    
    st.markdown(f"<div class='main-header'>{t('list', lang)}</div>", unsafe_allow_html=True)
    
    # Filtres
    with st.expander(t('filters', lang), expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ilots = [t('all', lang)] + st.session_state.db.obtenir_valeurs_uniques('ilot')
            filtre_ilot = st.selectbox(t('ilot', lang), ilots)
        
        with col2:
            depts = [t('all', lang)] + st.session_state.db.obtenir_valeurs_uniques('departement')
            filtre_dept = st.selectbox(t('departement', lang), depts)
        
        with col3:
            profs = [t('all', lang)] + st.session_state.db.obtenir_valeurs_uniques('profession')
            filtre_prof = st.selectbox(t('profession', lang), profs)
        
        with col4:
            terme_recherche = st.text_input(t('search_placeholder', lang))
    
    # Construire les filtres
    filtres = {}
    if filtre_ilot != t('all', lang):
        filtres['ilot'] = filtre_ilot
    if filtre_dept != t('all', lang):
        filtres['departement'] = filtre_dept
    if filtre_prof != t('all', lang):
        filtres['profession'] = filtre_prof
    
    # Charger les données
    if terme_recherche:
        df = st.session_state.db.rechercher(terme_recherche)
    else:
        df = st.session_state.db.lire_tous(filtres)
    
    # Nettoyer les données
    df = nettoyer_dataframe(df, lang)
    
    st.info(f"{t('showing', lang)} {len(df)} {t('results', lang)}")
    
    if not df.empty:
        # Sélection des colonnes à afficher
        colonnes_disponibles = list(df.columns)
        colonnes_par_defaut = ['ilot', 'logement', 'nom_affectaire', 'profession', 
                              'departement', 'telephone', 'nni', 'en_activite']
        
        colonnes_selectionnees = st.multiselect(
            "Colonnes à afficher",
            colonnes_disponibles,
            default=[col for col in colonnes_par_defaut if col in colonnes_disponibles]
        )
        
        if colonnes_selectionnees:
            df_display = df[colonnes_selectionnees]
        else:
            df_display = df
        
        # Boutons d'action globaux
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("📥 " + t('export', lang)):
                output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                nom_fichier = f"logements_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                output_path = os.path.join(output_dir, nom_fichier)
                success, message = st.session_state.db.exporter_vers_excel(output_path)
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        with col2:
            if st.button("🗺️ Carte"):
                st.session_state.page = 'map_filtered'
                st.rerun()
        
        with col3:
            if st.button("🖨️ Imprimer"):
                preparer_impression(df_display)
        
        # Affichage du tableau
        st.dataframe(
            df_display,
            use_container_width=True,
            height=400
        )
        
        # Actions sur les lignes
        st.subheader("Actions")
        
        if 'id' in df.columns and len(df) > 0:
            logement_id = st.selectbox(
                t('select_housing', lang),
                df['id'].tolist(),
                format_func=lambda x: f"ID:{x} - {get_safe_value(df[df['id']==x].iloc[0], 'ilot')}-{get_safe_value(df[df['id']==x].iloc[0], 'logement')} - {get_safe_value(df[df['id']==x].iloc[0], 'nom_affectaire')}"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✏️ " + t('edit_action', lang)):
                    st.session_state.edit_id = logement_id
                    st.session_state.page = 'edit'
                    st.rerun()
            
            with col2:
                if st.button("🗺️ " + t('view_map', lang)):
                    st.session_state.selected_logements = [logement_id]
                    st.session_state.page = 'map_filtered'
                    st.rerun()
            
            with col3:
                if st.button("🗑️ " + t('delete', lang), type="secondary"):
                    success, message = st.session_state.db.supprimer_logement(logement_id)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.warning(t('no_housing', lang))


def page_ajout():
    """Page d'ajout d'un nouveau logement"""
    lang = st.session_state.lang
    
    st.markdown(f"<div class='main-header'>{t('add', lang)}</div>", unsafe_allow_html=True)
    
    with st.form("form_ajout"):
        col1, col2 = st.columns(2)
        
        with col1:
            ilot = st.text_input(t('ilot', lang) + " *")
            logement = st.text_input(t('logement', lang) + " *")
            decision = st.text_input(t('decision', lang))
            date_decision = st.text_input(t('date_decision', lang))
            nom_affectaire = st.text_input(t('affectaire', lang) + " *")
            matricule = st.text_input(t('matricule', lang))
            nni = st.text_input(t('nni', lang))
            profession = st.text_input(t('profession', lang))
            fonction = st.text_input(t('fonction', lang))
        
        with col2:
            departement = st.text_input(t('departement', lang))
            telephone = st.text_input(t('telephone', lang))
            en_activite = st.selectbox(t('en_activite', lang), ["", t('yes', lang), t('no', lang)])
            a_la_retraite = st.selectbox(t('a_la_retraite', lang), ["", t('yes', lang), t('no', lang)])
            decede = st.selectbox(t('decede', lang), ["", t('yes', lang), t('no', lang)])
            nom_repondant = st.text_input(t('nom_repondant', lang))
            lien_parente = st.text_input(t('lien_parente', lang))
            tel_repondant = st.text_input(t('tel_repondant', lang))
        
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input(t('latitude', lang), value=18.0735, format="%.6f")
        with col2:
            longitude = st.number_input(t('longitude', lang), value=-15.9582, format="%.6f")
        
        observation = st.text_area(t('observation', lang))
        
        submitted = st.form_submit_button("💾 " + t('save', lang))
        
        if submitted:
            if not ilot or not logement or not nom_affectaire:
                st.error(t('required_fields', lang))
            else:
                # Convertir les valeurs de langue en français pour la base de données
                en_activite_db = "Oui" if en_activite == t('yes', lang) else "Non" if en_activite == t('no', lang) else ""
                a_la_retraite_db = "Oui" if a_la_retraite == t('yes', lang) else "Non" if a_la_retraite == t('no', lang) else ""
                decede_db = "Oui" if decede == t('yes', lang) else "Non" if decede == t('no', lang) else ""
                
                data = {
                    'ilot': ilot,
                    'logement': logement,
                    'decision': decision,
                    'date_decision': date_decision,
                    'nom_affectaire': nom_affectaire,
                    'matricule': matricule,
                    'nni': nni,
                    'profession': profession,
                    'fonction': fonction,
                    'departement': departement,
                    'telephone': telephone,
                    'en_activite': en_activite_db,
                    'a_la_retraite': a_la_retraite_db,
                    'decede': decede_db,
                    'nom_repondant': nom_repondant,
                    'lien_parente': lien_parente,
                    'tel_repondant': tel_repondant,
                    'latitude': latitude,
                    'longitude': longitude,
                    'observation': observation,
                    'statut': 'Actif'
                }
                
                logement_id, message = st.session_state.db.creer_logement(data)
                if logement_id > 0:
                    st.success(t('success_add', lang))
                    st.balloons()
                else:
                    st.error(message)


def page_modification():
    """Page de modification d'un logement"""
    lang = st.session_state.lang
    
    st.markdown(f"<div class='main-header'>{t('edit', lang)}</div>", unsafe_allow_html=True)
    
    if 'edit_id' not in st.session_state:
        st.warning(t('no_selection', lang))
        return
    
    logement = st.session_state.db.lire_logement(st.session_state.edit_id)
    
    if not logement:
        st.error(t('not_found', lang))
        return
    
    with st.form("form_modification"):
        col1, col2 = st.columns(2)
        
        with col1:
            ilot = st.text_input(t('ilot', lang), value=get_safe_value(logement, 'ilot'))
            logement_num = st.text_input(t('logement', lang), value=get_safe_value(logement, 'logement'))
            decision = st.text_input(t('decision', lang), value=get_safe_value(logement, 'decision'))
            date_decision = st.text_input(t('date_decision', lang), value=get_safe_value(logement, 'date_decision'))
            nom_affectaire = st.text_input(t('affectaire', lang), value=get_safe_value(logement, 'nom_affectaire'))
            matricule = st.text_input(t('matricule', lang), value=get_safe_value(logement, 'matricule'))
            nni = st.text_input(t('nni', lang), value=get_safe_value(logement, 'nni'))
            profession = st.text_input(t('profession', lang), value=get_safe_value(logement, 'profession'))
            fonction = st.text_input(t('fonction', lang), value=get_safe_value(logement, 'fonction'))
        
        with col2:
            departement = st.text_input(t('departement', lang), value=get_safe_value(logement, 'departement'))
            telephone = st.text_input(t('telephone', lang), value=get_safe_value(logement, 'telephone'))
            
            # Gestion robuste des selectbox
            valeur_activite = get_safe_value(logement, 'en_activite', '')
            options_activite = ["", t('yes', lang), t('no', lang)]
            if valeur_activite.lower() == 'oui':
                index_activite = 1
            elif valeur_activite.lower() == 'non':
                index_activite = 2
            else:
                index_activite = 0
            en_activite = st.selectbox(t('en_activite', lang), options_activite, index=index_activite)
            
            valeur_retraite = get_safe_value(logement, 'a_la_retraite', '')
            if valeur_retraite.lower() == 'oui':
                index_retraite = 1
            elif valeur_retraite.lower() == 'non':
                index_retraite = 2
            else:
                index_retraite = 0
            a_la_retraite = st.selectbox(t('a_la_retraite', lang), options_activite, index=index_retraite)
            
            valeur_decede = get_safe_value(logement, 'decede', '')
            if valeur_decede.lower() == 'oui':
                index_decede = 1
            elif valeur_decede.lower() == 'non':
                index_decede = 2
            else:
                index_decede = 0
            decede = st.selectbox(t('decede', lang), options_activite, index=index_decede)
            
            nom_repondant = st.text_input(t('nom_repondant', lang), value=get_safe_value(logement, 'nom_repondant'))
            lien_parente = st.text_input(t('lien_parente', lang), value=get_safe_value(logement, 'lien_parente'))
            tel_repondant = st.text_input(t('tel_repondant', lang), value=get_safe_value(logement, 'tel_repondant'))
        
        col1, col2 = st.columns(2)
        with col1:
            try:
                lat_value = float(get_safe_value(logement, 'latitude', 18.0735))
            except:
                lat_value = 18.0735
            latitude = st.number_input(t('latitude', lang), value=lat_value, format="%.6f")
        
        with col2:
            try:
                lon_value = float(get_safe_value(logement, 'longitude', -15.9582))
            except:
                lon_value = -15.9582
            longitude = st.number_input(t('longitude', lang), value=lon_value, format="%.6f")
        
        observation = st.text_area(t('observation', lang), value=get_safe_value(logement, 'observation'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            submitted = st.form_submit_button("💾 " + t('save', lang))
        
        with col2:
            cancelled = st.form_submit_button("❌ " + t('cancel', lang))
        
        if submitted:
            # Convertir les valeurs de langue en français pour la base de données
            en_activite_db = "Oui" if en_activite == t('yes', lang) else "Non" if en_activite == t('no', lang) else ""
            a_la_retraite_db = "Oui" if a_la_retraite == t('yes', lang) else "Non" if a_la_retraite == t('no', lang) else ""
            decede_db = "Oui" if decede == t('yes', lang) else "Non" if decede == t('no', lang) else ""
            
            data = {
                'ilot': ilot,
                'logement': logement_num,
                'decision': decision,
                'date_decision': date_decision,
                'nom_affectaire': nom_affectaire,
                'matricule': matricule,
                'nni': nni,
                'profession': profession,
                'fonction': fonction,
                'departement': departement,
                'telephone': telephone,
                'en_activite': en_activite_db,
                'a_la_retraite': a_la_retraite_db,
                'decede': decede_db,
                'nom_repondant': nom_repondant,
                'lien_parente': lien_parente,
                'tel_repondant': tel_repondant,
                'latitude': latitude,
                'longitude': longitude,
                'observation': observation
            }
            
            success, message = st.session_state.db.modifier_logement(st.session_state.edit_id, data)
            if success:
                st.success(t('success_edit', lang))
                del st.session_state.edit_id
                st.rerun()
            else:
                st.error(message)
        
        if cancelled:
            if 'edit_id' in st.session_state:
                del st.session_state.edit_id
            st.rerun()


def afficher_carte_generale():
    """Affiche la carte avec tous les logements"""
    df = st.session_state.db.lire_tous()
    
    if df.empty:
        st.warning(t('no_data', st.session_state.lang))
        return
    
    # Créer la carte centrée sur Nouakchott
    m = folium.Map(
        location=[18.0735, -15.9582],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Couleurs par îlot
    couleurs_ilot = {
        'A': 'red', 'B': 'blue', 'C': 'green', 'D': 'purple',
        'E': 'orange', 'F': 'darkred', 'G': 'lightred', 'H': 'beige',
        'I': 'pink', 'J': 'lightblue', 'K': 'darkgreen', 'L': 'cadetblue'
    }
    
    # Ajouter les marqueurs
    for idx, row in df.iterrows():
        try:
            lat = float(get_safe_value(row, 'latitude', 18.0735))
            lon = float(get_safe_value(row, 'longitude', -15.9582))
            
            if pd.notna(lat) and pd.notna(lon):
                popup_html = f"""
                <div style='min-width: 200px'>
                    <h4>🏠 {get_safe_value(row, 'ilot')}-{get_safe_value(row, 'logement')}</h4>
                    <hr>
                    <b>Affectaire:</b> {get_safe_value(row, 'nom_affectaire', 'N/A')}<br>
                    <b>Profession:</b> {get_safe_value(row, 'profession', 'N/A')}<br>
                    <b>Département:</b> {get_safe_value(row, 'departement', 'N/A')}<br>
                    <b>Téléphone:</b> {get_safe_value(row, 'telephone', 'N/A')}<br>
                    <b>NNI:</b> {get_safe_value(row, 'nni', 'N/A')}<br>
                    <b>En activité:</b> {afficher_valeur_activite(get_safe_value(row, 'en_activite'), st.session_state.lang)}
                </div>
                """
                
                couleur = couleurs_ilot.get(get_safe_value(row, 'ilot', ''), 'gray')
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{get_safe_value(row, 'ilot')}-{get_safe_value(row, 'logement')}: {get_safe_value(row, 'nom_affectaire')}",
                    icon=folium.Icon(color=couleur, icon='home', prefix='fa')
                ).add_to(m)
        except Exception as e:
            continue
    
    # Afficher la carte
    st_folium(m, width=1200, height=600)


def page_carte_filtree():
    """Affiche la carte avec les logements filtrés/sélectionnés"""
    lang = st.session_state.lang
    
    st.markdown(f"<div class='main-header'>{t('map', lang)}</div>", unsafe_allow_html=True)
    
    # Filtres pour la carte
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ilots = [t('all', lang)] + st.session_state.db.obtenir_valeurs_uniques('ilot')
        filtre_ilot = st.selectbox("Filtrer par " + t('ilot', lang), ilots)
    
    with col2:
        depts = [t('all', lang)] + st.session_state.db.obtenir_valeurs_uniques('departement')
        filtre_dept = st.selectbox("Filtrer par " + t('departement', lang), depts)
    
    with col3:
        profs = [t('all', lang)] + st.session_state.db.obtenir_valeurs_uniques('profession')
        filtre_prof = st.selectbox("Filtrer par " + t('profession', lang), profs)
    
    # Construire les filtres
    filtres = {}
    if filtre_ilot != t('all', lang):
        filtres['ilot'] = filtre_ilot
    if filtre_dept != t('all', lang):
        filtres['departement'] = filtre_dept
    if filtre_prof != t('all', lang):
        filtres['profession'] = filtre_prof
    
    df = st.session_state.db.lire_tous(filtres)
    df = nettoyer_dataframe(df, lang)
    
    st.info(f"📍 {len(df)} logements sur la carte")
    
    # Créer la carte
    if not df.empty:
        m = folium.Map(
            location=[18.0735, -15.9582],
            zoom_start=13,
            tiles='OpenStreetMap'
        )
        
        couleurs_ilot = {
            'A': 'red', 'B': 'blue', 'C': 'green', 'D': 'purple',
            'E': 'orange', 'F': 'darkred', 'G': 'lightred', 'H': 'beige'
        }
        
        for idx, row in df.iterrows():
            try:
                lat = float(get_safe_value(row, 'latitude', 18.0735))
                lon = float(get_safe_value(row, 'longitude', -15.9582))
                
                if pd.notna(lat) and pd.notna(lon):
                    popup_html = f"""
                    <div style='min-width: 250px'>
                        <h4 style='color: #1f77b4'>🏠 Logement {get_safe_value(row, 'ilot')}-{get_safe_value(row, 'logement')}</h4>
                        <hr>
                        <table style='width: 100%'>
                            <tr><td><b>Affectaire:</b></td><td>{get_safe_value(row, 'nom_affectaire', 'N/A')}</td></tr>
                            <tr><td><b>NNI:</b></td><td>{get_safe_value(row, 'nni', 'N/A')}</td></tr>
                            <tr><td><b>Profession:</b></td><td>{get_safe_value(row, 'profession', 'N/A')}</td></tr>
                            <tr><td><b>Fonction:</b></td><td>{get_safe_value(row, 'fonction', 'N/A')}</td></tr>
                            <tr><td><b>Département:</b></td><td>{get_safe_value(row, 'departement', 'N/A')}</td></tr>
                            <tr><td><b>Téléphone:</b></td><td>{get_safe_value(row, 'telephone', 'N/A')}</td></tr>
                            <tr><td><b>En activité:</b></td><td>{get_safe_value(row, 'en_activite', 'N/A')}</td></tr>
                        </table>
                    </div>
                    """
                    
                    couleur = couleurs_ilot.get(get_safe_value(row, 'ilot', ''), 'gray')
                    
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_html, max_width=350),
                        tooltip=f"{get_safe_value(row, 'ilot')}-{get_safe_value(row, 'logement')}: {get_safe_value(row, 'nom_affectaire')}",
                        icon=folium.Icon(color=couleur, icon='home', prefix='fa')
                    ).add_to(m)
            except Exception:
                continue
        
        st_folium(m, width=1200, height=700)
        
        # Afficher les détails sous la carte
        st.subheader("📋 Détails des logements affichés")
        colonnes_affichage = ['ilot', 'logement', 'nom_affectaire', 'profession', 
                             'departement', 'telephone', 'en_activite']
        colonnes_disponibles = [col for col in colonnes_affichage if col in df.columns]
        st.dataframe(df[colonnes_disponibles], use_container_width=True)
    else:
        st.warning(t('no_housing', lang))


def page_import_export():
    """Page d'import/export des données"""
    lang = st.session_state.lang
    
    st.markdown(f"<div class='main-header'>{t('import_export', lang)}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 " + t('import', lang))
        
        uploaded_file = st.file_uploader("Choisir un fichier Excel", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            if st.button("Importer les données"):
                try:
                    # Créer un fichier temporaire dans le répertoire temp du système
                    temp_dir = tempfile.gettempdir()
                    temp_path = os.path.join(temp_dir, 'temp_import.xlsx')
                    
                    # Sauvegarder le fichier temporairement
                    with open(temp_path, 'wb') as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Mettre à jour le chemin et importer
                    st.session_state.db.excel_path = temp_path
                    count, message = st.session_state.db.importer_depuis_excel()
                    
                    # Nettoyer le fichier temporaire
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    
                    if count > 0:
                        st.success(t('import_success', lang) + f": {count} logements")
                        st.session_state.data_loaded = True
                        st.balloons()
                    else:
                        st.error(message)
                        
                except Exception as e:
                    st.error(f"❌ {t('error', lang)}: {str(e)}")
                    # Nettoyer en cas d'erreur
                    if 'temp_path' in locals() and os.path.exists(temp_path):
                        os.remove(temp_path)
    
    with col2:
        st.subheader("📤 " + t('export', lang))
        
        nom_fichier = st.text_input(
            "Nom du fichier",
            value=f"logements_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        
        if st.button("Exporter les données"):
            try:
                # Créer le dossier de sortie s'il n'existe pas
                output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, nom_fichier)
                
                success, message = st.session_state.db.exporter_vers_excel(output_path)
                
                if success:
                    st.success(t('export_success', lang))
                    st.info(f"📁 {t('file_saved', lang)}: {output_path}")
                    
                    # Permettre le téléchargement direct
                    try:
                        with open(output_path, 'rb') as f:
                            st.download_button(
                                label="📥 Télécharger le fichier",
                                data=f,
                                file_name=nom_fichier,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    except Exception as e:
                        st.warning(f"Téléchargement non disponible: {str(e)}")
                else:
                    st.error(message)
            except Exception as e:
                st.error(f"❌ {t('error', lang)}: {str(e)}")
    
    # Statistiques d'import/export
    st.subheader("📊 Informations sur les données")
    
    stats = st.session_state.db.obtenir_statistiques()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total des enregistrements", stats.get('total', 0))
    
    with col2:
        st.metric("Îlots différents", len(stats.get('par_ilot', {})))
    
    with col3:
        st.metric("Départements différents", len(stats.get('par_departement', {})))


def page_historique():
    """Page d'historique des modifications"""
    lang = st.session_state.lang
    
    st.markdown(f"<div class='main-header'>{t('history', lang)}</div>", unsafe_allow_html=True)
    
    df_historique = st.session_state.db.obtenir_historique(limit=100)
    
    if not df_historique.empty:
        df_historique = nettoyer_dataframe(df_historique, lang)
        st.dataframe(df_historique, use_container_width=True, height=600)
    else:
        st.info(t('no_data', lang))


def preparer_impression(df):
    """Prépare les données pour l'impression"""
    st.subheader("🖨️ Aperçu pour impression")
    
    # Créer une version formatée pour l'impression
    st.markdown("""
    <style>
    @media print {
        .no-print, .stSidebar, .stButton { display: none !important; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(df, use_container_width=True, height=400)
    
    st.info("💡 Utilisez Ctrl+P (ou Cmd+P sur Mac) pour imprimer cette page")


# ============================================
# FONCTION PRINCIPALE
# ============================================

def main():
    """Fonction principale de l'application"""
    
    # Appliquer les styles CSS
    apply_custom_css()
    
    # Barre latérale
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg", width=100)
        st.title("🏘️ Gestion Logements")
        st.markdown("---")
        
        # Sélection de la langue avec callback
        def change_langue():
            """Callback pour changer la langue"""
            pass
        
        lang_actuelle = st.session_state.lang
        
        lang = st.radio(
            "🌐 " + t('language', lang_actuelle),
            ['fr', 'ar'],
            format_func=lambda x: "🇫🇷 Français" if x == 'fr' else "🇸🇦 العربية",
            index=0 if lang_actuelle == 'fr' else 1,
            key='lang_radio',
            on_change=change_langue
        )
        
        # Mettre à jour la langue si changée
        if lang != st.session_state.lang:
            st.session_state.lang = lang
            st.rerun()
        
        st.markdown("---")
        
        # Menu de navigation
        st.subheader(t('menu', lang))
        
        if st.button("📊 " + t('dashboard', lang), use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
        
        if st.button("📋 " + t('list', lang), use_container_width=True):
            st.session_state.page = 'list'
            st.rerun()
        
        if st.button("➕ " + t('add', lang), use_container_width=True):
            st.session_state.page = 'add'
            st.rerun()
        
        if st.button("🗺️ " + t('map', lang), use_container_width=True):
            st.session_state.page = 'map_filtered'
            st.rerun()
        
        if st.button("💾 " + t('import_export', lang), use_container_width=True):
            st.session_state.page = 'import_export'
            st.rerun()
        
        if st.button("📜 " + t('history', lang), use_container_width=True):
            st.session_state.page = 'history'
            st.rerun()
        
        st.markdown("---")
        st.caption("© 2024 - Système de Gestion")
        st.caption("Nouakchott, Mauritanie 🇲🇷")
    
    # Affichage de la page sélectionnée
    try:
        if st.session_state.page == 'dashboard':
            page_dashboard()
        elif st.session_state.page == 'list':
            page_liste()
        elif st.session_state.page == 'add':
            page_ajout()
        elif st.session_state.page == 'edit':
            page_modification()
        elif st.session_state.page == 'map_filtered':
            page_carte_filtree()
        elif st.session_state.page == 'import_export':
            page_import_export()
        elif st.session_state.page == 'history':
            page_historique()
        else:
            page_dashboard()
    except Exception as e:
        st.error(f"❌ {t('error', st.session_state.lang)}: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
