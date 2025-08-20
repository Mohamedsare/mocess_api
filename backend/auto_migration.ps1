# Script automatique de migration SQLite vers PostgreSQL
Write-Host "🚀 Migration automatique SQLite vers PostgreSQL" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Test de connexion PostgreSQL
Write-Host "🧪 Test de connexion PostgreSQL..." -ForegroundColor Yellow
$testResult = psql -U mocess_user -d mocess_db -h localhost -c "SELECT 1;" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Connexion PostgreSQL réussie !" -ForegroundColor Green
    Write-Host ""
    
    # Lancement de la migration
    Write-Host "🔄 Lancement de la migration..." -ForegroundColor Yellow
    C:\Users\hp\AppData\Local\Programs\Python\Python311\python.exe migrate_to_postgresql.py
    
    Write-Host ""
    Write-Host "🔍 Vérification de la migration..." -ForegroundColor Yellow
    C:\Users\hp\AppData\Local\Programs\Python\Python311\python.exe verify_migration.py
    
    Write-Host ""
    Write-Host "🎉 Migration terminée !" -ForegroundColor Green
    Write-Host "Vérifiez dans pgAdmin que toutes les tables ont été créées." -ForegroundColor Cyan
    
} else {
    Write-Host "❌ Échec de la connexion PostgreSQL" -ForegroundColor Red
    Write-Host "Erreur: $testResult" -ForegroundColor Red
    Write-Host ""
    Write-Host "Vérifiez dans pgAdmin:" -ForegroundColor Yellow
    Write-Host "1. Que l'utilisateur mocess_user existe" -ForegroundColor Yellow
    Write-Host "2. Que les permissions sont données" -ForegroundColor Yellow
    Write-Host "3. Que la base de données mocess_db existe" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
