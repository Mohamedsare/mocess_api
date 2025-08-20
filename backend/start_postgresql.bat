@echo off
echo ========================================
echo SiteMocess - Demarrage avec PostgreSQL
echo ========================================
echo.

echo Configuration de l'environnement...
set DB_ENGINE=postgresql
set DB_NAME=mocess_db
set DB_USER=mocess_user
set DB_PASSWORD=@Basbedo@123
set DB_HOST=localhost
set DB_PORT=5432

echo.
echo Test de la connexion PostgreSQL...
python -c "import psycopg2; conn = psycopg2.connect(host='localhost', port='5432', database='mocess_db', user='mocess_user', password='@Basbedo@123'); print('PostgreSQL connection successful'); conn.close()"

if %errorlevel% neq 0 (
    echo.
    echo ERREUR: Impossible de se connecter a PostgreSQL
    echo Verifiez que PostgreSQL est en cours d'execution
    echo.
    pause
    exit /b 1
)

echo.
echo Demarrage du serveur Django...
echo.
echo L'application sera accessible sur:
echo - Interface d'administration: http://localhost:8000/admin/
echo - API: http://localhost:8000/api/
echo - Frontend: http://localhost:3000/
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

python manage.py runserver

pause
