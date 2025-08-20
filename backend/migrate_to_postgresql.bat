@echo off
echo ========================================
echo Migration SQLite vers PostgreSQL
echo ========================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé!
    echo Veuillez créer un environnement virtuel d'abord:
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Vérifier les dépendances
echo 📦 Vérification des dépendances...
python -c "import psycopg2" 2>nul
if errorlevel 1 (
    echo ❌ psycopg2-binary non installé!
    echo Installation en cours...
    pip install psycopg2-binary
)

REM Exécuter la migration
echo 🚀 Début de la migration...
python migrate_to_postgresql.py

REM Vérifier la migration
echo.
echo 🔍 Vérification de la migration...
python verify_migration.py

echo.
echo ========================================
echo Migration terminée!
echo ========================================
echo.
echo 📝 Prochaines étapes:
echo 1. Tester votre application
echo 2. Vérifier que toutes les données sont présentes
echo 3. Mettre à jour votre fichier .env avec DB_ENGINE=postgresql
echo.
pause
