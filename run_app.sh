#!/bin/bash

# Script de lancement de l'application de gestion des logements
# Nouakchott, Mauritanie

echo "=========================================="
echo "🏘️  Gestion des Logements - Nouakchott"
echo "=========================================="
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python 3 détecté: $(python3 --version)"
echo ""

# Vérifier que pip est installé
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip n'est pas installé"
    exit 1
fi

echo "✅ pip détecté"
echo ""

# Installer les dépendances si nécessaire
echo "📦 Installation des dépendances..."
pip install -q -r requirements.txt
echo "✅ Dépendances installées"
echo ""

# Vérifier que le fichier Excel existe
if [ ! -f "logements.xlsx" ]; then
    echo "⚠️  Attention: logements.xlsx n'est pas trouvé"
    echo "   L'application démarrera mais vous devrez importer un fichier Excel"
else
    echo "✅ Fichier logements.xlsx trouvé"
fi
echo ""

# Lancer l'application
echo "🚀 Lancement de l'application..."
echo "   L'application s'ouvrira dans votre navigateur"
echo "   URL: http://localhost:8501"
echo ""
echo "   Appuyez sur Ctrl+C pour arrêter l'application"
echo ""
echo "=========================================="

streamlit run app.py
