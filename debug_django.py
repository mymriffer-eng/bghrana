#!/usr/bin/env python
import os
import sys

print("=" * 60)
print("DJANGO DEBUG TEST")
print("=" * 60)

# Test 1: Django import
print("\n1. Testing Django import...")
try:
    import django
    print(f"   ✓ Django version: {django.get_version()}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 2: Settings load
print("\n2. Testing settings...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
    sys.path.insert(0, '/home/bghranac/repositories/bghrana')
    django.setup()
    print("   ✓ Django setup complete")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Database connection
print("\n3. Testing database...")
try:
    from django.db import connection
    connection.ensure_connection()
    print("   ✓ Database connection works")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: WSGI application
print("\n4. Testing WSGI application...")
try:
    from products.wsgi import application
    print(f"   ✓ WSGI application loaded: {type(application)}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Check passenger_wsgi.py
print("\n5. Testing passenger_wsgi.py...")
try:
    with open('/home/bghranac/repositories/bghrana/passenger_wsgi.py', 'r') as f:
        content = f.read()
    print("   ✓ passenger_wsgi.py exists")
    print(f"   Content length: {len(content)} bytes")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Environment variables
print("\n6. Environment variables...")
print(f"   DEBUG: {os.environ.get('DEBUG', 'NOT SET')}")
print(f"   DB_NAME: {os.environ.get('DB_NAME', 'NOT SET')}")
print(f"   ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS', 'NOT SET')}")

print("\n" + "=" * 60)
print("If all tests pass, check Passenger error logs")
print("=" * 60)
