@echo off
echo ========================================
echo Migration SQLite vers PostgreSQL
echo ========================================
echo.

echo Verifying Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Verifying PostgreSQL service...
sc query postgresql-x64-17 | find "RUNNING"
if %errorlevel% neq 0 (
    echo WARNING: PostgreSQL service might not be running
    echo Please ensure PostgreSQL is installed and running
    echo.
)

echo.
echo Starting migration process...
echo ========================================
python migrate_complete.py

echo.
echo ========================================
echo Migration completed!
echo ========================================
echo.
echo Next steps:
echo 1. Test the application: python manage.py runserver
echo 2. Check admin interface
echo 3. Test API endpoints
echo 4. Backup sqlite_backup.json file
echo 5. Remove db.sqlite3 if everything works
echo.
pause
