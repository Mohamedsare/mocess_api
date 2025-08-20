#!/usr/bin/env python
"""
Script simple pour migrer les données de SQLite vers PostgreSQL
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, env_vars=None):
    """Exécuter une commande avec des variables d'environnement"""
    print(f"🔄 Exécution: {command}")
    
    my_env = os.environ.copy()
    if env_vars:
        my_env.update(env_vars)
    
    result = subprocess.run(command, shell=True, env=my_env, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Erreur: {result.stderr}")
        return False
    print(f"✅ Succès: {result.stdout}")
    return True

def main():
    """Fonction principale"""
    print("🚀 Migration simple des données SQLite vers PostgreSQL")
    print("=" * 60)
    
    # Étape 1: Sauvegarder les données SQLite
    print("\n📋 Étape 1: Sauvegarde des données SQLite")
    print("-" * 40)
    
    sqlite_env = {
        'DB_ENGINE': 'sqlite3'
    }
    
    if not run_command("python manage.py dumpdata api --indent 2 > api_data.json", sqlite_env):
        print("❌ Échec de la sauvegarde des données SQLite")
        return
    
    # Vérifier si le fichier de sauvegarde contient des données
    backup_file = Path("api_data.json")
    if not backup_file.exists() or backup_file.stat().st_size == 0:
        print("⚠️ Aucune donnée trouvée dans SQLite. Migration terminée.")
        return
    
    print(f"✅ Sauvegarde créée: {backup_file} ({backup_file.stat().st_size} bytes)")
    
    # Étape 2: Restaurer vers PostgreSQL
    print("\n📋 Étape 2: Restauration vers PostgreSQL")
    print("-" * 40)
    
    postgresql_env = {
        'DB_ENGINE': 'postgresql',
        'DB_NAME': 'mocess_db',
        'DB_USER': 'mocess_user',
        'DB_PASSWORD': '@Basbedo@123',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432'
    }
    
    if not run_command("python manage.py loaddata api_data.json", postgresql_env):
        print("❌ Échec de la restauration vers PostgreSQL")
        return
    
    print("\n" + "=" * 60)
    print("🎉 MIGRATION DES DONNÉES TERMINÉE AVEC SUCCÈS!")
    print("✅ Toutes les données ont été migrées de SQLite vers PostgreSQL")
    print("\n📋 Prochaines étapes:")
    print("1. Tester l'application: python test_final.py")
    print("2. Démarrer le serveur: python manage.py runserver")
    print("3. Vérifier les données dans l'admin Django")
    print("4. Supprimer db.sqlite3 si tout fonctionne")

if __name__ == '__main__':
    main()
