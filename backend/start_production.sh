#!/bin/bash
# Script de démarrage pour l'hébergement

echo "🚀 Démarrage de Mocess en production..."

# Appliquer les migrations
echo "📊 Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer le répertoire de logs si nécessaire
mkdir -p logs

# Démarrer Gunicorn
echo "🌐 Démarrage du serveur Gunicorn..."
gunicorn mocess_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3
