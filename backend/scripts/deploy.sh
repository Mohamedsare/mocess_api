#!/bin/bash
# Script de déploiement automatisé pour Mocess

echo "🚀 Déploiement de Mocess en cours..."

# Vérifications préalables
echo "🔍 Vérifications préalables..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: manage.py non trouvé. Assurez-vous d'être dans le répertoire backend/"
    exit 1
fi

# Vérifier que les variables d'environnement sont définies
if [ -z "$SECRET_KEY" ] || [ -z "$ALLOWED_HOSTS" ]; then
    echo "❌ Erreur: Variables d'environnement manquantes (SECRET_KEY, ALLOWED_HOSTS)"
    echo "💡 Définissez ces variables avant le déploiement"
    exit 1
fi

# Tests de configuration
echo "🧪 Tests de configuration..."
python manage.py check --deploy
if [ $? -ne 0 ]; then
    echo "❌ Erreur dans la configuration Django"
    exit 1
fi

# Sauvegarde avant déploiement
echo "💾 Sauvegarde avant déploiement..."
if [ -f "scripts/backup.sh" ]; then
    chmod +x scripts/backup.sh
    ./scripts/backup.sh
fi

# Migrations
echo "📊 Application des migrations..."
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors des migrations"
    exit 1
fi

# Collecte des fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de la collecte des statiques"
    exit 1
fi

# Créer les répertoires nécessaires
echo "📂 Création des répertoires..."
mkdir -p logs media backups

# Test final
echo "🔧 Test final de l'application..."
python manage.py check
if [ $? -eq 0 ]; then
    echo "✅ Déploiement réussi !"
    echo "🌐 Votre application Mocess est prête"
else
    echo "❌ Erreur lors du test final"
    exit 1
fi

echo "🎉 Déploiement terminé avec succès !"
