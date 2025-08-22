#!/bin/bash

# Script de démarrage robuste pour Railway
# Gère la variable PORT et les fallbacks

# Définir le port par défaut si $PORT n'est pas défini
export PORT=${PORT:-8000}

echo "🚀 Démarrage de l'application Django sur le port $PORT"

# Vérifier que le port est valide
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
    echo "❌ Erreur: PORT invalide: $PORT"
    echo "🔧 Utilisation du port par défaut: 8000"
    export PORT=8000
fi

echo "✅ Port configuré: $PORT"

# Démarrer Gunicorn
exec gunicorn mocess_backend.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
