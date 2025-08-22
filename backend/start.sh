#!/bin/bash

# Script de démarrage robuste pour Railway
# Gère la variable PORT et les fallbacks

echo "🚀 Démarrage de l'application Django sur Railway"

# Vérifier que la variable PORT est définie par Railway
if [ -z "$PORT" ]; then
    echo "❌ Erreur: Variable PORT non définie par Railway"
    echo "🔧 Utilisation du port par défaut: 8000"
    export PORT=8000
else
    echo "✅ Port Railway détecté: $PORT"
fi

# Vérifier que le port est valide
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
    echo "❌ Erreur: PORT invalide: $PORT"
    echo "🔧 Utilisation du port par défaut: 8000"
    export PORT=8000
fi

echo "✅ Port final configuré: $PORT"

# Démarrer Gunicorn avec la configuration Railway
exec gunicorn mocess_backend.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --preload
