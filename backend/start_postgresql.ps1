# Script de démarrage SiteMocess avec PostgreSQL
Write-Host "========================================" -ForegroundColor Green
Write-Host "SiteMocess - Démarrage avec PostgreSQL" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Configuration de l'environnement
$env:DB_ENGINE = "postgresql"
$env:DB_NAME = "mocess_db"
$env:DB_USER = "mocess_user"
$env:DB_PASSWORD = "@Basbedo@123"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"

Write-Host "Configuration de l'environnement..." -ForegroundColor Yellow

Write-Host ""
Write-Host "Test de la connexion PostgreSQL..." -ForegroundColor Yellow
try {
    python -c "import psycopg2; conn = psycopg2.connect(host='localhost', port='5432', database='mocess_db', user='mocess_user', password='@Basbedo@123'); print('PostgreSQL connection successful'); conn.close()"
    Write-Host "✅ Connexion PostgreSQL réussie" -ForegroundColor Green
} catch {
    Write-Host "❌ ERREUR: Impossible de se connecter à PostgreSQL" -ForegroundColor Red
    Write-Host "Vérifiez que PostgreSQL est en cours d'exécution" -ForegroundColor Red
    Write-Host ""
    Read-Host "Appuyez sur Entrée pour continuer"
    exit 1
}

Write-Host ""
Write-Host "Démarrage du serveur Django..." -ForegroundColor Yellow
Write-Host ""
Write-Host "L'application sera accessible sur:" -ForegroundColor Cyan
Write-Host "- Interface d'administration: http://localhost:8000/admin/" -ForegroundColor White
Write-Host "- API: http://localhost:8000/api/" -ForegroundColor White
Write-Host "- Frontend: http://localhost:3000/" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver
