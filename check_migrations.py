#!/usr/bin/env python
"""
Проверка на наличните миграции в catalog app
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.db.migrations.recorder import MigrationRecorder

print("=" * 70)
print("ПРИЛОЖЕНИ МИГРАЦИИ В БАЗАТА ДАННИ")
print("=" * 70)

migrations = MigrationRecorder.Migration.objects.filter(app='catalog').order_by('id')

for migration in migrations:
    print(f"✓ {migration.name}")

print("\n" + "=" * 70)
print("ФАЙЛОВЕ С МИГРАЦИИ В ПАПКАТА")
print("=" * 70)

migrations_dir = 'catalog/migrations'
files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py'])

for f in files:
    print(f"  {f}")

print("\n" + "=" * 70)
print("ПОСЛЕДНА ПРИЛОЖЕНА МИГРАЦИЯ:")
if migrations.exists():
    last = migrations.last()
    print(f"  {last.name}")
else:
    print("  Няма приложени миграции")
print("=" * 70)
