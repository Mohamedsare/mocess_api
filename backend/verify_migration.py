#!/usr/bin/env python
"""
Script de vérification de la migration vers PostgreSQL
Vérifie que toutes les données ont été correctement migrées
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

from django.db import connections
from django.conf import settings
from api.models import *

def check_database_connection():
    """Vérifie la connexion à la base de données"""
    print("🔍 Vérification de la connexion à la base de données...")
    
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Connexion réussie: {version[0]}")
            
            # Vérifier le type de base de données
            if 'postgresql' in settings.DATABASES['default']['ENGINE']:
                print("✅ Base de données PostgreSQL détectée")
            elif 'sqlite3' in settings.DATABASES['default']['ENGINE']:
                print("⚠️ Base de données SQLite détectée (pas encore migrée)")
            else:
                print("❓ Type de base de données inconnu")
                
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def count_records():
    """Compte les enregistrements dans chaque modèle"""
    print("\n📊 Comptage des enregistrements...")
    
    models_to_check = [
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
    
    total_records = 0
    
    for model_name in models_to_check:
        try:
            model = globals()[model_name]
            count = model.objects.count()
            print(f"📈 {model_name}: {count} enregistrements")
            total_records += count
        except Exception as e:
            print(f"❌ Erreur lors du comptage de {model_name}: {e}")
    
    print(f"\n📊 Total: {total_records} enregistrements")
    return total_records

def check_backup_file():
    """Vérifie le fichier de sauvegarde SQLite"""
    print("\n💾 Vérification du fichier de sauvegarde...")
    
    backup_file = BASE_DIR / 'sqlite_backup.json'
    
    if not backup_file.exists():
        print("❌ Fichier de sauvegarde non trouvé")
        return False
    
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        backup_total = 0
        for model_name, objects_data in backup_data.items():
            print(f"📋 {model_name}: {len(objects_data)} enregistrements dans la sauvegarde")
            backup_total += len(objects_data)
        
        print(f"📋 Total dans la sauvegarde: {backup_total} enregistrements")
        return backup_total
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier de sauvegarde: {e}")
        return False

def check_sample_data():
    """Vérifie quelques exemples de données"""
    print("\n🔍 Vérification d'exemples de données...")
    
    # Vérifier quelques modèles clés
    try:
        # Vérifier les catégories
        categories = Category.objects.all()[:3]
        print(f"📂 Catégories (3 premières): {[c.name for c in categories]}")
        
        # Vérifier les projets
        projects = Project.objects.all()[:3]
        print(f"📁 Projets (3 premiers): {[p.title for p in projects]}")
        
        # Vérifier les membres de l'équipe
        team_members = TeamMember.objects.all()[:3]
        print(f"👥 Membres de l'équipe (3 premiers): {[m.name for m in team_members]}")
        
        # Vérifier les actualités
        news = News.objects.all()[:3]
        print(f"📰 Actualités (3 premières): {[n.title for n in news]}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des exemples: {e}")

def check_file_fields():
    """Vérifie que les fichiers média sont accessibles"""
    print("\n📁 Vérification des fichiers média...")
    
    try:
        # Vérifier les images de projets
        project_images = ProjectImage.objects.all()[:5]
        for img in project_images:
            if img.image:
                if img.image.storage.exists(img.image.name):
                    print(f"✅ Image projet accessible: {img.image.name}")
                else:
                    print(f"❌ Image projet manquante: {img.image.name}")
        
        # Vérifier les photos d'équipe
        team_photos = TeamMember.objects.filter(photo__isnull=False)[:5]
        for member in team_photos:
            if member.photo.storage.exists(member.photo.name):
                print(f"✅ Photo équipe accessible: {member.photo.name}")
            else:
                print(f"❌ Photo équipe manquante: {member.photo.name}")
                
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des fichiers: {e}")

def main():
    """Fonction principale de vérification"""
    print("🔍 Vérification de la migration vers PostgreSQL")
    print("=" * 60)
    
    # Étape 1: Vérifier la connexion
    if not check_database_connection():
        print("❌ Impossible de se connecter à la base de données")
        return
    
    # Étape 2: Compter les enregistrements
    current_total = count_records()
    
    # Étape 3: Vérifier la sauvegarde
    backup_total = check_backup_file()
    
    # Étape 4: Comparer les totaux
    if backup_total and current_total:
        if current_total >= backup_total:
            print(f"\n✅ Migration réussie! {current_total} enregistrements migrés sur {backup_total}")
        else:
            print(f"\n⚠️ Migration partielle: {current_total} enregistrements sur {backup_total}")
    
    # Étape 5: Vérifier les exemples
    check_sample_data()
    
    # Étape 6: Vérifier les fichiers
    check_file_fields()
    
    print("\n" + "=" * 60)
    print("🎉 Vérification terminée!")
    
    if current_total > 0:
        print("✅ Votre migration semble réussie!")
        print("📝 N'oubliez pas de tester manuellement votre application")
    else:
        print("❌ Aucune donnée trouvée. Vérifiez votre migration.")

if __name__ == '__main__':
    main()
