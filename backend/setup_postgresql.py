#!/usr/bin/env python
"""
Script de configuration PostgreSQL pour SiteMocess
Ce script crée la base de données et l'utilisateur PostgreSQL si ils n'existent pas
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from pathlib import Path
from decouple import config

def setup_postgresql():
    """Configure PostgreSQL avec la base de données et l'utilisateur"""
    
    # Récupérer les paramètres de configuration
    db_name = config('DB_NAME', default='mocess_db')
    db_user = config('DB_USER', default='mocess_user')
    db_password = config('DB_PASSWORD', default='@Basbedo@123')
    db_host = config('DB_HOST', default='localhost')
    db_port = config('DB_PORT', default='5432')
    
    print(f"🔧 Configuration PostgreSQL...")
    print(f"   Base de données: {db_name}")
    print(f"   Utilisateur: {db_user}")
    print(f"   Hôte: {db_host}:{db_port}")
    
    try:
        # Se connecter à PostgreSQL en tant que superutilisateur
        print("📡 Connexion à PostgreSQL...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user='postgres',
            password='postgres'  # Mot de passe par défaut, à adapter si nécessaire
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Vérifier si l'utilisateur existe
        print("👤 Vérification de l'utilisateur...")
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (db_user,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"➕ Création de l'utilisateur {db_user}...")
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}';")
            print(f"✅ Utilisateur {db_user} créé")
        else:
            print(f"✅ Utilisateur {db_user} existe déjà")
        
        # Vérifier si la base de données existe
        print("🗄️ Vérification de la base de données...")
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print(f"➕ Création de la base de données {db_name}...")
            cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user};")
            print(f"✅ Base de données {db_name} créée")
        else:
            print(f"✅ Base de données {db_name} existe déjà")
        
        # Donner les privilèges à l'utilisateur
        print("🔐 Attribution des privilèges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")
        cursor.execute(f"ALTER DATABASE {db_name} OWNER TO {db_user};")
        print("✅ Privilèges attribués")
        
        cursor.close()
        conn.close()
        
        # Tester la connexion avec le nouvel utilisateur
        print("🧪 Test de connexion avec le nouvel utilisateur...")
        test_conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        test_cursor = test_conn.cursor()
        test_cursor.execute("SELECT version();")
        version = test_cursor.fetchone()
        print(f"✅ Connexion réussie: {version[0]}")
        
        test_cursor.close()
        test_conn.close()
        
        print("🎉 Configuration PostgreSQL terminée avec succès!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Erreur de connexion: {e}")
        print("💡 Assurez-vous que:")
        print("   1. PostgreSQL est installé et en cours d'exécution")
        print("   2. Le mot de passe de l'utilisateur 'postgres' est correct")
        print("   3. Le service PostgreSQL est démarré")
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return False

if __name__ == '__main__':
    setup_postgresql()
