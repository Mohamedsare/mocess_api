#!/usr/bin/env python
"""
Script final pour migrer les données de SQLite vers PostgreSQL
"""

import os
import sys
import django
import json
from pathlib import Path

def setup_django_sqlite():
    """Configurer Django pour SQLite"""
    os.environ['DB_ENGINE'] = 'sqlite3'
    
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.append(str(BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocess_backend.settings')
    
    django.setup()
    return BASE_DIR

def setup_django_postgresql():
    """Configurer Django pour PostgreSQL"""
    os.environ['DB_ENGINE'] = 'postgresql'
    os.environ['DB_NAME'] = 'mocess_db'
    os.environ['DB_USER'] = 'mocess_user'
    os.environ['DB_PASSWORD'] = '@Basbedo@123'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.append(str(BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocess_backend.settings')
    
    django.setup()
    return BASE_DIR

def backup_sqlite_data():
    """Sauvegarder les données SQLite"""
    print("🔍 Configuration Django pour SQLite...")
    BASE_DIR = setup_django_sqlite()
    
    from api.models import *
    
    print("📦 Sauvegarde des données SQLite...")
    
    # Liste des modèles à sauvegarder
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
    
    backup_data = []
    total_objects = 0
    
    for model_name in models:
        try:
            model = globals()[model_name]
            objects = model.objects.all()
            
            for obj in objects:
                obj_data = {
                    'model': f'api.{model_name.lower()}',
                    'pk': obj.pk,
                    'fields': {}
                }
                
                for field in obj._meta.fields:
                    if field.name != 'id':
                        value = getattr(obj, field.name)
                        if hasattr(value, 'isoformat'):
                            value = value.isoformat()
                        elif hasattr(value, 'url'):
                            value = str(value) if value else None
                        obj_data['fields'][field.name] = value
                
                backup_data.append(obj_data)
            
            count = objects.count()
            total_objects += count
            print(f"✅ {model_name}: {count} objets sauvegardés")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde de {model_name}: {e}")
    
    # Sauvegarder dans un fichier JSON
    backup_file = BASE_DIR / 'final_backup.json'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Sauvegarde sauvegardée dans: {backup_file}")
    print(f"📊 Total: {total_objects} objets sauvegardés")
    
    return backup_file, backup_data

def restore_to_postgresql(backup_file):
    """Restaurer les données vers PostgreSQL"""
    print("\n🔍 Configuration Django pour PostgreSQL...")
    BASE_DIR = setup_django_postgresql()
    
    from api.models import *
    from django.conf import settings
    
    print("📦 Restauration des données vers PostgreSQL...")
    
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        total_restored = 0
        
        for item in backup_data:
            try:
                model_name = item['model'].split('.')[-1]
                model = globals()[model_name.capitalize()]
                fields = item['fields']
                
                # Gérer les champs de fichiers/images
                for field_name, value in fields.items():
                    if value and isinstance(value, str):
                        if field_name in ['image', 'photo', 'file'] and value.startswith('/'):
                            old_path = BASE_DIR / value.lstrip('/')
                            if old_path.exists():
                                new_path = settings.MEDIA_ROOT / Path(value).name
                                new_path.parent.mkdir(parents=True, exist_ok=True)
                                import shutil
                                shutil.copy2(old_path, new_path)
                                fields[field_name] = str(new_path.relative_to(settings.MEDIA_ROOT))
                
                # Créer l'objet
                model.objects.create(**fields)
                total_restored += 1
                
            except Exception as e:
                print(f"⚠️ Erreur lors de la restauration d'un objet {item.get('model', 'unknown')}: {e}")
                continue
        
        print(f"\n🎉 Restauration terminée! {total_restored} objets restaurés vers PostgreSQL")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la restauration: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Migration finale des données SQLite vers PostgreSQL")
    print("=" * 60)
    
    # Étape 1: Sauvegarder les données SQLite
    print("\n📋 Étape 1: Sauvegarde des données SQLite")
    print("-" * 40)
    
    try:
        backup_file, backup_data = backup_sqlite_data()
        
        # Vérifier s'il y a des données
        if len(backup_data) == 0:
            print("⚠️ Aucune donnée trouvée dans SQLite. Migration terminée.")
            return
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return
    
    # Étape 2: Restaurer vers PostgreSQL
    print("\n📋 Étape 2: Restauration vers PostgreSQL")
    print("-" * 40)
    
    try:
        success = restore_to_postgresql(backup_file)
        if success:
            print("\n" + "=" * 60)
            print("🎉 MIGRATION DES DONNÉES TERMINÉE AVEC SUCCÈS!")
            print("✅ Toutes les données ont été migrées de SQLite vers PostgreSQL")
            print("\n📋 Prochaines étapes:")
            print("1. Tester l'application: python test_final.py")
            print("2. Démarrer le serveur: python manage.py runserver")
            print("3. Vérifier les données dans l'admin Django")
            print("4. Supprimer db.sqlite3 si tout fonctionne")
        else:
            print("\n❌ La migration a échoué. Vérifiez les erreurs ci-dessus.")
            
    except Exception as e:
        print(f"❌ Erreur lors de la restauration: {e}")

if __name__ == '__main__':
    main()
