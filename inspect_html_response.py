#!/usr/bin/env python3
"""
ПОКАЗВА HTML СЪДЪРЖАНИЕТО което Facebook/Google view-та връщат
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.urls import resolve
from django.contrib.sites.models import Site

print("=" * 80)
print("HTML RESPONSE CONTENT INSPECTION")
print("=" * 80)

factory = RequestFactory()

# Test 1: Facebook view
print("\n1. FACEBOOK LOGIN VIEW HTML:")
print("-" * 80)

request1 = factory.get('/accounts/facebook/login/')
middleware = SessionMiddleware(lambda x: None)
middleware.process_request(request1)
request1.session.save()
msg_middleware = MessageMiddleware(lambda x: None)
msg_middleware.process_request(request1)
request1.site = Site.objects.get_current()

try:
    resolved1 = resolve('/accounts/facebook/login/')
    response1 = resolved1.func(request1, **resolved1.kwargs)
    
    html_content = response1.content.decode('utf-8')
    
    print(f"Status: {response1.status_code}")
    print(f"Content-Type: {response1.get('Content-Type')}")
    print(f"HTML Length: {len(html_content)} bytes")
    print(f"\nHTML CONTENT (първи 2000 символа):")
    print("-" * 80)
    print(html_content[:2000])
    print("-" * 80)
    
    # Search for OAuth URLs
    if 'facebook.com' in html_content:
        print("\n✅ HTML съдържа 'facebook.com'")
        # Extract the URL
        import re
        fb_urls = re.findall(r'https://[^"\s]*facebook\.com[^"\s]*', html_content)
        for url in fb_urls[:3]:
            print(f"   Facebook URL: {url[:150]}...")
    else:
        print("\n❌ HTML НЕ съдържа 'facebook.com' - ПРОБЛЕМ!")
    
    if 'google.com' in html_content or 'accounts.google.com' in html_content:
        print("\n❌❌❌ HTML съдържа 'google.com' - ТУК Е ПРОБЛЕМЪТ!")
        # Extract the URL
        import re
        google_urls = re.findall(r'https://[^"\s]*(?:accounts\.)?google\.com[^"\s]*', html_content)
        for url in google_urls[:3]:
            print(f"   Google URL: {url[:150]}...")
    else:
        print("\n✅ HTML не съдържа 'google.com'")
        
except Exception as e:
    import traceback
    print(f"❌ ERROR: {e}")
    print(traceback.format_exc())

# Test 2: Google view за сравнение
print("\n\n2. GOOGLE LOGIN VIEW HTML (за сравнение):")
print("-" * 80)

request2 = factory.get('/accounts/google/login/')
middleware.process_request(request2)
request2.session.save()
msg_middleware.process_request(request2)
request2.site = Site.objects.get_current()

try:
    resolved2 = resolve('/accounts/google/login/')
    response2 = resolved2.func(request2, **resolved2.kwargs)
    
    html_content2 = response2.content.decode('utf-8')
    
    print(f"Status: {response2.status_code}")
    print(f"HTML Length: {len(html_content2)} bytes")
    print(f"\nHTML CONTENT (първи 1500 символа):")
    print("-" * 80)
    print(html_content2[:1500])
    print("-" * 80)
    
    if 'google.com' in html_content2 or 'accounts.google.com' in html_content2:
        print("\n✅ Google HTML коректно съдържа 'google.com'")
    
    if 'facebook.com' in html_content2:
        print("\n❌ Google HTML грешно съдържа 'facebook.com'")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 3: Extract OAuth URLs precisely
print("\n\n3. EXACT OAUTH URL COMPARISON:")
print("-" * 80)

import re

try:
    # Facebook view
    request_fb = factory.get('/accounts/facebook/login/')
    middleware.process_request(request_fb)
    request_fb.session.save()
    msg_middleware.process_request(request_fb)
    request_fb.site = Site.objects.get_current()
    
    resolved_fb = resolve('/accounts/facebook/login/')
    response_fb = resolved_fb.func(request_fb, **resolved_fb.kwargs)
    html_fb = response_fb.content.decode('utf-8')
    
    # Find OAuth redirect URL in form action or meta refresh
    form_actions = re.findall(r'action=["\']([^"\']+)["\']', html_fb)
    meta_refresh = re.findall(r'<meta[^>]+url=([^"\s>]+)', html_fb)
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html_fb)
    
    print("FACEBOOK VIEW Extracted URLs:")
    if form_actions:
        print(f"  Form actions: {form_actions[:2]}")
    if meta_refresh:
        print(f"  Meta refresh: {meta_refresh[:2]}")
    if hrefs:
        oauth_hrefs = [h for h in hrefs if 'oauth' in h.lower() or 'facebook' in h or 'google' in h]
        if oauth_hrefs:
            print(f"  OAuth hrefs: {oauth_hrefs[:2]}")
    
    # Google view
    request_g = factory.get('/accounts/google/login/')
    middleware.process_request(request_g)
    request_g.session.save()
    msg_middleware.process_request(request_g)
    request_g.site = Site.objects.get_current()
    
    resolved_g = resolve('/accounts/google/login/')
    response_g = resolved_g.func(request_g, **resolved_g.kwargs)
    html_g = response_g.content.decode('utf-8')
    
    form_actions_g = re.findall(r'action=["\']([^"\']+)["\']', html_g)
    meta_refresh_g = re.findall(r'<meta[^>]+url=([^"\s>]+)', html_g)
    
    print("\nGOOGLE VIEW Extracted URLs:")
    if form_actions_g:
        print(f"  Form actions: {form_actions_g[:2]}")
    if meta_refresh_g:
        print(f"  Meta refresh: {meta_refresh_g[:2]}")
    
except Exception as e:
    import traceback
    print(f"❌ ERROR: {e}")
    print(traceback.format_exc())

print("\n" + "=" * 80)
print("ДИАГНОСТИКА ЗАВЪРШЕНА")
print("=" * 80)
print("\nАКО Facebook HTML съдържа google.com URL, проблемът е в django-allauth")
print("генерирането на OAuth URL - provider-ите са swap-нати в паметта!")
