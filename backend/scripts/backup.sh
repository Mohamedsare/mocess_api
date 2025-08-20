#!/bin/bash
# Script de sauvegarde pour Mocess

echo "💾 Démarrage de la sauvegarde Mocess..."

# Créer le répertoire de sauvegarde s'il n'existe pas
mkdir -p backups

# Générer le nom de fichier avec timestamp
BACKUP_FILE="backups/mocess_backup_$(date +%Y%m%d_%H%M%S).json"

# Sauvegarder les données
echo "📊 Sauvegarde des données de l'application..."
python manage.py dumpdata --natural-foreign --natural-primary \
    -e contenttypes -e auth.Permission > "$BACKUP_FILE"

# Vérifier que la sauvegarde s'est bien passée
if [ $? -eq 0 ]; then
    echo "✅ Sauvegarde réussie : $BACKUP_FILE"
    echo "📏 Taille : $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "❌ Erreur lors de la sauvegarde"
    exit 1
fi

# Nettoyer les anciennes sauvegardes (garder seulement les 7 dernières)
echo "🧹 Nettoyage des anciennes sauvegardes..."
find backups/ -name "mocess_backup_*.json" -type f -mtime +7 -delete

echo "🎉 Sauvegarde terminée avec succès !"
