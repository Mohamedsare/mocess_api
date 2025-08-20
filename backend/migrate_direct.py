#!/usr/bin/env python
"""
Direct migration script SQLite to PostgreSQL using Django
"""

import os
import sys
import django
import json
from pathlib import Path

# Django setup
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocess_backend.settings')

django.setup()

from django.core.management import call_command
from django.db import connections
from django.conf import settings
from api.models import *

def backup_sqlite_data():
    """Backup all SQLite data to JSON file"""
    print("Backing up SQLite data...")
    
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
                obj_data = {}
                for field in obj._meta.fields:
                    value = getattr(obj, field.name)
                    if hasattr(value, 'isoformat'):
                        value = value.isoformat()
                    elif hasattr(value, 'url'):
                        value = str(value) if value else None
                    obj_data[field.name] = value
                
                backup_data[model_name].append(obj_data)
            
            print(f"{model_name}: {len(backup_data[model_name])} objects backed up")
            
        except Exception as e:
            print(f"Error backing up {model_name}: {e}")
    
    backup_file = BASE_DIR / 'sqlite_backup.json'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    print(f"Backup saved to: {backup_file}")
    return backup_file

def test_postgresql_connection():
    """Test PostgreSQL connection"""
    print("Testing PostgreSQL connection...")
    
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"PostgreSQL connection successful: {version[0]}")
        return True
    except Exception as e:
        print(f"PostgreSQL connection error: {e}")
        return False

def migrate_schema():
    """Migrate schema to PostgreSQL"""
    print("Migrating schema to PostgreSQL...")
    
    try:
        call_command('migrate', '--fake-initial')
        call_command('migrate')
        print("Schema migration successful")
        return True
    except Exception as e:
        print(f"Schema migration error: {e}")
        return False

def restore_data_from_backup(backup_file):
    """Restore data from SQLite backup"""
    print("Restoring data from backup...")
    
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        for model_name, objects_data in backup_data.items():
            try:
                model = globals()[model_name]
                print(f"Restoring {model_name}...")
                
                for obj_data in objects_data:
                    if 'id' in obj_data:
                        del obj_data['id']
                    
                    for field_name, value in obj_data.items():
                        if value and isinstance(value, str):
                            if field_name in ['image', 'photo', 'file'] and value.startswith('/'):
                                old_path = BASE_DIR / value.lstrip('/')
                                if old_path.exists():
                                    new_path = settings.MEDIA_ROOT / Path(value).name
                                    new_path.parent.mkdir(parents=True, exist_ok=True)
                                    import shutil
                                    shutil.copy2(old_path, new_path)
                                    obj_data[field_name] = str(new_path.relative_to(settings.MEDIA_ROOT))
                    
                    model.objects.create(**obj_data)
                
                print(f"{model_name}: {len(objects_data)} objects restored")
                
            except Exception as e:
                print(f"Error restoring {model_name}: {e}")
        
        print("Data restoration completed")
        return True
        
    except Exception as e:
        print(f"Data restoration error: {e}")
        return False

def verify_migration():
    """Verify migration was successful"""
    print("Verifying migration...")
    
    try:
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
                print(f"{model_name}: {count} objects")
                total_objects += count
            except Exception as e:
                print(f"Error counting {model_name}: {e}")
        
        print(f"Total: {total_objects} objects migrated")
        return True
        
    except Exception as e:
        print(f"Verification error: {e}")
        return False

def main():
    """Main migration function"""
    print("Starting SQLite to PostgreSQL migration")
    print("=" * 50)
    
    # Step 1: Backup SQLite data
    backup_file = backup_sqlite_data()
    
    # Step 2: Test PostgreSQL connection
    print("\n" + "=" * 50)
    if not test_postgresql_connection():
        print("Cannot connect to PostgreSQL. Stopping migration.")
        return
    
    # Step 3: Migrate schema
    print("\n" + "=" * 50)
    if not migrate_schema():
        print("Cannot migrate schema. Stopping migration.")
        return
    
    # Step 4: Restore data
    print("\n" + "=" * 50)
    if not restore_data_from_backup(backup_file):
        print("Cannot restore data. Stopping migration.")
        return
    
    # Step 5: Verify migration
    print("\n" + "=" * 50)
    verify_migration()
    
    print("\n" + "=" * 50)
    print("Migration completed successfully!")
    print("Next steps:")
    print("1. Test application: python manage.py runserver")
    print("2. Check admin interface")
    print("3. Test API endpoints")
    print("4. Backup sqlite_backup.json file")
    print("5. Remove db.sqlite3 if everything works")

if __name__ == '__main__':
    main()
