#!/usr/bin/env python
"""
Дебъг на 400 Bad Request грешката
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/bghranac/public_html')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.urls import resolve
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

print("=" * 70)
print("DEBUG 400 BAD REQUEST")
print("=" * 70)

# 1. Проверка на settings
print("\n1. DJANGO SETTINGS:")
from django.conf import settings

print(f"   DEBUG: {settings.DEBUG}")
print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"   SITE_ID: {settings.SITE_ID}")
print(f"   SECRET_KEY: {'SET' if settings.SECRET_KEY else 'MISSING'}")

# 2. Проверка на Site
print("\n2. SITE CONFIGURATION:")
from django.contrib.sites.models import Site

try:
    current_site = Site.objects.get(id=settings.SITE_ID)
    print(f"   ✅ Site ID {settings.SITE_ID}: {current_site.domain}")
except Exception as e:
    print(f"   ❌ Error getting site: {e}")

# 3. Проверка на URL resolution
print("\n3. URL RESOLUTION:")
try:
    resolved = resolve('/accounts/facebook/login/')
    print(f"   ✅ URL resolves to: {resolved.func}")
    print(f"   View name: {resolved.view_name}")
    print(f"   URL name: {resolved.url_name}")
except Exception as e:
    print(f"   ❌ Error resolving URL: {e}")

# 4. Проверка на Provider registry
print("\n4. PROVIDER REGISTRY:")
from allauth.socialaccount import providers

try:
    registry = providers.registry
    print(f"   Registry: {registry}")
    
    # List all providers
    provider_list = list(registry.get_class_list())
    print(f"   Available providers: {[p.id for p in provider_list]}")
    
    # Get Facebook specifically
    fb_provider_class = registry.get_class('facebook')
    print(f"   ✅ Facebook provider class: {fb_provider_class}")
    
except Exception as e:
    print(f"   ❌ Error with provider registry: {e}")
    import traceback
    traceback.print_exc()

# 5. Direct view call
print("\n5. DIRECT VIEW CALL:")
from django.test import RequestFactory

try:
    factory = RequestFactory()
    request = factory.get('/accounts/facebook/login/', HTTP_HOST='bghrana.com')
    
    # Add session
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    # Add messages
    msg_middleware = MessageMiddleware(lambda x: None)
    msg_middleware.process_request(request)
    
    # Get the view
    from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
    
    print(f"   Request: {request}")
    print(f"   HTTP_HOST: {request.META.get('HTTP_HOST')}")
    
    # Try to call the view
    resolved = resolve('/accounts/facebook/login/')
    view_func = resolved.func
    
    print(f"   Calling view: {view_func}")
    
    try:
        response = view_func(request)
        print(f"   ✅ Response status: {response.status_code}")
        
        if response.status_code == 400:
            print(f"   ❌ View returns 400!")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                print(f"   Response content: {content[:500]}")
        elif response.status_code == 302:
            print(f"   ✅ Redirect to: {response.url}")
            
    except Exception as e:
        print(f"   ❌ Exception calling view: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"   ❌ Error in direct view call: {e}")
    import traceback
    traceback.print_exc()

# 6. Проверка на SOCIALACCOUNT_PROVIDERS setting
print("\n6. SOCIALACCOUNT_PROVIDERS SETTING:")
if hasattr(settings, 'SOCIALACCOUNT_PROVIDERS'):
    print(f"   ✅ SOCIALACCOUNT_PROVIDERS: {settings.SOCIALACCOUNT_PROVIDERS}")
else:
    print(f"   ⚠️ SOCIALACCOUNT_PROVIDERS не е настроен")

# 7. Проверка на INSTALLED_APPS
print("\n7. INSTALLED_APPS:")
required_apps = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.sites',
]

for app in required_apps:
    if app in settings.INSTALLED_APPS:
        print(f"   ✅ {app}")
    else:
        print(f"   ❌ MISSING: {app}")

print("\n" + "=" * 70)
print("ЗАКЛЮЧЕНИЕ:")
print("=" * 70)

print("\nАко view-то връща 400 при всички request-и,")
print("проблемът е някоя от тези причини:")
print("1. ALLOWED_HOSTS не включва bghrana.com")
print("2. Provider не е правилно регистриран")  
print("3. Site framework конфигурация")
print("4. django-allauth middleware липсва")
print("=" * 70)
