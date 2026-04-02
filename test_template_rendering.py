#!/usr/bin/env python
"""
Рендерира login template и показва ТОЧНИЯ генериран HTML
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.template import Template, Context
from django.test import RequestFactory
from django.contrib.sites.shortcuts import get_current_site

# Създай фалшива заявка
factory = RequestFactory()
request = factory.get('/accounts/login/')

# Set site
from django.contrib.sites.models import Site
request.site = Site.objects.get_current()

print("\n" + "="*70)
print("🔍 ТЕСТ НА TEMPLATE TAG RENDERING")
print("="*70 + "\n")

# Тествай template tag директно
template_code = """
{% load socialaccount %}
Google URL: {% provider_login_url 'google' %}
Facebook URL: {% provider_login_url 'facebook' %}
"""

template = Template(template_code)
context = Context({'request': request})

try:
    output = template.render(context)
    print("✅ Template рендериран успешно:\n")
    print(output)
    print()
    
    # Провери дали URL-ите са различни
    lines = output.strip().split('\n')
    google_line = [l for l in lines if 'Google' in l][0] if any('Google' in l for l in lines) else None
    facebook_line = [l for l in lines if 'Facebook' in l][0] if any('Facebook' in l for l in lines) else None
    
    if google_line and facebook_line:
        google_url = google_line.split(': ')[1].strip()
        facebook_url = facebook_line.split(': ')[1].strip()
        
        print(f"Google URL:   '{google_url}'")
        print(f"Facebook URL: '{facebook_url}'")
        print()
        
        if google_url == facebook_url:
            print("❌ ПРОБЛЕМ ОТКРИТ: И двете URL-та са ЕДНАКВИ!")
            print("   Template tag {% provider_login_url 'facebook' %} връща Google URL")
        else:
            print("✅ URL-тата са различни - template tag работи правилно")
            
        if 'facebook' in facebook_url:
            print("✅ Facebook URL съдържа 'facebook'")
        else:
            print("❌ Facebook URL НЕ съдържа 'facebook'!")
            
except Exception as e:
    print(f"❌ Грешка при рендериране: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("🔍 ПРОВЕРКА НА SOCIALACCOUNT ADAPTER")
print("="*70 + "\n")

try:
    from allauth.socialaccount import app_settings
    from allauth.socialaccount.adapter import get_adapter
    
    adapter = get_adapter(request)
    
    print("Adapter class:", adapter.__class__)
    print()
    
    # Опитай се да вземеш Google provider
    try:
        google_provider = adapter.get_provider(request, 'google')
        print(f"✅ Google provider: {google_provider}")
        print(f"   Provider ID: {google_provider.id}")
    except Exception as e:
        print(f"❌ Google provider грешка: {e}")
    
    # Опитай се да вземеш Facebook provider
    try:
        facebook_provider = adapter.get_provider(request, 'facebook')
        print(f"✅ Facebook provider: {facebook_provider}")
        print(f"   Provider ID: {facebook_provider.id}")
    except Exception as e:
        print(f"❌ Facebook provider грешка: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"❌ Adapter грешка: {e}")
    import traceback
    traceback.print_exc()

print()
