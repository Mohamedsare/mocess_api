#!/usr/bin/env python
"""
Script de migration de SQLite vers PostgreSQL
Ce script sauvegarde les données SQLite et les transfère vers PostgreSQL
"""

import os
import sys
import django
import json
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocess_backend.settings')

# Import Django après configuration
django.setup()

from django.core.management import call_command
from django.db import connections
from django.conf import settings
from api.models import *

def backup_sqlite_data():
    """Sauvegarde toutes les données SQLite dans un fichier JSON"""
    print("🔍 Sauvegarde des données SQLite...")
    
    # Liste de tous les modèles de l'application api
    models = [
        'Category',
        'Project',
        'ProjectImage',
        'News',
        'NewsImage',
        'Publication',
        'Resource',
        'ContactForm',
        'PartnershipForm',
        'NewsletterSubscription',
        'TeamMember',
        'Partner',
        'EventRegistration',
        'ExternalLink',
    ]
    
    backup_data = {}
    
    for model_name in models:
        try:
            model = globals()[model_name]
            objects = model.objects.all()
            backup_data[model_name] = []
            
            for obj in objects:
                # Convertir l'objet en dictionnaire
                obj_data = {}
                for field in obj._meta.fields:
                    value = getattr(obj, field.name)
                    # Gérer les types spéciaux
                    if hasattr(value, 'isoformat'):  # Pour les dates
                        value = value.isoformat()
                    elif hasattr(value, 'url'):  # Pour les ImageField/FileField
                        value = str(value) if value else None
                    obj_data[field.name] = value
                
                backup_data[model_name].append(obj_data)
            
            print(f"✅ {model_name}: {len(backup_data[model_name])} objets sauvegardés")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde de {model_name}: {e}")
    
    # Sauvegarder dans un fichier JSON
    backup_file = BASE_DIR / 'sqlite_backup.json'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Sauvegarde complète sauvegardée dans: {backup_file}")
    return backup_file

def setup_postgresql():
    """Configure la base de données PostgreSQL"""
    print("🔧 Configuration de PostgreSQL...")
    
    # Vérifier si PostgreSQL est configuré
    if 'postgresql' not in settings.DATABASES['default']['ENGINE']:
        print("❌ PostgreSQL n'est pas configuré dans settings.py")
        print("Assurez-vous que DB_ENGINE=postgresql dans votre fichier .env")
        return False
    
    # Tester la connexion PostgreSQL
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Connexion PostgreSQL réussie: {version[0]}")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion PostgreSQL: {e}")
        return False

def migrate_schema():
    """Migre le schéma vers PostgreSQL"""
    print("🏗️ Migration du schéma vers PostgreSQL...")
    
    try:
        # Supprimer les migrations existantes si nécessaire
        call_command('migrate', '--fake-initial')
        
        # Appliquer toutes les migrations
        call_command('migrate')
        print("✅ Schéma migré avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la migration du schéma: {e}")
        return False

def restore_data_from_backup(backup_file):
    """Restaure les données depuis la sauvegarde SQLite"""
    print("📥 Restauration des données depuis la sauvegarde...")
    
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        for model_name, objects_data in backup_data.items():
            try:
                model = globals()[model_name]
                print(f"🔄 Restauration de {model_name}...")
                
                for obj_data in objects_data:
                    # Créer l'objet sans l'ID pour éviter les conflits
                    if 'id' in obj_data:
                        del obj_data['id']
                    
                    # Gérer les champs spéciaux
                    for field_name, value in obj_data.items():
                        if value and isinstance(value, str):
                            # Vérifier si c'est un chemin de fichier
                            if field_name in ['image', 'photo', 'file'] and value.startswith('/'):
                                # Copier le fichier vers le nouveau chemin
                                old_path = BASE_DIR / value.lstrip('/')
                                if old_path.exists():
                                    # Créer le nouveau chemin
                                    new_path = settings.MEDIA_ROOT / Path(value).name
                                    new_path.parent.mkdir(parents=True, exist_ok=True)
                                    import shutil
                                    shutil.copy2(old_path, new_path)
                                    obj_data[field_name] = str(new_path.relative_to(settings.MEDIA_ROOT))
                    
                    # Créer l'objet
                    model.objects.create(**obj_data)
                
                print(f"✅ {model_name}: {len(objects_data)} objets restaurés")
                
            except Exception as e:
                print(f"❌ Erreur lors de la restauration de {model_name}: {e}")
        
        print("✅ Restauration des données terminée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la restauration: {e}")
        return False

def main():
    """Fonction principale de migration"""
    print("🚀 Début de la migration SQLite vers PostgreSQL")
    print("=" * 50)
    
    # Étape 1: Sauvegarder les données SQLite
    backup_file = backup_sqlite_data()
    
    # Étape 2: Configurer PostgreSQL
    if not setup_postgresql():
        print("❌ Impossible de configurer PostgreSQL. Arrêt de la migration.")
        return
    
    # Étape 3: Migrer le schéma
    if not migrate_schema():
        print("❌ Impossible de migrer le schéma. Arrêt de la migration.")
        return
    
    # Étape 4: Restaurer les données
    if not restore_data_from_backup(backup_file):
        print("❌ Impossible de restaurer les données. Arrêt de la migration.")
        return
    
    print("=" * 50)
    print("🎉 Migration terminée avec succès!")
    print("📝 N'oubliez pas de:")
    print("   1. Tester votre application")
    print("   2. Sauvegarder le fichier sqlite_backup.json")
    print("   3. Mettre à jour votre fichier .env avec DB_ENGINE=postgresql")

if __name__ == '__main__':
    main()
