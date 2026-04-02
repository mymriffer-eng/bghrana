#!/usr/bin/env python
"""
REAL WEB REQUEST симулация към Facebook endpoint
Ще покаже КАКЪВ TEMPLATE реално се използва
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/bghranac/public_html')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser
import re

print("=" * 70)
print("REAL WEB REQUEST SIMULATION - Facebook Login")
print("=" * 70)

# 1. Направо прави HTTP GET request като браузър
print("\n1. HTTP GET REQUEST към /accounts/facebook/login/:")
client = Client()

try:
    response = client.get('/accounts/facebook/login/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        # Вземаме HTML съдържанието
        content = response.content.decode('utf-8')
        
        # Търсим заглавието
        title_match = re.search(r'<title>(.*?)</title>', content)
        if title_match:
            print(f"   <title>: {title_match.group(1)}")
        
        # Търсим h2 заглавие
        h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', content)
        if h2_match:
            h2_text = re.sub(r'<[^>]+>', '', h2_match.group(1))  # Премахваме HTML tags
            print(f"   <h2>: {h2_text.strip()}")
        
        # Проверка дали е Facebook или Google
        if 'Facebook' in content and 'Вход с Facebook' in content:
            print("   ✅ СЪДЪРЖА: 'Вход с Facebook'")
        elif 'Google' in content and 'Вход с Google' in content:
            print("   ❌ СЪДЪРЖА: 'Вход с Google' (ГРЕШЕН TEMPLATE!)")
        
        # Проверка за OAuth redirect URL
        oauth_match = re.search(r'https://www\.(facebook|google)\.com', content)
        if oauth_match:
            print(f"   OAuth Provider: {oauth_match.group(1)}")
            
    elif response.status_code == 302:
        print(f"   Redirect to: {response.url}")
        
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# 2. Проверка на view resolution
print("\n2. VIEW RESOLUTION:")
from django.urls import resolve

try:
    facebook_url = '/accounts/facebook/login/'
    resolved = resolve(facebook_url)
    print(f"   URL: {facebook_url}")
    print(f"   View: {resolved.func}")
    print(f"   View name: {resolved.view_name}")
    print(f"   URL name: {resolved.url_name}")
    print(f"   Kwargs: {resolved.kwargs}")
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# 3. Проверка какъв template django-allauth използва
print("\n3. DJANGO-ALLAUTH TEMPLATE LOOKUP:")

try:
    from allauth.socialaccount import providers
    
    # Вземаме Facebook provider
    facebook_provider = providers.registry.by_id('facebook')
    print(f"   Facebook Provider: {facebook_provider}")
    print(f"   Provider ID: {facebook_provider.id if facebook_provider else 'N/A'}")
    print(f"   Provider Name: {facebook_provider.name if facebook_provider else 'N/A'}")
    
    # Проверка на template пътищата които allauth би използвал
    if facebook_provider:
        # Allauth използва тази логика за template selection:
        # 1. socialaccount/{provider.id}/login.html
        # 2. socialaccount/login.html (fallback)
        
        template_name = f"socialaccount/{facebook_provider.id}/login.html"
        print(f"   Expected template: {template_name}")
        
        # Проверка дали template съществува
        from django.template.loader import get_template
        try:
            template = get_template(template_name)
            print(f"   ✅ Template found: {template.origin.name if hasattr(template, 'origin') else 'unknown'}")
            
            # Проверка на съдържанието
            if hasattr(template, 'template') and hasattr(template.template, 'source'):
                content = template.template.source
                if 'Facebook' in content:
                    print(f"   ✅ Template contains 'Facebook'")
                elif 'Google' in content:
                    print(f"   ❌ Template contains 'Google' (WRONG!)")
                    
        except Exception as e:
            print(f"   ❌ Template not found: {e}")
            
except Exception as e:
    print(f"   ⚠️ Error checking allauth: {e}")

# 4. Template cache status
print("\n4. TEMPLATE CACHE STATUS:")
from django.template import engines

engine = engines['django']
if hasattr(engine, 'engine'):
    loaders = engine.engine.template_loaders
    print(f"   Loaders: {loaders}")
    
    # Проверка дали има cached loader
    for loader in loaders:
        loader_type = type(loader).__name__
        print(f"   - {loader_type}")
        
        if 'Cached' in loader_type or 'cached' in loader_type:
            print(f"     ⚠️ CACHED LOADER DETECTED!")
            if hasattr(loader, 'get_template_cache'):
                cache = loader.get_template_cache()
                print(f"     Cache size: {len(cache)} templates")
                
                # Показваме cache keys
                if cache:
                    print(f"     Cached templates:")
                    for key in list(cache.keys())[:10]:  # Показваме първите 10
                        print(f"       - {key}")

print("\n" + "=" * 70)
print("ДИАГНОЗА:")
print("=" * 70)

# Финална диагноза
if response.status_code == 200:
    content = response.content.decode('utf-8')
    if 'Вход с Google' in content:
        print("❌ ПРОБЛЕМ ПОТВЪРДЕН:")
        print("   /accounts/facebook/login/ показва Google template")
        print("\n   ВЪЗМОЖНИ ПРИЧИНИ:")
        print("   1. Template cache все още активен (въпреки STOP/START)")
        print("   2. django-allauth view НЕ подава provider в context")
        print("   3. Има hardcoded fallback към socialaccount/login.html")
        print("\n   СЛЕДВАЩИ СТЪПКИ:")
        print("   → Проверка на django-allauth view source code")
        print("   → Disable template caching в settings.py")
    elif 'Вход с Facebook' in content:
        print("✅ РАБОТИ! Facebook template се показва коректно!")

print("=" * 70)
