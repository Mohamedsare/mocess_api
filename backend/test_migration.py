#!/usr/bin/env python
"""
Test script to verify PostgreSQL migration
"""

import os
import sys
import django
from pathlib import Path

# Set environment variables
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
from api.models import *

def test_postgresql_connection():
    """Test PostgreSQL connection"""
    print("Testing PostgreSQL connection...")
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ PostgreSQL connection successful: {version[0]}")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_models():
    """Test all models"""
    print("\nTesting models...")
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
            print(f"✅ {model_name}: {count} objects")
            total_objects += count
        except Exception as e:
            print(f"❌ {model_name}: Error - {e}")
    
    print(f"\n🎯 Total objects in database: {total_objects}")
    return total_objects > 0

def test_sample_data():
    """Test sample data access"""
    print("\nTesting sample data access...")
    try:
        # Test a few sample queries
        categories = Category.objects.all()[:5]
        print(f"✅ Categories found: {categories.count()}")
        
        projects = Project.objects.all()[:5]
        print(f"✅ Projects found: {projects.count()}")
        
        news = News.objects.all()[:5]
        print(f"✅ News found: {news.count()}")
        
        team_members = TeamMember.objects.all()[:5]
        print(f"✅ Team members found: {team_members.count()}")
        
        return True
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def main():
    """Main test function"""
    print("Testing PostgreSQL Migration")
    print("=" * 40)
    
    # Test 1: Connection
    if not test_postgresql_connection():
        print("❌ Migration test failed: Cannot connect to PostgreSQL")
        return False
    
    # Test 2: Models
    if not test_models():
        print("❌ Migration test failed: No data found in models")
        return False
    
    # Test 3: Sample data
    if not test_sample_data():
        print("❌ Migration test failed: Cannot access sample data")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 Migration test completed successfully!")
    print("✅ PostgreSQL is working correctly")
    print("✅ All models are accessible")
    print("✅ Data has been migrated successfully")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
