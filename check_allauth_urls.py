#!/usr/bin/env python3
"""
Проверка на django-allauth URL patterns - дали facebook и google имат различни endpoints
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.urls import reverse, resolve, get_resolver
from allauth.socialaccount import providers

print("=" * 60)
print("DJANGO-ALLAUTH URL ROUTING DIAGNOSTIC")
print("=" * 60)

# 1. Проверка на reverse() URLs
print("\n1. REVERSE LOOKUP (какви URLs генерира Django):")
print("-" * 60)

try:
    google_url = reverse('google_login')
    print(f"✅ reverse('google_login') = {google_url}")
except Exception as e:
    print(f"❌ Google reverse error: {e}")

try:
    facebook_url = reverse('facebook_login')
    print(f"✅ reverse('facebook_login') = {facebook_url}")
except Exception as e:
    print(f"❌ Facebook reverse error: {e}")

# Алтернативен метод - през socialaccount namespace
try:
    google_alt = reverse('socialaccount_login', kwargs={'provider': 'google'})
    print(f"✅ reverse socialaccount google = {google_alt}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    facebook_alt = reverse('socialaccount_login', kwargs={'provider': 'facebook'})
    print(f"✅ reverse socialaccount facebook = {facebook_alt}")
except Exception as e:
    print(f"❌ Error: {e}")

# 2. URL Resolution - какво се случва когато се отвори URL-а
print("\n2. URL RESOLUTION (какво се извиква при достъп до URL):")
print("-" * 60)

for path in ['/accounts/google/login/', '/accounts/facebook/login/']:
    try:
        resolved = resolve(path)
        print(f"\nPath: {path}")
        print(f"  View: {resolved.func}")
        print(f"  View name: {resolved.view_name}")
        print(f"  URL name: {resolved.url_name}")
        print(f"  Kwargs: {resolved.kwargs}")
        print(f"  Namespace: {resolved.namespace}")
    except Exception as e:
        print(f"\n❌ Path {path} - Error: {e}")

# 3. Installed providers registry
print("\n3. ALLAUTH PROVIDERS REGISTRY:")
print("-" * 60)

registry = providers.registry.get_class_list()
print(f"Registered providers: {len(registry)}")
for provider_class in registry:
    provider_id = provider_class.id if hasattr(provider_class, 'id') else 'N/A'
    provider_name = provider_class.name if hasattr(provider_class, 'name') else 'N/A'
    print(f"  - {provider_id}: {provider_name} ({provider_class})")

# 4. URL Patterns inspection
print("\n4. ALLAUTH URL PATTERNS (registered routes):")
print("-" * 60)

resolver = get_resolver()

def find_allauth_patterns(urlpatterns, prefix=''):
    """Recursively find all allauth URL patterns"""
    results = []
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            # URLResolver (include)
            new_prefix = prefix + str(pattern.pattern)
            results.extend(find_allauth_patterns(pattern.url_patterns, new_prefix))
        else:
            # URLPattern
            full_path = prefix + str(pattern.pattern)
            if 'account' in full_path or 'facebook' in full_path or 'google' in full_path:
                results.append({
                    'path': full_path,
                    'name': pattern.name,
                    'view': str(pattern.callback) if hasattr(pattern, 'callback') else 'N/A'
                })
    return results

allauth_patterns = find_allauth_patterns(resolver.url_patterns)
for p in allauth_patterns[:20]:  # Покажи първите 20
    print(f"  {p['path']}")
    print(f"    name: {p['name']}")
    # print(f"    view: {p['view']}")

# 5. Provider URL pattern check
print("\n5. PROVIDER-SPECIFIC URL CHECK:")
print("-" * 60)

from allauth.socialaccount.models import SocialApp

google_apps = SocialApp.objects.filter(provider='google')
facebook_apps = SocialApp.objects.filter(provider='facebook')

print(f"Google SocialApps in DB: {google_apps.count()}")
for app in google_apps:
    print(f"  - ID: {app.id}, Client ID: {app.client_id[:20]}..., Sites: {list(app.sites.all())}")

print(f"\nFacebook SocialApps in DB: {facebook_apps.count()}")
for app in facebook_apps:
    print(f"  - ID: {app.id}, Client ID: {app.client_id[:20]}..., Sites: {list(app.sites.all())}")

# 6. КРИТИЧЕН ТЕСТ - Request simulation
print("\n6. REQUEST SIMULATION (most важен тест):")
print("-" * 60)

from django.test import RequestFactory
from django.contrib.sites.models import Site

factory = RequestFactory()
request = factory.get('/accounts/facebook/login/')
request.site = Site.objects.get_current()

try:
    resolved = resolve('/accounts/facebook/login/')
    view_func = resolved.func
    
    print(f"Resolved view: {view_func}")
    print(f"View name: {resolved.view_name}")
    
    # Опитай да извикаш view-то
    # response = view_func(request, **resolved.kwargs)
    # print(f"Response status: {response.status_code}")
    # print(f"Response Location header: {response.get('Location', 'N/A')}")
    
except Exception as e:
    import traceback
    print(f"❌ Error: {e}")
    print(traceback.format_exc())

print("\n" + "=" * 60)
print("DIAGNOSTIC ЗАВЪРШЕН")
print("=" * 60)
