#!/usr/bin/env python
"""
АГРЕСИВНО изчистване на Django template cache + HARD restart
"""

import os
import sys
import time
import shutil

print("=" * 70)
print("FORCE CLEAR TEMPLATE CACHE + HARD RESTART")
print("=" * 70)

# 1. Изтриване на всички .pyc файлове (compiled Python cache)
print("\n1. ИЗТРИВАНЕ НА .pyc CACHE FILES:")
pyc_count = 0
for root, dirs, files in os.walk('/home/bghranac/public_html'):
    # Skip __pycache__ directories
    dirs[:] = [d for d in dirs if d != '__pycache__']
    
    for file in files:
        if file.endswith('.pyc') or file.endswith('.pyo'):
            filepath = os.path.join(root, file)
            try:
                os.remove(filepath)
                pyc_count += 1
            except Exception as e:
                print(f"   ⚠️ Не може да се изтрие: {filepath} - {e}")

# Изтриване на __pycache__ директории
pycache_count = 0
for root, dirs, files in os.walk('/home/bghranac/public_html'):
    for dir_name in dirs:
        if dir_name == '__pycache__':
            dir_path = os.path.join(root, dir_name)
            try:
                shutil.rmtree(dir_path)
                pycache_count += 1
            except Exception as e:
                print(f"   ⚠️ Не може да се изтрие: {dir_path} - {e}")

print(f"   ✅ Изтрити {pyc_count} .pyc файла")
print(f"   ✅ Изтрити {pycache_count} __pycache__ директории")

# 2. Setup Django и изчистване на template cache
print("\n2. DJANGO TEMPLATE CACHE CLEAR:")
try:
    sys.path.insert(0, '/home/bghranac/public_html')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
    import django
    django.setup()
    
    from django.template import engines
    from django.core.cache import cache
    
    # Изчистване на Django cache
    cache.clear()
    print("   ✅ Django cache.clear() executed")
    
    # Изчистване на template engine cache
    engine = engines['django']
    if hasattr(engine, 'engine'):
        # Reset template loaders
        if hasattr(engine.engine, 'template_loaders'):
            for loader in engine.engine.template_loaders:
                if hasattr(loader, 'reset'):
                    loader.reset()
                    print(f"   ✅ Reset loader: {loader}")
                if hasattr(loader, 'get_template_cache'):
                    loader.get_template_cache().clear()
                    print(f"   ✅ Cleared template cache: {loader}")
        
        # Force reload templates by clearing internal cache
        if hasattr(engine.engine, 'templates'):
            engine.engine.templates.clear()
            print("   ✅ Cleared engine.templates")
            
    print("   ✅ Template engine cache cleared")
    
except Exception as e:
    print(f"   ⚠️ Django cache clear error: {e}")

# 3. Изтриване на session files (ако има)
print("\n3. SESSION FILES:")
session_dir = '/home/bghranac/public_html/django_sessions'
if os.path.exists(session_dir):
    try:
        shutil.rmtree(session_dir)
        print(f"   ✅ Изтрити session files: {session_dir}")
    except Exception as e:
        print(f"   ⚠️ {e}")
else:
    print(f"   ℹ️ Няма session directory: {session_dir}")

# 4. SUPER HARD RESTART - модифициране на passenger_wsgi.py
print("\n4. PASSENGER SUPER HARD RESTART:")
wsgi_file = '/home/bghranac/public_html/passenger_wsgi.py'

if os.path.exists(wsgi_file):
    # Прочитаме файла
    with open(wsgi_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Добавяме timestamp коментар с уникален timestamp
    timestamp = time.time()
    new_comment = f"\n# Force reload timestamp: {timestamp}\n"
    
    # Проверяваме дали вече има timestamp коментари и ги премахваме
    lines = content.split('\n')
    filtered_lines = [line for line in lines if not line.startswith('# Force reload timestamp:')]
    content = '\n'.join(filtered_lines)
    
    # Добавяме новия коментар в началото
    content = new_comment + content
    
    # Записваме файла
    with open(wsgi_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Променяме timestamp на файла
    os.utime(wsgi_file, None)
    
    print(f"   ✅ Modified: {wsgi_file}")
    print(f"   ✅ Added timestamp: {timestamp}")
else:
    print(f"   ❌ Not found: {wsgi_file}")

# 5. Update tmp/restart.txt
print("\n5. TMP/RESTART.TXT:")
restart_file = '/home/bghranac/public_html/tmp/restart.txt'
restart_dir = os.path.dirname(restart_file)

if not os.path.exists(restart_dir):
    os.makedirs(restart_dir)
    print(f"   ✅ Created directory: {restart_dir}")

# Записваме текущия timestamp в файла
with open(restart_file, 'w') as f:
    f.write(f"Restart at: {time.time()}\n")

os.utime(restart_file, None)
print(f"   ✅ Updated: {restart_file}")

# 6. Финална верификация
print("\n6. ВЕРИФИКАЦИЯ НА TEMPLATE FILES:")
templates_to_check = [
    '/home/bghranac/public_html/catalog/templates/socialaccount/facebook/login.html',
    '/home/bghranac/public_html/catalog/templates/socialaccount/google/login.html',
]

for template_path in templates_to_check:
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'Facebook' in content:
                print(f"   ✅ {os.path.basename(template_path)} - Contains 'Facebook'")
            elif 'Google' in content:
                print(f"   ✅ {os.path.basename(template_path)} - Contains 'Google'")
    else:
        print(f"   ❌ NOT FOUND: {template_path}")

print("\n" + "=" * 70)
print("✅ ГОТОВО! Template cache ИЗЧИСТЕН + HARD RESTART")
print("=" * 70)
print("\nИзчакай 15-20 секунди и тествай:")
print("https://bghrana.com/accounts/facebook/login/")
print("→ ТРЯБВА да показва 'Вход с Facebook' (НЕ Google)")
print("\nАко ПУАК не работи, направи от cPanel:")
print("Setup Python App → STOP → изчакай 10 сек → START")
print("=" * 70)
