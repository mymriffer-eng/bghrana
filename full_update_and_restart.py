#!/usr/bin/env python3
"""
ПЪЛЕН UPDATE - git pull + copy files + HARD restart на Passenger
Пусни този script от cPanel: Setup Python App → Run Python Script
"""
import os
import subprocess
import time
from datetime import datetime

print("=" * 70)
print("ПЪЛЕН UPDATE НА PRODUCTION")
print("=" * 70)

# 1. GIT PULL
print("\n1. GIT PULL (изтегляне на промени от GitHub)...")
print("-" * 70)
repo_path = '/home/bghranac/repositories/bghrana'
os.chdir(repo_path)

try:
    result = subprocess.run(['git', 'pull'], capture_output=True, text=True, timeout=30)
    print(result.stdout)
    if result.returncode == 0:
        print("✅ Git pull успешен")
    else:
        print(f"⚠️  Git pull warning: {result.stderr}")
except Exception as e:
    print(f"❌ Git pull грешка: {e}")

# 2. COPY FILES
print("\n2. КОПИРАНЕ НА ФАЙЛОВЕ към public_html...")
print("-" * 70)

import shutil

source = '/home/bghranac/repositories/bghrana'
dest = '/home/bghranac/public_html'

# Files and folders to copy
items_to_copy = [
    'catalog',
    'products', 
    'locale',
    'media',
    'staticfiles',
    'manage.py',
    'requirements.txt',
    'db.sqlite3'
]

copied_count = 0
for item in items_to_copy:
    src_path = os.path.join(source, item)
    dest_path = os.path.join(dest, item)
    
    if os.path.exists(src_path):
        try:
            if os.path.isdir(src_path):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(src_path, dest_path)
                print(f"  ✅ Копиран folder: {item}")
            else:
                shutil.copy2(src_path, dest_path)
                print(f"  ✅ Копиран файл: {item}")
            copied_count += 1
        except Exception as e:
            print(f"  ❌ Грешка при {item}: {e}")
    else:
        print(f"  ⚠️  Не съществува: {item}")

print(f"\n✅ Копирани {copied_count} от {len(items_to_copy)} елемента")

# 3. HARD RESTART на Passenger
print("\n3. HARD RESTART НА PASSENGER...")
print("-" * 70)

# Method 1: Modify passenger_wsgi.py timestamp (forces reload)
passenger_file = '/home/bghranac/public_html/passenger_wsgi.py'
try:
    # Touch the file to update its timestamp
    os.utime(passenger_file, None)
    print(f"✅ Updated passenger_wsgi.py timestamp")
except Exception as e:
    print(f"⚠️  Couldn't update passenger_wsgi.py: {e}")

# Method 2: Touch tmp/restart.txt (graceful restart)
restart_file = '/home/bghranac/public_html/tmp/restart.txt'
os.makedirs('/home/bghranac/public_html/tmp', exist_ok=True)
try:
    open(restart_file, 'a').close()
    os.utime(restart_file, None)
    print(f"✅ Created/updated tmp/restart.txt")
except Exception as e:
    print(f"⚠️  Couldn't update restart.txt: {e}")

# Method 3: Modify a dummy comment in passenger_wsgi.py to force full reload
try:
    with open(passenger_file, 'r') as f:
        content = f.read()
    
    # Add timestamp comment
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_content = f"# Last restart: {timestamp}\n" + content
    
    with open(passenger_file, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Modified passenger_wsgi.py content (forced full reload)")
    print(f"   Timestamp: {timestamp}")
except Exception as e:
    print(f"⚠️  Couldn't modify passenger_wsgi.py: {e}")

# 4. VERIFY
print("\n4. ВЕРИФИКАЦИЯ...")
print("-" * 70)

# Check if key files exist in public_html
key_files = [
    'catalog/templates/socialaccount/facebook/login.html',
    'catalog/templates/socialaccount/google/login.html',
]

for file in key_files:
    full_path = os.path.join(dest, file)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        print(f"  ✅ {file} ({size} bytes)")
    else:
        print(f"  ❌ ЛИПСВА: {file}")

print("\n" + "=" * 70)
print("✅ UPDATE ЗАВЪРШЕН!")
print("=" * 70)
print("\nИзчакай 5-10 секунди и тествай сайта:")
print("  1. https://bghrana.com/accounts/facebook/login/")
print("       → трябва да показва 'Вход с Facebook' (не Google)")
print("  2. Кликни бутона → трябва да redirect-ва към facebook.com")
print("\nАко пак не работи, проблемът е в Passenger cache - трябва")
print("STOP/START от cPanel Setup Python App.")
print("=" * 70)
