#!/usr/bin/env python
"""
Промяна на default validity_period от 180 на 30 дни
"""
import os
import sys
import django

BASE_DIR = '/home/bghranac/public_html'
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

print("=" * 60)
print("UPDATE VALIDITY_PERIOD DEFAULT: 180 -> 30")
print("=" * 60)

# 1. Промени default в базата данни
print("\n1. Променяне на DEFAULT в MySQL колоната...")
print("-" * 60)

from django.db import connection

with connection.cursor() as cursor:
    # Провери текуща структура
    cursor.execute("SHOW CREATE TABLE catalog_product")
    create_table = cursor.fetchone()[1]
    
    if 'DEFAULT 180' in create_table:
        print("✓ Намерен DEFAULT 180, променям на DEFAULT 30...")
        
        # Промени default
        cursor.execute("""
            ALTER TABLE catalog_product 
            MODIFY COLUMN validity_period INT NOT NULL DEFAULT 30
        """)
        print("✅ Променен DEFAULT на 30 в MySQL колоната")
    elif 'DEFAULT 30' in create_table:
        print("✅ DEFAULT вече е 30, няма какво да се прави")
    else:
        print("⚠️  Не може да се определи DEFAULT стойността")

# 2. Обнови съществуващите записи с 180 на 30
print("\n2. Обновяване на съществуващи обяви...")
print("-" * 60)

from catalog.models import Product

products_180 = Product.objects.filter(validity_period=180)
count = products_180.count()

if count > 0:
    print(f"Намерени {count} обяви с validity_period=180")
    print("Обновявам на 30 дни (1 месец)...")
    
    products_180.update(validity_period=30)
    print(f"✅ Обновени {count} обяви")
else:
    print("✅ Няма обяви с validity_period=180")

# 3. Рестартирай Passenger
print("\n3. Рестартиране на Passenger...")
print("-" * 60)

tmp_dir = os.path.join(BASE_DIR, 'tmp')
os.makedirs(tmp_dir, exist_ok=True)
restart_file = os.path.join(tmp_dir, 'restart.txt')

with open(restart_file, 'w') as f:
    f.write('restart')

print(f"✅ Създаден {restart_file}")

print("\n" + "=" * 60)
print("✅ ГОТОВО!")
print("=" * 60)
print("\nВалидността вече е:")
print("  • Падащо меню (dropdown)")
print("  • Default: 1 месец (30 дни)")
print("  • Опции: 1 седмица / 1 месец / 6 месеца")
print("\nИзчакай 30-60 секунди за Passenger restart.")
print("=" * 60)
