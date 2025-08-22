@echo off
REM Script de démarrage Windows pour Railway
REM Gère la variable PORT et les fallbacks

REM Définir le port par défaut si %PORT% n'est pas défini
if "%PORT%"=="" set PORT=8000

echo 🚀 Démarrage de l'application Django sur le port %PORT%

REM Vérifier que le port est valide (basique)
echo %PORT%| findstr /r "^[0-9]*$" >nul
if errorlevel 1 (
    echo ❌ Erreur: PORT invalide: %PORT%
    echo 🔧 Utilisation du port par défaut: 8000
    set PORT=8000
)

echo ✅ Port configuré: %PORT%

REM Démarrer Gunicorn
gunicorn mocess_backend.wsgi:application --bind 0.0.0.0:%PORT% --workers 4 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100 --access-logfile - --error-logfile - --log-level info
