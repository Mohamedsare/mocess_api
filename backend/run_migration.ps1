# Script de migration SQLite vers PostgreSQL
Write-Host "========================================" -ForegroundColor Green
Write-Host "Migration SQLite vers PostgreSQL" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Chemin vers Python
$pythonPath = "C:\Users\hp\AppData\Local\Programs\Python\Python311\python.exe"

# Vérifier que Python existe
if (-not (Test-Path $pythonPath)) {
    Write-Host "❌ Python non trouvé à: $pythonPath" -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour continuer"
    exit 1
}

Write-Host "✅ Python trouvé: $pythonPath" -ForegroundColor Green

# Installer les dépendances
Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow
& $pythonPath -m pip install -r requirements.txt

# Exécuter la migration
Write-Host "🚀 Début de la migration..." -ForegroundColor Yellow
& $pythonPath migrate_to_postgresql.py

# Vérifier la migration
Write-Host ""
Write-Host "🔍 Vérification de la migration..." -ForegroundColor Yellow
& $pythonPath verify_migration.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Migration terminée!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Read-Host "Appuyez sur Entrée pour continuer"
