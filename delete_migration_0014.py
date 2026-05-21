#!/usr/bin/env python
"""
Скрипт за изтриване на неуспешна миграция 0014 и нейната база данни запис
"""
import os
import sys
import django
import subprocess

# Задай пътя на Django проекта
BASE_DIR = '/home/bghranac/public_html'
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

# Конфигурирай Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.db import connection

print("Изтриване на неуспешна миграция 0014...")
print("=" * 60)

# 1. Изтрий записа от django_migrations таблицата
print("\n1. Изтриване на запис от django_migrations...")
with connection.cursor() as cursor:
    cursor.execute(
        "SELECT id, app, name FROM django_migrations WHERE app = 'catalog' ORDER BY id DESC LIMIT 5"
    )
    rows = cursor.fetchall()
    print("Последни 5 миграции в catalog:")
    for row in rows:
        print(f"  ID: {row[0]}, App: {row[1]}, Name: {row[2]}")
    
    # Изтрий 0014 ако съществува
    cursor.execute(
        "DELETE FROM django_migrations WHERE app = 'catalog' AND name = '0014_alter_category_seo_description_and_more'"
    )
    deleted = cursor.rowcount
    print(f"\n✅ Изтрити {deleted} записа от django_migrations")

# 2. Изтрий файла на миграцията
migration_file = os.path.join(BASE_DIR, 'catalog', 'migrations', '0014_alter_category_seo_description_and_more.py')
if os.path.exists(migration_file):
    os.remove(migration_file)
    print(f"✅ Изтрит файл: {migration_file}")
else:
    print(f"⚠️  Файлът не съществува: {migration_file}")

# 3. Изтрий .pyc файла ако съществува
pyc_file = migration_file + 'c'
if os.path.exists(pyc_file):
    os.remove(pyc_file)
    print(f"✅ Изтрит .pyc файл")

print("\n" + "=" * 60)
print("Миграция 0014 е изтрита!")
print("\nСледващи стъпки:")
print("1. Стартирай fix_category_seo_data.py за да коригираш данните")
print("2. Стартирай create_validity_migration.py наново")
