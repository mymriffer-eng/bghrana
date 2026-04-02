#!/usr/bin/env python
"""
DISABLE template caching в settings.py
Ще направи templates да се зареждат отново при всеки request
"""

import os
import shutil
import time

settings_file = '/home/bghranac/public_html/products/settings.py'
backup_file = settings_file + '.backup_before_cache_disable'

print("=" * 70)
print("DISABLE TEMPLATE CACHING")
print("=" * 70)

# 1. Backup на settings.py
if not os.path.exists(backup_file):
    shutil.copy2(settings_file, backup_file)
    print(f"\n✅ Backup created: {backup_file}")
else:
    print(f"\n✅ Backup already exists: {backup_file}")

# 2. Прочитаме settings.py
with open(settings_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 3. Проверка дали вече сме променили файла
if "'loaders':" in content and "filesystem.Loader" in content:
    print("\n⚠️ Template loaders вече са конфигурирани")
    print("   Проверяваме дали са правилни...")
else:
    print("\n📝 Добавяме explicit loaders БЕЗ caching...")

# 4. Намираме TEMPLATES секцията и добавяме loaders
# Търсим 'OPTIONS': {
# и добавяме 'loaders' преди 'context_processors'

new_loaders_config = """            'loaders': [
                # БЕЗ cached.Loader - винаги зарежда от диск
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
"""

# Търсим OPTIONS секцията
if "'OPTIONS': {" in content:
    # Проверяваме дали вече има loaders
    if "'loaders':" not in content:
        # Добавяме loaders ПРЕДИ context_processors
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            # Когато намерим 'OPTIONS': {, на следващия ред добавяме loaders
            if "'OPTIONS': {" in line and i < len(lines) - 1:
                # Проверяваме дали следващият ред е context_processors
                if 'context_processors' in lines[i+1]:
                    # Добавяме loaders ПРЕДИ context_processors
                    new_lines.append(new_loaders_config)
        
        content = '\n'.join(new_lines)
        
        # Записваме обновения файл
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ Добавени explicit loaders БЕЗ caching")
    else:
        print("   ✅ Loaders вече са дефинирани")

# 5. Изтриваме __pycache__ директории
print("\n📁 Изтриваме __pycache__ директории:")
pycache_count = 0
for root, dirs, files in os.walk('/home/bghranac/public_html'):
    for dir_name in list(dirs):  # Use list() to avoid modification during iteration
        if dir_name == '__pycache__':
            dir_path = os.path.join(root, dir_name)
            try:
                import shutil
                shutil.rmtree(dir_path)
                pycache_count += 1
            except Exception as e:
                pass

print(f"   ✅ Изтрити {pycache_count} __pycache__ директории")

# 6. HARD restart
print("\n🔄 PASSENGER HARD RESTART:")
wsgi_file = '/home/bghranac/public_html/passenger_wsgi.py'

if os.path.exists(wsgi_file):
    # Модифицираме passenger_wsgi.py
    with open(wsgi_file, 'r', encoding='utf-8') as f:
        wsgi_content = f.read()
    
    # Премахваме стари timestamp коментари
    lines = wsgi_content.split('\n')
    filtered_lines = [line for line in lines if not line.startswith('# Force reload timestamp:')]
    wsgi_content = '\n'.join(filtered_lines)
    
    # Добавяме нов timestamp
    timestamp = time.time()
    wsgi_content = f"# Force reload timestamp: {timestamp}\n" + wsgi_content
    
    with open(wsgi_file, 'w', encoding='utf-8') as f:
        f.write(wsgi_content)
    
    os.utime(wsgi_file, None)
    print(f"   ✅ Modified: {wsgi_file}")

# Update tmp/restart.txt
restart_file = '/home/bghranac/public_html/tmp/restart.txt'
os.makedirs('/home/bghranac/public_html/tmp', exist_ok=True)
with open(restart_file, 'w') as f:
    f.write(f"Restart at: {time.time()}\n")
os.utime(restart_file, None)
print(f"   ✅ Updated: {restart_file}")

print("\n" + "=" * 70)
print("✅ ГОТОВО!")
print("=" * 70)
print("\n⚠️ IMPORTANT:")
print("   1. Изчакай 15-20 секунди")
print("   2. Тествай: https://bghrana.com/accounts/facebook/login/")
print("   3. АКО ПАК е Google → направи STOP/START от cPanel")
print("\n   Backup на оригинален settings.py:")
print(f"   {backup_file}")
print("\n   За да възстановиш оригинала:")
print(f"   cp {backup_file} {settings_file}")
print("=" * 70)
