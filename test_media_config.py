#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Test media files serving and configuration
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
print("CHECKING MEDIA FILES CONFIGURATION")
print("=" * 70)

# Check settings
print("\nMEDIA SETTINGS:")
print("-" * 70)
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"DEBUG: {settings.DEBUG}")

# Check if MEDIA_ROOT exists
if os.path.exists(settings.MEDIA_ROOT):
    print(f"\n✓ MEDIA_ROOT exists: {settings.MEDIA_ROOT}")
else:
    print(f"\n✗ MEDIA_ROOT does NOT exist: {settings.MEDIA_ROOT}")

# Check tomatos.jpg
tomatos_path = os.path.join(settings.MEDIA_ROOT, 'products', 'tomatos.jpg')
if os.path.exists(tomatos_path):
    size = os.path.getsize(tomatos_path)
    print(f"✓ tomatos.jpg exists ({size:,} bytes)")
    print(f"  Path: {tomatos_path}")
else:
    print(f"✗ tomatos.jpg NOT found")
    print(f"  Expected at: {tomatos_path}")

# Check URL patterns
print("\nURL PATTERNS:")
print("-" * 70)
resolver = get_resolver()
patterns = resolver.url_patterns

media_pattern_found = False
for pattern in patterns:
    pattern_str = str(pattern)
    if 'media' in pattern_str.lower():
        print(f"✓ Found media pattern: {pattern_str}")
        media_pattern_found = True

if not media_pattern_found:
    print("✗ No media URL pattern found!")

# Check MIDDLEWARE
print("\nMIDDLEWARE:")
print("-" * 70)
for middleware in settings.MIDDLEWARE:
    if 'whitenoise' in middleware.lower():
        print(f"⚠ WhiteNoise detected: {middleware}")
        print("  WhiteNoise may interfere with media serving")

print("\n" + "=" * 70)
print("RECOMMENDATION:")
print("=" * 70)
print("\nIf media pattern not found or WhiteNoise interferes,")
print("we need to adjust the configuration.")
