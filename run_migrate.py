#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
sys.path.insert(0, '/home/bghranac/repositories/bghrana')

django.setup()

# Run migrations
from django.core.management import call_command

print("Starting database migrations...")
print("=" * 60)

try:
    call_command('migrate', verbosity=2)
    print("=" * 60)
    print("✓ Migrations completed successfully!")
except Exception as e:
    print("=" * 60)
    print(f"✗ ERROR: {e}")
    sys.exit(1)
