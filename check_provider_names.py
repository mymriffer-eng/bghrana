#!/usr/bin/env python
"""
Проверка за Case Sensitivity и Provider Name формат
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from allauth.socialaccount.models import SocialApp

print("\n" + "="*70)
print("🔍 ПРОВЕРКА ЗА PROVIDER NAME ФОРМАТ")
print("="*70 + "\n")

apps = SocialApp.objects.all()

for app in apps:
    print(f"Provider: '{app.provider}'")
    print(f"  ASCII bytes: {[ord(c) for c in app.provider]}")
    print(f"  Length: {len(app.provider)}")
    print(f"  Lower: '{app.provider.lower()}'")
    print(f"  Expected: 'facebook' or 'google'")
    
    # Провери дали има whitespace или странни символи
    if app.provider != app.provider.strip():
        print(f"  ⚠️  ВНИМАНИЕ: Има whitespace!")
    
    if app.provider.lower() == 'facebook':
        print(f"  ✅ Facebook provider name е OK (lowercase match)")
    elif app.provider == 'facebook':
        print(f"  ✅ Facebook provider name е ТОЧНО 'facebook'")
    elif 'facebook' in app.provider.lower():
        print(f"  ⚠️  Съдържа 'facebook' но НЕ е точно 'facebook'")
    
    print()

print("\n" + "="*70)
print("🔍 ПРОВЕРКА ЗА URL PATTERN TESTING")
print("="*70 + "\n")

# Тествай дали URL-ите съществуват
from django.urls import reverse, NoReverseMatch

try:
    google_url = reverse('google_login')
    print(f"✅ Google URL намерен: {google_url}")
except NoReverseMatch:
    print(f"⚠️  'google_login' URL pattern НЕ съществува")

try:
    fb_url = reverse('facebook_login')
    print(f"✅ Facebook URL намерен: {fb_url}")
except NoReverseMatch:
    print(f"⚠️  'facebook_login' URL pattern НЕ съществува")

# Алтернативен начин
from django.conf import settings
from django.urls import get_resolver

resolver = get_resolver()
url_patterns = list(resolver.url_patterns)

print(f"\n📋 Allauth URL patterns:")
for pattern in url_patterns:
    pattern_str = str(pattern.pattern)
    if 'account' in pattern_str:
        print(f"  {pattern_str}")

print()
