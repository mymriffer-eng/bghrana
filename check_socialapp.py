#!/usr/bin/env python
"""
Проверка дали Facebook SocialApp е регистриран в Django Admin
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/bghranac/public_html')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=" * 70)
print("SOCIALAPP VERIFICATION")
print("=" * 70)

# 1. Проверка на Sites
print("\n1. SITES:")
sites = Site.objects.all()
for site in sites:
    print(f"   ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

# 2. Проверка на SocialApp записи
print("\n2. SOCIALAPP RECORDS:")
apps = SocialApp.objects.all()

if not apps:
    print("   ❌ НЯМА НИТО ЕДИН SocialApp!")
    print("   ⚠️ ТОВА Е ПРОБЛЕМЪТ - няма регистрирани OAuth providers в Admin")
else:
    for app in apps:
        print(f"\n   Provider: {app.provider}")
        print(f"   Name: {app.name}")
        print(f"   Client ID: {app.client_id[:20]}..." if len(app.client_id) > 20 else f"   Client ID: {app.client_id}")
        print(f"   Secret: {'***' if app.secret else 'ПРАЗЕН'}")
        print(f"   Sites: {[s.domain for s in app.sites.all()]}")
        
        if app.provider == 'facebook':
            print("   ✅ Facebook е регистриран")
        elif app.provider == 'google':
            print("   ✅ Google е регистриран")

# 3. Проверка дали Facebook е наличен като provider
print("\n3. AVAILABLE PROVIDERS:")
from allauth.socialaccount import providers

provider_registry = providers.registry.get_list()
print(f"   Registry: {provider_registry}")

for provider in provider_registry:
    print(f"   - {provider.id}: {provider.name}")

# 4. Проверка на SITE_ID
print("\n4. SITE_ID SETTING:")
from django.conf import settings
print(f"   SITE_ID = {settings.SITE_ID}")

# 5. Диагноза
print("\n" + "=" * 70)
print("ДИАГНОЗА:")
print("=" * 70)

facebook_app = SocialApp.objects.filter(provider='facebook').first()
google_app = SocialApp.objects.filter(provider='google').first()

if not facebook_app:
    print("❌ ПРОБЛЕМ: Няма Facebook SocialApp в Admin!")
    print("   ➡️ Allauth НЕ знае Facebook credentials")
    print("   ➡️ Може да fallback-ва към Google")
    print("\n   FIX: Отиди в Django Admin:")
    print("   /admin/socialaccount/socialapp/add/")
    print("   Provider: Facebook")
    print("   Client ID: <от Facebook Developers>")
    print("   Secret key: <от Facebook Developers>")
    print("   Sites: избери bghrana.com")
else:
    print("✅ Facebook SocialApp е регистриран")
    # Проверка на sites
    fb_sites = facebook_app.sites.all()
    if not fb_sites:
        print("   ⚠️ ПРОБЛЕМ: Facebook app НЯМА site!")
        print("   ➡️ Добави bghrana.com към Facebook app в Admin")
    else:
        print(f"   ✅ Facebook app има sites: {[s.domain for s in fb_sites]}")

if google_app:
    print("\n✅ Google SocialApp е регистриран")
else:
    print("\n⚠️ Google SocialApp НЕ е регистриран")

print("=" * 70)
