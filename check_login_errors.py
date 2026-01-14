#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Check Django logs and test login page
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

print("=" * 70)
print("CHECKING DJANGO CONFIGURATION FOR LOGIN/REGISTER")
print("=" * 70)

# Check email backend
from django.conf import settings

print("\nEMAIL SETTINGS:")
print("-" * 70)
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")

# Check allauth settings
print("\nALLAUTH SETTINGS:")
print("-" * 70)
print(f"ACCOUNT_EMAIL_VERIFICATION: {settings.ACCOUNT_EMAIL_VERIFICATION}")
print(f"ACCOUNT_EMAIL_REQUIRED: {settings.ACCOUNT_EMAIL_REQUIRED}")

# Check installed apps
print("\nINSTALLED APPS (relevant):")
print("-" * 70)
for app in settings.INSTALLED_APPS:
    if 'allauth' in app or 'account' in app or 'social' in app:
        print(f"  - {app}")

# Check SITE_ID
print(f"\nSITE_ID: {settings.SITE_ID}")

# Check if sites exist in database
print("\nCHECKING DATABASE SITES:")
print("-" * 70)
try:
    from django.contrib.sites.models import Site
    sites = Site.objects.all()
    print(f"Found {sites.count()} site(s):")
    for site in sites:
        print(f"  ID {site.id}: {site.domain} - {site.name}")
except Exception as e:
    print(f"✗ ERROR checking sites: {e}")

# Try to reverse URLs
print("\nCHECKING URL PATTERNS:")
print("-" * 70)
try:
    from django.urls import reverse
    urls_to_check = [
        ('account_login', 'Login'),
        ('account_signup', 'Signup'),
        ('account_logout', 'Logout'),
    ]
    
    for url_name, desc in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"✓ {desc}: {url}")
        except Exception as e:
            print(f"✗ {desc}: ERROR - {e}")
except Exception as e:
    print(f"✗ ERROR reversing URLs: {e}")

print("\n" + "=" * 70)
print("RECOMMENDATION:")
print("=" * 70)
print("\nIf SITE_ID=1 doesn't exist in database, the issue is likely here.")
print("We need to create the Site or change email verification settings.")
