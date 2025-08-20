#!/bin/bash

# Script de démarrage pour SiteMocess en production

echo "🚀 Démarrage de SiteMocess..."

# Attendre que la base de données soit prête
echo "⏳ Attente de la base de données..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
    sleep 2
done
echo "✅ Base de données prête!"

# Appliquer les migrations
echo "🔄 Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer un superutilisateur si nécessaire
echo "👤 Vérification du superutilisateur..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@mocess.com', 'admin123')
    print('Superutilisateur créé: admin/admin123')
else:
    print('Superutilisateur existe déjà')
"

# Démarrer Gunicorn
echo "🌐 Démarrage du serveur..."
exec gunicorn mocess_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
