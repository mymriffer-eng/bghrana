#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Fix common allauth/login issues
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
print("FIXING LOGIN/REGISTER ISSUES")
print("=" * 70)

# Fix 1: Create or update Site
print("\n1. Checking/Creating Site...")
try:
    from django.contrib.sites.models import Site
    
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': 'bghrana.com',
            'name': 'БГ Храна'
        }
    )
    
    if created:
        print(f"✓ Created new site: {site.domain}")
    else:
        # Update existing site
        if site.domain != 'bghrana.com':
            site.domain = 'bghrana.com'
            site.name = 'БГ Храна'
            site.save()
            print(f"✓ Updated site to: {site.domain}")
        else:
            print(f"✓ Site already correct: {site.domain}")
            
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Fix 2: Test email backend
print("\n2. Testing email backend...")
try:
    from django.conf import settings
    from django.core.mail import EmailMessage
    
    print(f"  Backend: {settings.EMAIL_BACKEND}")
    
    if 'console' in settings.EMAIL_BACKEND.lower():
        print("  ✓ Using console backend (emails print to console)")
    elif 'filebased' in settings.EMAIL_BACKEND.lower():
        print("  ✓ Using file-based backend (emails saved to files)")
    else:
        print(f"  ⚠ Using SMTP backend - may cause delays")
        
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("\n" + "=" * 70)
print("✓ FIXES APPLIED")
print("=" * 70)
print("\nNEXT STEPS:")
print("1. Restart Python App")
print("2. Test login page: https://bghrana.com/accounts/login/")
print("3. Test register page: https://bghrana.com/accounts/signup/")
