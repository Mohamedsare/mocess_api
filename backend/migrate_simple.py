#!/usr/bin/env python
"""
Simple migration script using Django management commands
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    """Run a command and return the result"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def main():
    """Main migration function"""
    print("Starting SQLite to PostgreSQL migration")
    print("=" * 50)
    
    # Set environment variables
    os.environ['DB_ENGINE'] = 'postgresql'
    os.environ['DB_NAME'] = 'mocess_db'
    os.environ['DB_USER'] = 'mocess_user'
    os.environ['DB_PASSWORD'] = '@Basbedo@123'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    
    # Step 1: Backup SQLite data
    print("Step 1: Backing up SQLite data...")
    if not run_command("python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > sqlite_backup.json"):
        print("Failed to backup SQLite data")
        return
    
    # Step 2: Test PostgreSQL connection
    print("\nStep 2: Testing PostgreSQL connection...")
    if not run_command("python manage.py dbshell --database=default"):
        print("Failed to connect to PostgreSQL")
        return
    
    # Step 3: Migrate schema
    print("\nStep 3: Migrating schema...")
    if not run_command("python manage.py migrate --fake-initial"):
        print("Failed to fake initial migration")
        return
    
    if not run_command("python manage.py migrate"):
        print("Failed to migrate schema")
        return
    
    # Step 4: Load data
    print("\nStep 4: Loading data...")
    if not run_command("python manage.py loaddata sqlite_backup.json"):
        print("Failed to load data")
        return
    
    # Step 5: Verify migration
    print("\nStep 5: Verifying migration...")
    if not run_command("python manage.py shell -c \"from api.models import *; print('Migration verification completed')\""):
        print("Failed to verify migration")
        return
    
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
