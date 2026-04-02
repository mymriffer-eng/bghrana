#!/usr/bin/env python
"""
Търси ВСИЧКИ login.html template файлове в production
"""

import os

print("=" * 70)
print("SEARCH ALL login.html TEMPLATES")
print("=" * 70)

# Търсим всички login.html файлове
print("\n🔍 ВСИЧКИ login.html ФАЙЛОВЕ:")

found_templates = []

for root, dirs, files in os.walk('/home/bghranac/public_html'):
    # Skip __pycache__ and .git
    dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules']]
    
    for file in files:
        if file == 'login.html':
            filepath = os.path.join(root, file)
            found_templates.append(filepath)

# Сортираме и показваме
found_templates.sort()

for idx, filepath in enumerate(found_templates, 1):
    print(f"\n{idx}. {filepath}")
    
    # Показваме размера
    size = os.path.getsize(filepath)
    print(f"   Size: {size} bytes")
    
    # Показваме първите 200 chars
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(500)
            
            # Проверка за Facebook/Google
            if 'Facebook' in content:
                print(f"   ✅ Contains: 'Facebook'")
            if 'Google' in content:
                print(f"   ✅ Contains: 'Google'")
                
            # Търсим head_title block
            if 'head_title' in content:
                import re
                match = re.search(r'{%\s*block head_title\s*%}(.*?){%\s*endblock', content, re.DOTALL)
                if match:
                    title = match.group(1).strip()
                    print(f"   Title block: {title[:50]}")
    except Exception as e:
        print(f"   ⚠️ Error reading: {e}")

print("\n" + "=" * 70)
print(f"TOTAL: {len(found_templates)} login.html файла")
print("=" * 70)

# Специална проверка на socialaccount templates
print("\n🔍 SOCIALACCOUNT TEMPLATES:")

socialaccount_dir = '/home/bghranac/public_html/catalog/templates/socialaccount'
if os.path.exists(socialaccount_dir):
    for root, dirs, files in os.walk(socialaccount_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                rel_path = filepath.replace('/home/bghranac/public_html/catalog/templates/', '')
                print(f"\n   {rel_path}")
                
                # Показваме размера и съдържанието
                size = os.path.getsize(filepath)
                print(f"      Size: {size} bytes")
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'Facebook' in content and 'Google' not in content:
                        print(f"      ✅ САМО Facebook")
                    elif 'Google' in content and 'Facebook' not in content:
                        print(f"      ✅ САМО Google")
                    elif 'Facebook' in content and 'Google' in content:
                        print(f"      ⚠️ И Facebook И Google")
else:
    print(f"   ❌ Директория не съществува: {socialaccount_dir}")

print("\n" + "=" * 70)
