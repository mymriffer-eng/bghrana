#!/usr/bin/env python
"""
Симулира POST request към Facebook login (като бутон click)
Показва къде редирект-ва и какви грешки има
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/bghranac/public_html')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.test import Client
from django.urls import reverse

print("=" * 70)
print("FACEBOOK LOGIN BUTTON SIMULATION")
print("=" * 70)

# Създаваме test client
client = Client()

# 1. GET request първо (за да вземем CSRF token)
print("\n1. GET /accounts/facebook/login/ (зареждане на страницата):")
get_response = client.get('/accounts/facebook/login/')
print(f"   Status: {get_response.status_code}")

if get_response.status_code == 200:
    print(f"   ✅ Страницата се зарежда")
    # Вземаме CSRF token
    if hasattr(get_response, 'cookies') and 'csrftoken' in get_response.cookies:
        csrf_token = get_response.cookies['csrftoken'].value
        print(f"   ✅ CSRF token: {csrf_token[:20]}...")
    else:
        print(f"   ⚠️ Няма CSRF token в cookies")
        csrf_token = None
else:
    print(f"   ❌ Грешка при зареждане")
    csrf_token = None

# 2. POST request (като бутон click)
print("\n2. POST /accounts/facebook/login/ (натискане на бутона):")

try:
    # Правим POST request с CSRF token
    post_data = {}
    if csrf_token:
        post_data['csrfmiddlewaretoken'] = csrf_token
    
    post_response = client.post(
        '/accounts/facebook/login/',
        data=post_data,
        follow=False  # Не следваме редиректи
    )
    
    print(f"   Status: {post_response.status_code}")
    
    if post_response.status_code == 302:
        # Redirect - това е очаквано
        redirect_url = post_response.url
        print(f"   ✅ REDIRECT към: {redirect_url}")
        
        # Проверка дали редирект-ва към Facebook
        if 'facebook.com' in redirect_url:
            print(f"   ✅ CORRECT: Редирект към Facebook OAuth!")
            print(f"\n   Facebook OAuth URL:")
            print(f"   {redirect_url[:100]}...")
            
            # Проверка на OAuth параметрите
            if 'client_id=' in redirect_url:
                print(f"   ✅ client_id е в URL-а")
            else:
                print(f"   ❌ ЛИПСВА client_id!")
                
            if 'redirect_uri=' in redirect_url:
                print(f"   ✅ redirect_uri е в URL-а")
                
                # Извличаме redirect_uri
                import urllib.parse
                parsed = urllib.parse.parse_qs(redirect_url.split('?')[1] if '?' in redirect_url else '')
                if 'redirect_uri' in parsed:
                    print(f"      Redirect URI: {parsed['redirect_uri'][0]}")
            else:
                print(f"   ❌ ЛИПСВА redirect_uri!")
                
        else:
            print(f"   ❌ ГРЕШКА: НЕ редирект-ва към Facebook!")
            print(f"      Редирект-ва към: {redirect_url}")
            
    elif post_response.status_code == 200:
        print(f"   ⚠️ Връща 200 вместо redirect")
        print(f"   Това означава че формата НЕ се submit-ва правилно")
        
        # Проверка за грешки в response
        content = post_response.content.decode('utf-8')
        if 'error' in content.lower():
            print(f"   ⚠️ Response съдържа 'error'")
            
    elif post_response.status_code == 400:
        print(f"   ❌ Bad Request (400)")
        content = post_response.content.decode('utf-8')
        if 'CSRF' in content:
            print(f"   ❌ CSRF token грешка!")
        else:
            print(f"   Response: {content[:200]}")
            
    elif post_response.status_code == 500:
        print(f"   ❌ Server Error (500)")
        
    else:
        print(f"   ⚠️ Неочаквал status code")
        
except Exception as e:
    print(f"   ❌ EXCEPTION: {e}")
    import traceback
    traceback.print_exc()

# 3. Проверка на Facebook App настройките
print("\n3. FACEBOOK APP CONFIG:")
from allauth.socialaccount.models import SocialApp

fb_app = SocialApp.objects.filter(provider='facebook').first()
if fb_app:
    print(f"   ✅ Client ID: {fb_app.client_id}")
    print(f"   ✅ Secret: {'SET' if fb_app.secret else 'MISSING'}")
    print(f"   ✅ Sites: {[s.domain for s in fb_app.sites.all()]}")
else:
    print(f"   ❌ Facebook app НЕ е в базата!")

# 4. Проверка на settings
print("\n4. DJANGO SETTINGS:")
from django.conf import settings

print(f"   DEBUG: {settings.DEBUG}")
print(f"   SITE_ID: {settings.SITE_ID}")

if hasattr(settings, 'SOCIALACCOUNT_PROVIDERS'):
    print(f"   ✅ SOCIALACCOUNT_PROVIDERS настроен")
else:
    print(f"   ⚠️ SOCIALACCOUNT_PROVIDERS не е в settings")

print("\n" + "=" * 70)
print("ДИАГНОЗА:")
print("=" * 70)

if post_response.status_code == 302 and 'facebook.com' in post_response.url:
    print("\n✅ POST REQUEST РАБОТИ ПРАВИЛНО!")
    print("   Django правилно redirect-ва към Facebook OAuth")
    print("\n   АКО БУТОНЪТ В БРАУЗЪРА НЕ РАБОТИ:")
    print("   → Проблемът е в browser/JavaScript")
    print("   → Отвори Browser Console (F12) и виж грешки")
    print("   → Провери Network tab какво се изпраща")
else:
    print("\n❌ POST REQUEST НЕ РАБОТИ!")
    print("   Django НЕ redirect-ва към Facebook правилно")
    
print("=" * 70)
