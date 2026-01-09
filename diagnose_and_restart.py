#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Force restart and diagnose media files issue
"""

import os
import sys
import django

# Setup Django
repo_path = '/home/bghranac/repositories/bghrana'
sys.path.insert(0, repo_path)
os.chdir(repo_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.conf import settings
from django.urls import get_resolver

print("=" * 70)
print("DIAGNOSING MEDIA FILES ISSUE")
print("=" * 70)

# Check settings
print("\nSETTINGS:")
print(f"  DEBUG: {settings.DEBUG}")
print(f"  MEDIA_URL: {settings.MEDIA_URL}")
print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")

# Check if file exists
tomatos_path = os.path.join(settings.MEDIA_ROOT, 'products', 'tomatos.jpg')
print(f"\nFILE CHECK:")
print(f"  Path: {tomatos_path}")
print(f"  Exists: {os.path.exists(tomatos_path)}")
if os.path.exists(tomatos_path):
    print(f"  Size: {os.path.getsize(tomatos_path):,} bytes")

# Check URL patterns
print(f"\nURL PATTERNS:")
resolver = get_resolver()
for pattern in resolver.url_patterns:
    pattern_str = str(pattern)
    if 'static' in pattern_str.lower():
        print(f"  {pattern_str}")

# Force restart by touching tmp/restart.txt
print(f"\nFORCING PASSENGER RESTART:")
tmp_dir = os.path.join(repo_path, 'tmp')
restart_file = os.path.join(tmp_dir, 'restart.txt')

os.makedirs(tmp_dir, exist_ok=True)

try:
    # Touch the file to trigger restart
    with open(restart_file, 'a'):
        os.utime(restart_file, None)
    print(f"✓ Touched: {restart_file}")
except Exception as e:
    print(f"✗ ERROR: {e}")

print("\n" + "=" * 70)
print("TEST URLS:")
print("=" * 70)
print("\n1. Direct file test: https://bghrana.com/media/products/tomatos.jpg")
print("2. Main page: https://bghrana.com")
print("\nWait 10-15 seconds for Passenger to restart, then test.")
