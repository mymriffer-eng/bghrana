#!/usr/bin/env python
"""
Тест на Facebook Login endpoint директно
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.test import RequestFactory
from allauth.socialaccount.providers.facebook.views import oauth2_login
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=" * 70)
print("ТЕСТ НА FACEBOOK LOGIN ENDPOINT")
print("=" * 70)

# Проверка на Facebook app
try:
    fb_app = SocialApp.objects.get(provider='facebook')
    print(f"\n✓ Facebook App намерен:")
    print(f"  Name: {fb_app.name}")
    print(f"  Client ID: {fb_app.client_id}")
    print(f"  Sites: {[s.domain for s in fb_app.sites.all()]}")
except SocialApp.DoesNotExist:
    print("\n✗ Facebook App НЕ е намерен!")
    exit(1)

# Симулация на request към /accounts/facebook/login/
factory = RequestFactory()
request = factory.get('/accounts/facebook/login/')

# Добавяне на session
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

middleware = SessionMiddleware(lambda r: None)
middleware.process_request(request)
request.session.save()

# Добавяне на site
request.site = Site.objects.get_current()
print(f"\n✓ Request site: {request.site.domain}")

# Проверка на allauth provider registry
from allauth.socialaccount import providers

print(f"\n✓ Регистрирани providers:")
for provider in providers.registry.get_list():
    print(f"  - {provider.id}: {provider.name}")

# Специфична проверка за Facebook
try:
    fb_provider = providers.registry.by_id('facebook')
    print(f"\n✓ Facebook provider намерен: {fb_provider.name}")
    
    # Опит да вземе app
    from allauth.socialaccount.adapter import get_adapter
    from django.contrib.auth.models import AnonymousUser
    request.user = AnonymousUser()
    
    adapter = get_adapter()
    try:
        app = adapter.get_app(request, 'facebook')
        print(f"✓ Facebook app достъпен през adapter:")
        print(f"  Name: {app.name}")
        print(f"  Client ID: {app.client_id}")
    except Exception as e:
        print(f"✗ Грешка при взимане на app: {e}")
        
except Exception as e:
    print(f"\n✗ Facebook provider НЕ е намерен: {e}")

print("\n" + "=" * 70)
print("ПРОВЕРКА НА SOCIALACCOUNT_PROVIDERS SETTINGS")
print("=" * 70)
from django.conf import settings

if hasattr(settings, 'SOCIALACCOUNT_PROVIDERS'):
    import pprint
    print("\nSOCIALACCOUNT_PROVIDERS configuration:")
    pprint.pprint(settings.SOCIALACCOUNT_PROVIDERS)
    
    if 'facebook' in settings.SOCIALACCOUNT_PROVIDERS:
        print("\n✓ Facebook е в SOCIALACCOUNT_PROVIDERS")
    else:
        print("\n✗ Facebook ЛИПСВА в SOCIALACCOUNT_PROVIDERS!")
else:
    print("\n✗ SOCIALACCOUNT_PROVIDERS не е дефиниран!")

print("=" * 70)
