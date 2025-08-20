#!/usr/bin/env python
"""
Final test script for PostgreSQL migration
"""

import os
import sys
import django
from pathlib import Path

# Set environment variables for PostgreSQL
os.environ['DB_ENGINE'] = 'postgresql'
os.environ['DB_NAME'] = 'mocess_db'
os.environ['DB_USER'] = 'mocess_user'
os.environ['DB_PASSWORD'] = '@Basbedo@123'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5432'

# Django setup
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocess_backend.settings')

django.setup()

from django.db import connections
from django.core.management import call_command
from api.models import *

def test_postgresql_connection():
    """Test PostgreSQL connection"""
    print("🔍 Testing PostgreSQL connection...")
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ PostgreSQL connection successful: {version[0]}")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_django_models():
    """Test Django models"""
    print("\n🔍 Testing Django models...")
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
    
    all_models_work = True
    for model_name in models:
        try:
            model = globals()[model_name]
            count = model.objects.count()
            print(f"✅ {model_name}: {count} objects")
        except Exception as e:
            print(f"❌ {model_name}: Error - {e}")
            all_models_work = False
    
    return all_models_work

def test_django_commands():
    """Test Django management commands"""
    print("\n🔍 Testing Django management commands...")
    try:
        # Test check command
        call_command('check')
        print("✅ Django check command successful")
        
        # Test showmigrations
        call_command('showmigrations')
        print("✅ Django showmigrations command successful")
        
        return True
    except Exception as e:
        print(f"❌ Django commands failed: {e}")
        return False

def create_test_data():
    """Create some test data"""
    print("\n🔍 Creating test data...")
    try:
        # Create a test category
        category, created = Category.objects.get_or_create(
            name="Test Category",
            defaults={'description': 'Test category for migration verification'}
        )
        if created:
            print("✅ Test category created")
        else:
            print("✅ Test category already exists")
        
        # Create a test project
        project, created = Project.objects.get_or_create(
            title="Test Project",
            defaults={
                'description': 'Test project for migration verification',
                'category': category
            }
        )
        if created:
            print("✅ Test project created")
        else:
            print("✅ Test project already exists")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create test data: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Final PostgreSQL Migration Test")
    print("=" * 50)
    
    # Test 1: PostgreSQL connection
    if not test_postgresql_connection():
        print("\n❌ Migration test failed: Cannot connect to PostgreSQL")
        return False
    
    # Test 2: Django models
    if not test_django_models():
        print("\n❌ Migration test failed: Django models not working")
        return False
    
    # Test 3: Django commands
    if not test_django_commands():
        print("\n❌ Migration test failed: Django commands not working")
        return False
    
    # Test 4: Create test data
    if not create_test_data():
        print("\n❌ Migration test failed: Cannot create test data")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 MIGRATION COMPLETED SUCCESSFULLY!")
    print("✅ PostgreSQL is working correctly")
    print("✅ Django is configured for PostgreSQL")
    print("✅ All models are accessible")
    print("✅ Test data can be created")
    print("\n📋 Next steps:")
    print("1. Start the server: python manage.py runserver")
    print("2. Access admin: http://localhost:8000/admin/")
    print("3. Access API: http://localhost:8000/api/")
    print("4. Add your data through the admin interface")
    print("5. Remove db.sqlite3 file (optional)")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
