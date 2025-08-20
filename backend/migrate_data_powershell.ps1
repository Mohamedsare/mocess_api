# Script de migration des données SQLite vers PostgreSQL
Write-Host "🚀 Migration des données SQLite vers PostgreSQL" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Étape 1: Sauvegarder les données SQLite
Write-Host "📋 Étape 1: Sauvegarde des données SQLite" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

$env:DB_ENGINE = "sqlite3"

try {
    python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > sqlite_data_backup.json
    Write-Host "✅ Sauvegarde SQLite réussie" -ForegroundColor Green
    
    # Vérifier la taille du fichier
    $backupFile = Get-Item "sqlite_data_backup.json" -ErrorAction SilentlyContinue
    if ($backupFile -and $backupFile.Length -gt 0) {
        Write-Host "📊 Taille du fichier de sauvegarde: $($backupFile.Length) bytes" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️ Aucune donnée trouvée dans SQLite" -ForegroundColor Yellow
        exit 0
    }
} catch {
    Write-Host "❌ Erreur lors de la sauvegarde SQLite: $_" -ForegroundColor Red
    exit 1
}

# Étape 2: Restaurer vers PostgreSQL
Write-Host ""
Write-Host "📋 Étape 2: Restauration vers PostgreSQL" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

$env:DB_ENGINE = "postgresql"
$env:DB_NAME = "mocess_db"
$env:DB_USER = "mocess_user"
$env:DB_PASSWORD = "@Basbedo@123"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"

try {
    # Essayer de charger les données avec gestion d'encodage
    python manage.py loaddata sqlite_data_backup.json
    Write-Host "✅ Restauration PostgreSQL réussie" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur lors de la restauration PostgreSQL: $_" -ForegroundColor Red
    
    # Essayer une approche alternative
    Write-Host "🔄 Tentative avec approche alternative..." -ForegroundColor Yellow
    try {
        # Recréer le fichier avec l'encodage correct
        $content = Get-Content "sqlite_data_backup.json" -Raw -Encoding UTF8
        $content | Out-File "sqlite_data_backup_fixed.json" -Encoding UTF8
        
        python manage.py loaddata sqlite_data_backup_fixed.json
        Write-Host "✅ Restauration PostgreSQL réussie (approche alternative)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Échec de l'approche alternative: $_" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "🎉 MIGRATION DES DONNÉES TERMINÉE AVEC SUCCÈS!" -ForegroundColor Green
Write-Host "✅ Toutes les données ont été migrées de SQLite vers PostgreSQL" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Prochaines étapes:" -ForegroundColor Yellow
Write-Host "1. Tester l'application: python test_final.py" -ForegroundColor White
Write-Host "2. Démarrer le serveur: python manage.py runserver" -ForegroundColor White
Write-Host "3. Vérifier les données dans l'admin Django" -ForegroundColor White
Write-Host "4. Supprimer db.sqlite3 si tout fonctionne" -ForegroundColor White
