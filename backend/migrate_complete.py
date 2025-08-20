#!/usr/bin/env python
"""
Script de migration complète SQLite vers PostgreSQL
Ce script configure PostgreSQL et migre toutes les données
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
from setup_postgresql import setup_postgresql

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

def test_postgresql_connection():
    """Teste la connexion PostgreSQL"""
    print("🧪 Test de connexion PostgreSQL...")
    
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

def verify_migration():
    """Vérifie que la migration s'est bien passée"""
    print("🔍 Vérification de la migration...")
    
    try:
        # Compter les objets dans chaque modèle
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
        
        total_objects = 0
        for model_name in models:
            try:
                model = globals()[model_name]
                count = model.objects.count()
                print(f"📊 {model_name}: {count} objets")
                total_objects += count
            except Exception as e:
                print(f"❌ Erreur lors du comptage de {model_name}: {e}")
        
        print(f"🎯 Total: {total_objects} objets migrés")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Fonction principale de migration"""
    print("🚀 Début de la migration complète SQLite vers PostgreSQL")
    print("=" * 60)
    
    # Étape 1: Sauvegarder les données SQLite
    backup_file = backup_sqlite_data()
    
    # Étape 2: Configurer PostgreSQL
    print("\n" + "=" * 60)
    if not setup_postgresql():
        print("❌ Impossible de configurer PostgreSQL. Arrêt de la migration.")
        return
    
    # Étape 3: Tester la connexion PostgreSQL
    print("\n" + "=" * 60)
    if not test_postgresql_connection():
        print("❌ Impossible de se connecter à PostgreSQL. Arrêt de la migration.")
        return
    
    # Étape 4: Migrer le schéma
    print("\n" + "=" * 60)
    if not migrate_schema():
        print("❌ Impossible de migrer le schéma. Arrêt de la migration.")
        return
    
    # Étape 5: Restaurer les données
    print("\n" + "=" * 60)
    if not restore_data_from_backup(backup_file):
        print("❌ Impossible de restaurer les données. Arrêt de la migration.")
        return
    
    # Étape 6: Vérifier la migration
    print("\n" + "=" * 60)
    verify_migration()
    
    print("\n" + "=" * 60)
    print("🎉 Migration complète terminée avec succès!")
    print("📝 Prochaines étapes:")
    print("   1. Tester votre application: python manage.py runserver")
    print("   2. Vérifier l'interface d'administration")
    print("   3. Tester les API endpoints")
    print("   4. Sauvegarder le fichier sqlite_backup.json")
    print("   5. Supprimer le fichier db.sqlite3 si tout fonctionne")

if __name__ == '__main__':
    main()
