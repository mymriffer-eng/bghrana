#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
sys.path.insert(0, '/home/bghranac/repositories/bghrana')

django.setup()

# Collect static files
from django.core.management import call_command

print("Collecting static files...")
print("=" * 60)

try:
    call_command('collectstatic', '--noinput', verbosity=2)
    print("=" * 60)
    print("✓ Static files collected successfully!")
except Exception as e:
    print("=" * 60)
    print(f"✗ ERROR: {e}")
    sys.exit(1)
