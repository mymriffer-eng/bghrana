#!/usr/bin/env python
"""
Проверка на Sites и Social Applications конфигурация в database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

print("=" * 70)
print("ПРОВЕРКА НА SITES И SOCIAL APPLICATIONS")
print("=" * 70)

# 1. Проверка на SITE_ID в settings
print(f"\n1. SITE_ID в settings.py: {settings.SITE_ID}")

# 2. Всички Sites в database
print("\n2. Всички Sites в database:")
print("-" * 70)
for site in Site.objects.all():
    marker = " <-- ACTIVE (SITE_ID)" if site.id == settings.SITE_ID else ""
    print(f"   ID: {site.id}, Domain: {site.domain}, Name: {site.name}{marker}")

# 3. Проверка дали има bghrana.com
try:
    bghrana_site = Site.objects.get(domain='bghrana.com')
    print(f"\n✓ bghrana.com намерен с ID: {bghrana_site.id}")
    if bghrana_site.id != settings.SITE_ID:
        print(f"⚠️  ПРОБЛЕМ: bghrana.com има ID {bghrana_site.id}, но SITE_ID в settings.py е {settings.SITE_ID}!")
        print(f"   РЕШЕНИЕ: Промени SITE_ID = {bghrana_site.id} в products/settings.py")
except Site.DoesNotExist:
    print("\n✗ bghrana.com НЕ е намерен в Sites!")
    print("   РЕШЕНИЕ: Промени example.com на bghrana.com в Django Admin → Sites")

# 4. Всички Social Applications
print("\n3. Всички Social Applications:")
print("-" * 70)
for app in SocialApp.objects.all():
    print(f"\n   Provider: {app.provider}")
    print(f"   Name: {app.name}")
    print(f"   Client ID: {app.client_id}")
    print(f"   Sites: {', '.join([str(s.domain) for s in app.sites.all()])}")
    
    # Проверка дали Site с SITE_ID е включен
    site_ids = [s.id for s in app.sites.all()]
    if settings.SITE_ID in site_ids:
        print(f"   ✓ Site ID {settings.SITE_ID} е включен")
    else:
        print(f"   ✗ Site ID {settings.SITE_ID} НЕ е включен!")
        print(f"   РЕШЕНИЕ: Добави site към {app.provider} Social Application")

# 5. Финална диагноза
print("\n" + "=" * 70)
print("ДИАГНОЗА:")
print("=" * 70)

try:
    current_site = Site.objects.get(id=settings.SITE_ID)
    print(f"Текущ активен Site (ID {settings.SITE_ID}): {current_site.domain}")
    
    # Проверка за Facebook app
    try:
        fb_app = SocialApp.objects.get(provider='facebook')
        if current_site in fb_app.sites.all():
            print(f"✓ Facebook app е правилно конфигуриран за {current_site.domain}")
        else:
            print(f"✗ Facebook app НЕ е свързан с активния site {current_site.domain}")
            print(f"  Facebook app е свързан с: {', '.join([s.domain for s in fb_app.sites.all()])}")
            print(f"\n  РЕШЕНИЕ 1: Ако {current_site.domain} е 'example.com' - промени го на 'bghrana.com'")
            print(f"  РЕШЕНИЕ 2: Добави {current_site.domain} към Facebook Social Application")
    except SocialApp.DoesNotExist:
        print("✗ Facebook Social Application НЕ СЪЩЕСТВУВА!")
        
except Site.DoesNotExist:
    print(f"✗ Site с ID {settings.SITE_ID} не съществува!")

print("=" * 70)
