#!/usr/bin/env python3
"""
Показва ПЪЛНИЯ HTML с фокус върху BODY и OAuth forms/scripts
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
print("FULL HTML BODY INSPECTION - OAuth URLs")
print("=" * 80)

factory = RequestFactory()

# Facebook view
request1 = factory.get('/accounts/facebook/login/')
middleware = SessionMiddleware(lambda x: None)
middleware.process_request(request1)
request1.session.save()
msg_middleware = MessageMiddleware(lambda x: None)
msg_middleware.process_request(request1)
request1.site = Site.objects.get_current()

print("\n1. FACEBOOK LOGIN HTML BODY (full content):")
print("-" * 80)

try:
    resolved1 = resolve('/accounts/facebook/login/')
    response1 = resolved1.func(request1, **resolved1.kwargs)
    
    html_content = response1.content.decode('utf-8')
    
    # Find <body> section
    import re
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
    
    if body_match:
        body_content = body_match.group(1)
        print("BODY TAG FOUND - Content:")
        print(body_content)
    else:
        print("No <body> tag found, showing full HTML:")
        print(html_content)
    
    # Search for specific patterns
    print("\n" + "=" * 80)
    print("SEARCH RESULTS:")
    print("=" * 80)
    
    # OAuth URLs
    oauth_urls = re.findall(r'https://[^"\'\s]*(?:facebook|google|accounts\.google)[^"\'\s]*oauth[^"\'\s]*', html_content, re.IGNORECASE)
    if oauth_urls:
        print(f"\n✅ OAuth URLs found ({len(oauth_urls)}):")
        for url in oauth_urls[:5]:
            print(f"   {url[:200]}")
    else:
        print("\n❌ No OAuth URLs found in HTML")
    
    # Forms
    forms = re.findall(r'<form[^>]*>.*?</form>', html_content, re.DOTALL | re.IGNORECASE)
    if forms:
        print(f"\n✅ Forms found ({len(forms)}):")
        for i, form in enumerate(forms[:3]):
            print(f"\n   Form {i+1}:")
            print(f"   {form[:500]}")
    else:
        print("\n❌ No forms found")
    
    # JavaScript redirects
    js_redirects = re.findall(r'location\.href\s*=\s*["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if js_redirects:
        print(f"\n✅ JavaScript redirects found ({len(js_redirects)}):")
        for url in js_redirects[:5]:
            print(f"   {url}")
    else:
        print("\n❌ No JavaScript location.href redirects")
    
    # window.location
    window_locs = re.findall(r'window\.location\s*=\s*["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if window_locs:
        print(f"\n✅ window.location redirects found ({len(window_locs)}):")
        for url in window_locs[:5]:
            print(f"   {url}")
    
    # Meta refresh
    meta_refresh = re.findall(r'<meta[^>]+http-equiv=["\']refresh["\'][^>]*content=["\'][^"\']*url=([^"\']+)["\']', html_content, re.IGNORECASE)
    if meta_refresh:
        print(f"\n✅ Meta refresh found ({len(meta_refresh)}):")
        for url in meta_refresh:
            print(f"   {url}")
    
    # Any mention of google domains in the context of OAuth
    if 'accounts.google.com' in html_content:
        print("\n❌❌❌ PROBLEM FOUND: 'accounts.google.com' in Facebook HTML!")
        positions = [m.start() for m in re.finditer('accounts.google.com', html_content)]
        for pos in positions[:3]:
            snippet = html_content[max(0, pos-200):min(len(html_content), pos+200)]
            print(f"\n   Context around position {pos}:")
            print(f"   ...{snippet}...")
    else:
        print("\n✅ 'accounts.google.com' NOT found in Facebook HTML (good)")
    
    if 'www.facebook.com/v' in html_content or 'graph.facebook.com' in html_content:
        print("\n✅ Facebook OAuth domains found (expected)")

except Exception as e:
    import traceback
    print(f"❌ ERROR: {e}")
    print(traceback.format_exc())

print("\n" + "=" * 80)
print("END OF INSPECTION")
print("=" * 80)
