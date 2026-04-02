#!/usr/bin/env python3
"""
Проверка на django-allauth templates - кой template се използва за Facebook vs Google
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.template.loader import get_template
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.urls import resolve
from django.contrib.sites.models import Site

print("=" * 80)
print("ALLAUTH TEMPLATE INVESTIGATION")
print("=" * 80)

# Check what templates exist for socialaccount
print("\n1. ALLAUTH SOCIALACCOUNT TEMPLATE PATHS:")
print("-" * 80)

from django.conf import settings

print(f"TEMPLATES DIRS: {settings.TEMPLATES[0].get('DIRS', [])}")
print(f"INSTALLED_APPS socialaccount:")
for app in settings.INSTALLED_APPS:
    if 'socialaccount' in app:
        print(f"  - {app}")

# Try to find templates
import glob
import os

# Search in project templates
for template_dir in settings.TEMPLATES[0].get('DIRS', []):
    if os.path.exists(template_dir):
        print(f"\nSearching in: {template_dir}")
        social_templates = glob.glob(f"{template_dir}/**/socialaccount/**/*.html", recursive=True)
        for t in social_templates[:10]:
            print(f"  - {t}")

# Test actual template rendering
print("\n\n2. TEMPLATE USED BY FACEBOOK VIEW:")
print("-" * 80)

factory = RequestFactory()

# Facebook request
request_fb = factory.get('/accounts/facebook/login/')
middleware = SessionMiddleware(lambda x: None)
middleware.process_request(request_fb)
request_fb.session.save()
msg_middleware = MessageMiddleware(lambda x: None)
msg_middleware.process_request(request_fb)
request_fb.site = Site.objects.get_current()

try:
    from django.test.utils import setup_test_environment
    from django.template import loader
    
    # Get the view
    resolved = resolve('/accounts/facebook/login/')
    
    # Call view to see which template it uses
    response = resolved.func(request_fb, **resolved.kwargs)
    
    # Try to extract template name from response
    if hasattr(response, 'template_name'):
        print(f"✅ Template name: {response.template_name}")
    
    if hasattr(response, 'context_data'):
        context = response.context_data
        print(f"\n✅ Context keys: {list(context.keys())}")
        
        if 'provider' in context:
            provider = context['provider']
            print(f"\n✅ Provider in context:")
            print(f"   ID: {provider.id if hasattr(provider, 'id') else 'N/A'}")
            print(f"   Name: {provider.name if hasattr(provider, 'name') else 'N/A'}")
            print(f"   Class: {provider.__class__}")
        else:
            print(f"\n❌ NO 'provider' in context")
    
    # Check templates attribute (for TemplateResponse)
    if hasattr(response, '_request'):
        print(f"\n✅ Response has _request")
    
    # Try to get the actual template object
    if hasattr(response, 'template_name'):
        try:
            template = loader.get_template(response.template_name)
            print(f"\n✅ Template object: {template}")
            print(f"   Template origin: {template.origin if hasattr(template, 'origin') else 'N/A'}")
        except Exception as e:
            print(f"\n❌ Could not load template: {e}")
            
except Exception as e:
    import traceback
    print(f"❌ ERROR: {e}")
    print(traceback.format_exc())

# Test Google view for comparison
print("\n\n3. TEMPLATE USED BY GOOGLE VIEW:")
print("-" * 80)

request_g = factory.get('/accounts/google/login/')
middleware.process_request(request_g)
request_g.session.save()
msg_middleware.process_request(request_g)
request_g.site = Site.objects.get_current()

try:
    resolved_g = resolve('/accounts/google/login/')
    response_g = resolved_g.func(request_g, **resolved_g.kwargs)
    
    if hasattr(response_g, 'template_name'):
        print(f"✅ Template name: {response_g.template_name}")
    
    if hasattr(response_g, 'context_data'):
        context_g = response_g.context_data
        if 'provider' in context_g:
            provider_g = context_g['provider']
            print(f"\n✅ Provider in context:")
            print(f"   ID: {provider_g.id if hasattr(provider_g, 'id') else 'N/A'}")
            print(f"   Name: {provider_g.name if hasattr(provider_g, 'name') else 'N/A'}")
            
except Exception as e:
    print(f"❌ ERROR: {e}")

# Check if there are custom templates overriding allauth defaults
print("\n\n4. CHECKING FOR CUSTOM SOCIALACCOUNT TEMPLATES:")
print("-" * 80)

template_paths_to_check = [
    'socialaccount/login.html',
    'socialaccount/provider_login.html', 
    'socialaccount/google/login.html',
    'socialaccount/facebook/login.html',
]

for path in template_paths_to_check:
    try:
        template = get_template(path)
        print(f"✅ Found: {path}")
        if hasattr(template, 'origin'):
            print(f"   Location: {template.origin.name}")
    except Exception as e:
        print(f"❌ Not found: {path}")

print("\n" + "=" * 80)
print("DIAGNOSTIC ЗАВЪРШЕН")
print("=" * 80)
print("\nАКО Facebook view използва същия template като Google,")
print("проблемът е в provider context - providers са swap-нати!")
