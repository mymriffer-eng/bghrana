#!/usr/bin/env python
"""
Верификация на template loading за Facebook/Google Login
Показва КОЙ template файл Django ще използва
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/bghranac/public_html')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.template.loader import select_template, get_template
from django.template import engines
from django.conf import settings

print("=" * 70)
print("DJANGO TEMPLATE LOADING VERIFICATION")
print("=" * 70)

# 1. Проверка на TEMPLATES settings
print("\n1. TEMPLATES SETTINGS:")
for idx, config in enumerate(settings.TEMPLATES):
    print(f"\nEngine {idx}: {config.get('BACKEND')}")
    if 'DIRS' in config:
        print(f"   DIRS: {config['DIRS']}")
    if 'APP_DIRS' in config:
        print(f"   APP_DIRS: {config['APP_DIRS']}")
    if 'OPTIONS' in config and 'context_processors' in config['OPTIONS']:
        print(f"   Context processors: {len(config['OPTIONS']['context_processors'])}")

# 2. Проверка на template loaders
print("\n2. TEMPLATE LOADERS:")
engine = engines['django']
print(f"   Engine: {engine}")
if hasattr(engine, 'engine'):
    loaders = engine.engine.template_loaders
    print(f"   Loaders: {loaders}")

# 3. Опит за зареждане на provider-specific templates
print("\n3. TEMPLATE RESOLUTION:")

templates_to_test = [
    'socialaccount/facebook/login.html',
    'socialaccount/google/login.html',
    'socialaccount/login.html',
]

for template_name in templates_to_test:
    print(f"\n   Testing: {template_name}")
    try:
        template = get_template(template_name)
        print(f"   ✅ FOUND: {template.origin.name if hasattr(template, 'origin') else 'unknown origin'}")
        
        # Опит да прочетем съдържанието
        try:
            content = template.template.source
            if 'Facebook' in content:
                print(f"      Contains: 'Facebook' ✅")
            elif 'Google' in content:
                print(f"      Contains: 'Google' ✅")
            # Показваме заглавието
            if 'head_title' in content:
                import re
                title_match = re.search(r'{%\s*block head_title\s*%}(.*?){%\s*endblock\s*%}', content)
                if title_match:
                    print(f"      Title: {title_match.group(1).strip()}")
        except Exception as e:
            print(f"      Could not read content: {e}")
            
    except Exception as e:
        print(f"   ❌ NOT FOUND: {e}")

# 4. Проверка дали файловете физически съществуват
print("\n4. PHYSICAL FILE CHECK:")
files_to_check = [
    '/home/bghranac/public_html/catalog/templates/socialaccount/facebook/login.html',
    '/home/bghranac/public_html/catalog/templates/socialaccount/google/login.html',
    '/home/bghranac/public_html/catalog/templates/socialaccount/login.html',
]

for filepath in files_to_check:
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"   ✅ {filepath}")
        print(f"      Size: {size} bytes")
        # Проверка на съдържанието
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(100)  # Първите 100 chars
            if 'Facebook' in content:
                print(f"      Content: Contains 'Facebook' ✅")
            elif 'Google' in content:
                print(f"      Content: Contains 'Google' ✅")
    else:
        print(f"   ❌ NOT FOUND: {filepath}")

# 5. Проверка на template dirs в настройките
print("\n5. TEMPLATE SEARCH PATHS:")
print(f"   BASE_DIR: {settings.BASE_DIR}")
for idx, config in enumerate(settings.TEMPLATES):
    if 'DIRS' in config:
        for directory in config['DIRS']:
            print(f"   Template DIR: {directory}")
            if os.path.exists(directory):
                print(f"      ✅ Exists")
            else:
                print(f"      ❌ Not found")

# 6. Проверка на installed apps
print("\n6. CATALOG APP:")
if 'catalog' in settings.INSTALLED_APPS:
    print("   ✅ 'catalog' in INSTALLED_APPS")
    catalog_templates = '/home/bghranac/public_html/catalog/templates'
    if os.path.exists(catalog_templates):
        print(f"   ✅ {catalog_templates} exists")
    else:
        print(f"   ❌ {catalog_templates} NOT FOUND")
else:
    print("   ❌ 'catalog' NOT in INSTALLED_APPS")

print("\n" + "=" * 70)
print("✅ ГОТОВО!")
print("=" * 70)
