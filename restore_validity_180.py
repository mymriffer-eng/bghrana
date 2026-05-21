#!/usr/bin/env python
"""
Връщане на validity_period на 180 дни за всички обяви с 30 дни
"""
import os
import sys
import django

BASE_DIR = '/home/bghranac/public_html'
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Product

print("=" * 60)
print("ВРЪЩАНЕ НА VALIDITY_PERIOD НА 180 ДНИ")
print("=" * 60)

# Намери всички обяви с validity_period=30
products_30 = Product.objects.filter(validity_period=30)
count = products_30.count()

print(f"\nНамерени обяви с validity_period=30: {count}")

if count > 0:
    print("\nВръщам ги на 180 дни (6 месеца)...")
    
    # Покажи първите 5
    print("\nПримерни обяви:")
    for p in products_30[:5]:
        print(f"  ID: {p.id}, Заглавие: {p.title[:50]}, Създадена: {p.created_at.date()}")
    
    # Update
    products_30.update(validity_period=180)
    print(f"\n✅ Обновени {count} обяви на 180 дни")
else:
    print("\n✅ Няма обяви с validity_period=30")

# Проверка
print("\n" + "-" * 60)
print("Текуща статистика:")
for days, label in Product.VALIDITY_CHOICES:
    count = Product.objects.filter(validity_period=days).count()
    print(f"  {label} ({days} дни): {count} обяви")

# Рестартирай Passenger
print("\n" + "-" * 60)
tmp_dir = os.path.join(BASE_DIR, 'tmp')
os.makedirs(tmp_dir, exist_ok=True)
restart_file = os.path.join(tmp_dir, 'restart.txt')

with open(restart_file, 'w') as f:
    f.write('restart')

print(f"✅ Създаден {restart_file}")

print("\n" + "=" * 60)
print("✅ ГОТОВО!")
print("=" * 60)
print("\nРезултат:")
print("  • Старите обяви са върнати на 180 дни (6 месеца)")
print("  • Новите обяви ще имат default 1 месец в ФОРМАТА")
print("  • Клиентът може да избере 1 седмица / 1 месец / 6 месеца")
print("\nИзчакай 30-60 секунди за Passenger restart.")
print("=" * 60)
