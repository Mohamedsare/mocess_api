# Script de migration SQLite vers PostgreSQL
Write-Host "Starting SQLite to PostgreSQL migration" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Configuration PostgreSQL
$env:DB_ENGINE = "postgresql"
$env:DB_NAME = "mocess_db"
$env:DB_USER = "mocess_user"
$env:DB_PASSWORD = "@Basbedo@123"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"

# Step 1: Backup SQLite data
Write-Host "`nStep 1: Backing up SQLite data..." -ForegroundColor Yellow
$env:DB_ENGINE = "sqlite3"
try {
    python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > sqlite_backup.json
    Write-Host "SQLite backup completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to backup SQLite data: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Test PostgreSQL connection
Write-Host "`nStep 2: Testing PostgreSQL connection..." -ForegroundColor Yellow
$env:DB_ENGINE = "postgresql"
try {
    python -c "import psycopg2; conn = psycopg2.connect(host='localhost', port='5432', database='mocess_db', user='mocess_user', password='@Basbedo@123'); print('PostgreSQL connection successful'); conn.close()"
    Write-Host "PostgreSQL connection test successful" -ForegroundColor Green
} catch {
    Write-Host "Failed to connect to PostgreSQL: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Migrate schema
Write-Host "`nStep 3: Migrating schema..." -ForegroundColor Yellow
try {
    python manage.py migrate --fake-initial
    python manage.py migrate
    Write-Host "Schema migration completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to migrate schema: $_" -ForegroundColor Red
    exit 1
}

# Step 4: Load data
Write-Host "`nStep 4: Loading data..." -ForegroundColor Yellow
try {
    python manage.py loaddata sqlite_backup.json
    Write-Host "Data loading completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to load data: $_" -ForegroundColor Red
    exit 1
}

# Step 5: Verify migration
Write-Host "`nStep 5: Verifying migration..." -ForegroundColor Yellow
try {
    python manage.py shell -c "from api.models import *; print('Migration verification completed')"
    Write-Host "Migration verification completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to verify migration: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "Migration completed successfully!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test application: python manage.py runserver" -ForegroundColor White
Write-Host "2. Check admin interface" -ForegroundColor White
Write-Host "3. Test API endpoints" -ForegroundColor White
Write-Host "4. Backup sqlite_backup.json file" -ForegroundColor White
Write-Host "5. Remove db.sqlite3 if everything works" -ForegroundColor White
