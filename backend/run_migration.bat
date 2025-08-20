@echo off
echo ========================================
echo SiteMocess - Migration SQLite vers PostgreSQL
echo ========================================
echo.

echo [1/5] Verifying Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo [2/5] Verifying PostgreSQL service...
sc query postgresql-x64-17 | find "RUNNING"
if %errorlevel% neq 0 (
    echo WARNING: PostgreSQL service might not be running
    echo Please ensure PostgreSQL is installed and running
    echo.
    echo To start PostgreSQL service:
    echo net start postgresql-x64-17
    echo.
)

echo.
echo [3/5] Checking current database configuration...
echo Current DB_ENGINE setting:
findstr "DB_ENGINE" env

echo.
echo [4/5] Starting migration process...
echo ========================================
python migrate_direct.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Migration failed!
    echo Please check the error messages above.
    echo.
    echo Troubleshooting:
    echo 1. Ensure PostgreSQL is running
    echo 2. Check database credentials in env file
    echo 3. Verify database and user exist in PostgreSQL
    pause
    exit /b 1
)

echo.
echo [5/5] Migration completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Test the application: python manage.py runserver
echo 2. Check admin interface: http://localhost:8000/admin/
echo 3. Test API endpoints
echo 4. Backup sqlite_backup.json file
echo 5. Remove db.sqlite3 if everything works
echo.
echo Migration completed! Press any key to exit...
pause
