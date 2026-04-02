#!/usr/bin/env python3
"""
КРИТИЧЕН ТЕСТ - Какво ТОЧНО връща Facebook Login view-то
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.urls import resolve
from django.contrib.sites.models import Site

print("=" * 70)
print("TEST: FACEBOOK LOGIN VIEW RESPONSE")
print("=" * 70)

# Test 1: Direct view call
print("\n1. DIRECT VIEW CALL (симулация на browser request):")
print("-" * 70)

factory = RequestFactory()
request = factory.get('/accounts/facebook/login/')

# Add session
middleware = SessionMiddleware(lambda x: None)
middleware.process_request(request)
request.session.save()

# Add messages
msg_middleware = MessageMiddleware(lambda x: None)
msg_middleware.process_request(request)

# Add site
request.site = Site.objects.get_current()
request.user = None

try:
    resolved = resolve('/accounts/facebook/login/')
    view_func = resolved.func
    
    print(f"View function: {view_func}")
    print(f"View name: {resolved.view_name}")
    
    # Извикай view-то
    response = view_func(request, **resolved.kwargs)
    
    print(f"\n✅ Response type: {type(response)}")
    print(f"✅ Status code: {response.status_code}")
    
    if hasattr(response, 'url'):
        print(f"✅ Redirect URL: {response.url}")
    elif 'Location' in response:
        location = response['Location']
        print(f"✅ Location header: {location}")
        
        # Parse Location за да видим какъв OAuth provider е
        if 'facebook.com' in location:
            print("   ✅✅✅ КОРЕКТНО: Redirect е към FACEBOOK OAuth!")
        elif 'google.com' in location or 'accounts.google.com' in location:
            print("   ❌❌❌ ГРЕШКА: Redirect е към GOOGLE OAuth (не Facebook)!")
        else:
            print(f"   ⚠️  Неизвестен OAuth provider в URL-а")
    
    print(f"\nПЪЛНИ HEADERS:")
    for key, value in response.items():
        print(f"  {key}: {value}")
        
except Exception as e:
    import traceback
    print(f"❌ ERROR: {e}")
    print(traceback.format_exc())

# Test 2: Google view за сравнение
print("\n\n2. GOOGLE LOGIN VIEW (за сравнение):")
print("-" * 70)

request2 = factory.get('/accounts/google/login/')
middleware.process_request(request2)
request2.session.save()
msg_middleware.process_request(request2)
request2.site = Site.objects.get_current()
request2.user = None

try:
    resolved2 = resolve('/accounts/google/login/')
    view_func2 = resolved2.func
    response2 = view_func2(request2, **resolved2.kwargs)
    
    print(f"Status code: {response2.status_code}")
    
    if hasattr(response2, 'url'):
        print(f"Redirect URL: {response2.url}")
    elif 'Location' in response2:
        location2 = response2['Location']
        print(f"Location header: {location2}")
        
        if 'google.com' in location2 or 'accounts.google.com' in location2:
            print("   ✅ КОРЕКТНО: Google view redirect-ва към Google OAuth")
        elif 'facebook.com' in location2:
            print("   ❌ ГРЕШКА: Google view redirect-ва към Facebook!")

except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 3: Provider adapter check
print("\n\n3. PROVIDER ADAPTER INSPECTION:")
print("-" * 70)

from allauth.socialaccount import providers
from allauth.socialaccount.adapter import get_adapter

adapter = get_adapter()
print(f"Adapter class: {adapter.__class__}")

# Get providers
try:
    google_provider = adapter.get_provider(request, 'google')
    facebook_provider = adapter.get_provider(request, 'facebook')
    
    print(f"\nGoogle Provider:")
    print(f"  Class: {google_provider.__class__}")
    print(f"  ID: {google_provider.id}")
    print(f"  Name: {google_provider.name}")
    
    print(f"\nFacebook Provider:")
    print(f"  Class: {facebook_provider.__class__}")
    print(f"  ID: {facebook_provider.id}")
    print(f"  Name: {facebook_provider.name}")
    
    # Test get_login_url
    print(f"\n4. GET_LOGIN_URL TEST:")
    print("-" * 70)
    
    # Този метод генерира OAuth URL-а
    # Тук може да е проблемът!
    
except Exception as e:
    import traceback
    print(f"❌ Provider adapter error: {e}")
    print(traceback.format_exc())

# Test 4: Check if providers are swapped somehow
print("\n\n5. PROVIDER REGISTRY CHECK:")
print("-" * 70)

registry = providers.registry
print(f"Registry class: {registry.__class__}")
print(f"Loaded providers: {registry.loaded}")

for provider_id in ['google', 'facebook']:
    try:
        provider_class = registry.by_id.get(provider_id)
        print(f"\n{provider_id}:")
        print(f"  Class: {provider_class}")
        print(f"  ID: {provider_class.id if provider_class else 'N/A'}")
        print(f"  Module: {provider_class.__module__ if provider_class else 'N/A'}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 70)
print("TEST ЗАВЪРШЕН")
print("=" * 70)
