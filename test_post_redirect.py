#!/usr/bin/env python3
"""
TEST: POST request към Facebook login - къде redirect-ва?
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
from django.middleware.csrf import CsrfViewMiddleware
from django.urls import resolve
from django.contrib.sites.models import Site

print("=" * 80)
print("POST REQUEST TEST - Facebook vs Google Login")
print("=" * 80)

# Test 1: POST to Facebook login
print("\n1. POST към /accounts/facebook/login/:")
print("-" * 80)

factory = RequestFactory()
request = factory.post('/accounts/facebook/login/', {})

# Add middleware
middleware = SessionMiddleware(lambda x: None)
middleware.process_request(request)
request.session.save()

msg_middleware = MessageMiddleware(lambda x: None)
msg_middleware.process_request(request)

request.site = Site.objects.get_current()
request.user = None

# Add CSRF token
csrf_middleware = CsrfViewMiddleware(lambda x: None)
csrf_middleware.process_request(request)

try:
    resolved = resolve('/accounts/facebook/login/')
    print(f"View: {resolved.view_name}")
    
    response = resolved.func(request, **resolved.kwargs)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code in [301, 302, 303, 307, 308]:
        location = response.get('Location', 'N/A')
        print(f"Redirect Location: {location}")
        
        if 'facebook.com' in location:
            print("✅✅✅ КОРЕКТНО: Redirect-ва към Facebook OAuth!")
        elif 'google.com' in location or 'accounts.google.com' in location:
            print("❌❌❌ ГРЕШКА: Redirect-ва към Google OAuth (не Facebook)!")
            print("\n🔍 ПРОБЛЕМЪТ Е:")
            print("   POST handler-ът не разпознава че това е Facebook endpoint!")
        else:
            print(f"⚠️  Неочакван redirect: {location}")
    else:
        print(f"⚠️  Не е redirect response (status {response.status_code})")
        
except Exception as e:
    import traceback
    print(f"❌ ERROR: {e}")
    print(traceback.format_exc())

# Test 2: POST to Google login (за сравнение)
print("\n\n2. POST към /accounts/google/login/ (за сравнение):")
print("-" * 80)

request2 = factory.post('/accounts/google/login/', {})
middleware.process_request(request2)
request2.session.save()
msg_middleware.process_request(request2)
request2.site = Site.objects.get_current()
request2.user = None
csrf_middleware.process_request(request2)

try:
    resolved2 = resolve('/accounts/google/login/')
    response2 = resolved2.func(request2, **resolved2.kwargs)
    
    print(f"Status code: {response2.status_code}")
    
    if response2.status_code in [301, 302, 303, 307, 308]:
        location2 = response2.get('Location', 'N/A')
        print(f"Redirect Location: {location2}")
        
        if 'google.com' in location2 or 'accounts.google.com' in location2:
            print("✅ Google POST коректно redirect-ва към Google")
        elif 'facebook.com' in location2:
            print("❌ Google POST грешно redirect-ва към Facebook")
            
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 3: Check URL kwargs
print("\n\n3. URL PATTERN KWARGS (какви параметри получава view-то):")
print("-" * 80)

for url in ['/accounts/facebook/login/', '/accounts/google/login/']:
    try:
        resolved = resolve(url)
        print(f"\n{url}:")
        print(f"  view_name: {resolved.view_name}")
        print(f"  url_name: {resolved.url_name}")
        print(f"  kwargs: {resolved.kwargs}")
        print(f"  args: {resolved.args}")
        
        # Check if 'provider' is in kwargs
        if 'provider' in resolved.kwargs:
            print(f"  ✅ Provider parameter: {resolved.kwargs['provider']}")
        else:
            print(f"  ⚠️  БЕЗ provider parameter в kwargs!")
            
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 80)
print("ДИАГНОСТИКА ЗАВЪРШЕНА")
print("=" * 80)
print("\nАКО Facebook POST redirect-ва към Google:")
print("  → Provider parameter липсва или е грешен в URL kwargs")
print("  → РЕШЕНИЕ: Трябва да проверим django-allauth URL patterns")
