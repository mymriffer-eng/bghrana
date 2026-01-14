#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Fix Google OAuth SocialApp issue
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
print("FIXING GOOGLE OAUTH SOCIALAPP")
print("=" * 70)

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from decouple import config

try:
    site = Site.objects.get(id=1)
    print(f"\n✓ Found site: {site.domain}")
    
    # Check if Google SocialApp exists
    google_apps = SocialApp.objects.filter(provider='google')
    
    if google_apps.exists():
        print(f"\n✓ Google SocialApp already exists")
        for app in google_apps:
            print(f"  - {app.name}")
    else:
        print(f"\n⚠ Google SocialApp does NOT exist, creating it...")
        
        # Get credentials from environment
        client_id = config('GOOGLE_CLIENT_ID', default='')
        client_secret = config('GOOGLE_CLIENT_SECRET', default='')
        
        if client_id and client_secret:
            # Create SocialApp
            social_app = SocialApp.objects.create(
                provider='google',
                name='Google',
                client_id=client_id,
                secret=client_secret
            )
            social_app.sites.add(site)
            print(f"✓ Created Google SocialApp with credentials")
        else:
            print(f"✗ ERROR: Google credentials not found in environment variables")
            print(f"  GOOGLE_CLIENT_ID: {'Set' if client_id else 'Not set'}")
            print(f"  GOOGLE_CLIENT_SECRET: {'Set' if client_secret else 'Not set'}")
            
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✓ COMPLETE")
print("=" * 70)
print("\nNEXT STEPS:")
print("1. Restart Python App")
print("2. Test login: https://bghrana.com/accounts/login/")
print("3. Test signup: https://bghrana.com/accounts/signup/")
