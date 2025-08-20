#!/usr/bin/env python
"""
Basic PostgreSQL setup script for SiteMocess
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_postgresql():
    """Setup PostgreSQL database and user"""
    
    # Configuration parameters
    db_name = 'mocess_db'
    db_user = 'mocess_user'
    db_password = '@Basbedo@123'
    db_host = 'localhost'
    db_port = '5432'
    
    print("PostgreSQL Configuration...")
    print(f"   Database: {db_name}")
    print(f"   User: {db_user}")
    print(f"   Host: {db_host}:{db_port}")
    
    try:
        # Connect to PostgreSQL as superuser
        print("Connecting to PostgreSQL...")
        
        # Try different passwords for postgres user
        postgres_passwords = ['postgres', 'admin', 'password', '']
        conn = None
        
        for password in postgres_passwords:
            try:
                conn = psycopg2.connect(
                    host=db_host,
                    port=db_port,
                    user='postgres',
                    password=password
                )
                print(f"Connection successful with password: {'(empty)' if password == '' else password}")
                break
            except psycopg2.OperationalError:
                continue
        
        if conn is None:
            print("Cannot connect to PostgreSQL")
            print("Please check:")
            print("   1. PostgreSQL is installed and running")
            print("   2. PostgreSQL service is started")
            return False
        
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if user exists
        print("Checking user...")
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (db_user,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"Creating user {db_user}...")
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}';")
            print(f"User {db_user} created")
        else:
            print(f"User {db_user} already exists")
        
        # Check if database exists
        print("Checking database...")
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print(f"Creating database {db_name}...")
            cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user};")
            print(f"Database {db_name} created")
        else:
            print(f"Database {db_name} already exists")
        
        # Grant privileges to user
        print("Granting privileges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")
        cursor.execute(f"ALTER DATABASE {db_name} OWNER TO {db_user};")
        print("Privileges granted")
        
        cursor.close()
        conn.close()
        
        # Test connection with new user
        print("Testing connection with new user...")
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
        print(f"Connection successful: {version[0]}")
        
        test_cursor.close()
        test_conn.close()
        
        print("PostgreSQL setup completed successfully!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"Connection error: {e}")
        print("Please check:")
        print("   1. PostgreSQL is installed and running")
        print("   2. PostgreSQL service is started")
        return False
        
    except Exception as e:
        print(f"Error during setup: {e}")
        return False

if __name__ == '__main__':
    setup_postgresql()
