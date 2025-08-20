#!/usr/bin/env python
"""
Script de restauration des données depuis la sauvegarde JSON vers SQLite
Utilisé en cas de rollback de PostgreSQL vers SQLite
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
from django.conf import settings
from api.models import *

def restore_data_from_json(backup_file):
    """Restaure les données depuis le fichier JSON de sauvegarde"""
    print("📥 Restauration des données depuis la sauvegarde...")
    
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        for model_name, objects_data in backup_data.items():
            try:
                model = globals()[model_name]
                print(f"🔄 Restauration de {model_name}...")
                
                # Supprimer les objets existants
                model.objects.all().delete()
                
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
    """Fonction principale de restauration"""
    print("🔄 Début de la restauration depuis la sauvegarde")
    print("=" * 50)
    
    # Chercher le fichier de sauvegarde
    backup_file = BASE_DIR / 'sqlite_backup.json'
    
    if not backup_file.exists():
        print(f"❌ Fichier de sauvegarde non trouvé: {backup_file}")
        print("Assurez-vous d'avoir exécuté le script de migration d'abord.")
        return
    
    # Vérifier que nous sommes en mode SQLite
    if 'sqlite3' not in settings.DATABASES['default']['ENGINE']:
        print("❌ La base de données n'est pas configurée pour SQLite")
        print("Modifiez votre fichier .env pour utiliser DB_ENGINE=sqlite3")
        return
    
    # Restaurer les données
    if restore_data_from_json(backup_file):
        print("=" * 50)
        print("🎉 Restauration terminée avec succès!")
        print("📝 Vérifiez que toutes les données sont correctement restaurées")
    else:
        print("❌ Échec de la restauration")

if __name__ == '__main__':
    main()
