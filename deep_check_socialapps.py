#!/usr/bin/env python
"""
Дълбока проверка на SocialApp конфигурацията в базата данни
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings

print("\n" + "="*70)
print("🔍 ДЪЛБОКА ПРОВЕРКА НА FACEBOOK LOGIN КОНФИГУРАЦИЯТА")
print("="*70 + "\n")

# 1. Проверка на SITE_ID
print("1️⃣  SITE_ID в settings.py")
print(f"   SITE_ID = {settings.SITE_ID}")
print()

# 2. Проверка на всички Sites
print("2️⃣  Всички Sites в базата данни:")
all_sites = Site.objects.all()
for site in all_sites:
    marker = "  ← АКТИВЕН" if site.id == settings.SITE_ID else ""
    print(f"   • ID: {site.id}, Domain: {site.domain}, Name: {site.name}{marker}")
print()

# 3. Проверка на всички SocialApps
print("3️⃣  Всички SocialApps в базата данни:")
all_apps = SocialApp.objects.all()
if not all_apps:
    print("   ❌ НЯМА SocialApps в базата!")
else:
    for app in all_apps:
        print(f"\n   📱 Provider: {app.provider}")
        print(f"      Name: {app.name}")
        print(f"      Client ID: {app.client_id[:30]}...")
        print(f"      Secret: {app.secret[:20]}..." if app.secret else "      Secret: (няма)")
        
        sites = app.sites.all()
        if sites:
            print(f"      Sites: {[f'{s.id}:{s.domain}' for s in sites]}")
        else:
            print(f"      ⚠️  Sites: НЯМА СВЪРЗАНИ SITES!")
print()

# 4. Специфична проверка за Facebook
print("4️⃣  Facebook SocialApp проверка:")
try:
    current_site = Site.objects.get(id=settings.SITE_ID)
    print(f"   Текущ site: {current_site.domain} (ID: {current_site.id})")
    
    facebook_apps = SocialApp.objects.filter(provider='facebook')
    print(f"   Брой Facebook apps в базата: {facebook_apps.count()}")
    
    if facebook_apps.count() == 0:
        print("   ❌ НЯМА Facebook SocialApp в базата!")
    elif facebook_apps.count() > 1:
        print("   ⚠️  ВНИМАНИЕ: Има повече от един Facebook app!")
        for i, fb_app in enumerate(facebook_apps, 1):
            sites_for_app = fb_app.sites.all()
            print(f"\n   Facebook App #{i}:")
            print(f"      Client ID: {fb_app.client_id}")
            print(f"      Sites: {[s.domain for s in sites_for_app]}")
            print(f"      Свързан с активния site? {current_site in sites_for_app}")
    else:
        fb_app = facebook_apps.first()
        sites_for_fb = fb_app.sites.all()
        print(f"\n   Facebook App:")
        print(f"      Client ID: {fb_app.client_id}")
        print(f"      Sites: {[s.domain for s in sites_for_fb]}")
        
        if current_site in sites_for_fb:
            print(f"      ✅ СВЪРЗАН с активния site ({current_site.domain})")
        else:
            print(f"      ❌ НЕ Е СВЪРЗАН с активния site ({current_site.domain})")
            print(f"      🔧 ПРОБЛЕМ: Facebook app е свързан с {[s.domain for s in sites_for_fb]}")
            print(f"                  но SITE_ID={settings.SITE_ID} е {current_site.domain}")
            
except Site.DoesNotExist:
    print(f"   ❌ Site с ID {settings.SITE_ID} не съществува!")
print()

# 5. Проверка на Google за сравнение
print("5️⃣  Google SocialApp проверка (за сравнение):")
google_apps = SocialApp.objects.filter(provider='google')
if google_apps.exists():
    google_app = google_apps.first()
    google_sites = google_app.sites.all()
    print(f"   Client ID: {google_app.client_id[:30]}...")
    print(f"   Sites: {[s.domain for s in google_sites]}")
    current_site = Site.objects.get(id=settings.SITE_ID)
    if current_site in google_sites:
        print(f"   ✅ Свързан с активния site")
    else:
        print(f"   ❌ НЕ е свързан с активния site")
else:
    print("   ℹ️  Няма Google app")
print()

# 6. Provider registry check
print("6️⃣  Allauth Provider Registry:")
try:
    from allauth.socialaccount import providers
    registry = providers.registry
    
    print(f"   Registered providers: {list(registry.get_list())}")
    
    # Опит да вземем Facebook provider
    try:
        fb_provider = registry.by_id('facebook')
        print(f"   ✅ Facebook provider е регистриран: {fb_provider}")
    except:
        print(f"   ❌ Facebook provider НЕ Е регистриран в registry!")
        
    # Опит да вземем Google provider
    try:
        google_provider = registry.by_id('google')
        print(f"   ✅ Google provider е регистриран: {google_provider}")
    except:
        print(f"   ❌ Google provider НЕ Е регистриран в registry!")
        
except Exception as e:
    print(f"   ⚠️  Грешка при проверка на registry: {e}")
print()

# 7. INSTALLED_APPS check
print("7️⃣  INSTALLED_APPS проверка:")
fb_in_installed = 'allauth.socialaccount.providers.facebook' in settings.INSTALLED_APPS
google_in_installed = 'allauth.socialaccount.providers.google' in settings.INSTALLED_APPS

print(f"   Facebook provider: {'✅ В INSTALLED_APPS' if fb_in_installed else '❌ НЕ Е в INSTALLED_APPS'}")
print(f"   Google provider: {'✅ В INSTALLED_APPS' if google_in_installed else '❌ НЕ Е в INSTALLED_APPS'}")
print()

print("="*70)
print("📊 ЗАКЛЮЧЕНИЕ:")
print("="*70)

# Проверка за типични проблеми
issues = []

if not fb_in_installed:
    issues.append("❌ Facebook provider липсва от INSTALLED_APPS")

fb_apps = SocialApp.objects.filter(provider='facebook')
if fb_apps.count() == 0:
    issues.append("❌ Няма Facebook SocialApp в базата")
elif fb_apps.count() > 1:
    issues.append("⚠️  Има повече от един Facebook SocialApp")

if fb_apps.exists():
    current_site = Site.objects.get(id=settings.SITE_ID)
    fb_app = fb_apps.first()
    if current_site not in fb_app.sites.all():
        issues.append(f"❌ Facebook app НЕ е свързан с активния site ({current_site.domain})")

if issues:
    print("\n🔴 ОТКРИТИ ПРОБЛЕМИ:")
    for issue in issues:
        print(f"   {issue}")
else:
    print("\n🟢 Всички проверки са ОК в базата данни!")
    print("   Проблемът е в Passenger module cache.")
    print("   Направете FULL RESTART (STOP → START) от cPanel.")

print()
