#!/bin/bash

echo "========================================"
echo "Migration SQLite vers PostgreSQL"
echo "========================================"
echo

# Vérifier si l'environnement virtuel existe
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Environnement virtuel non trouvé!"
    echo "Veuillez créer un environnement virtuel d'abord:"
    echo "python3 -m venv venv"
    echo "source venv/bin/activate"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
python -c "import psycopg2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ psycopg2-binary non installé!"
    echo "Installation en cours..."
    pip install psycopg2-binary
fi

# Vérifier que PostgreSQL est installé
echo "🔍 Vérification de PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL non installé!"
    echo "Veuillez installer PostgreSQL:"
    echo "Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    echo "macOS: brew install postgresql"
    exit 1
fi

# Exécuter la migration
echo "🚀 Début de la migration..."
python migrate_to_postgresql.py

# Vérifier la migration
echo
echo "🔍 Vérification de la migration..."
python verify_migration.py

echo
echo "========================================"
echo "Migration terminée!"
echo "========================================"
echo
echo "📝 Prochaines étapes:"
echo "1. Tester votre application"
echo "2. Vérifier que toutes les données sont présentes"
echo "3. Mettre à jour votre fichier .env avec DB_ENGINE=postgresql"
echo
