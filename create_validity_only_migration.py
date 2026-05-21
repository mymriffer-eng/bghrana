#!/usr/bin/env python
"""
Създаване на ръчна миграция САМО за validity_period полето
"""
import os
import sys

BASE_DIR = '/home/bghranac/public_html'
os.chdir(BASE_DIR)

print("=" * 60)
print("СЪЗДАВАНЕ НА РЪЧНА МИГРАЦИЯ ЗА VALIDITY_PERIOD")
print("=" * 60)

# 1. Изтрий миграция 0014 ако съществува
print("\n1. Изтриване на миграция 0014...")
print("-" * 60)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute(
        "DELETE FROM django_migrations WHERE app = 'catalog' AND name = '0014_alter_category_seo_description_and_more'"
    )
    deleted = cursor.rowcount
    print(f"✅ Изтрити {deleted} записа от django_migrations")

migration_file_0014 = os.path.join(BASE_DIR, 'catalog', 'migrations', '0014_alter_category_seo_description_and_more.py')
if os.path.exists(migration_file_0014):
    os.remove(migration_file_0014)
    print(f"✅ Изтрит файл 0014")

# 2. Създай ръчна миграция само за validity_period
print("\n2. Създаване на ръчна миграция 0014_product_validity_period.py...")
print("-" * 60)

migration_content = """# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20250124_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='validity_period',
            field=models.IntegerField(
                choices=[(7, '1 седмица'), (30, '1 месец'), (180, '6 месеца')],
                default=180,
                verbose_name='Валидност на обявата'
            ),
        ),
    ]
"""

# Намери последната миграция за dependencies
migrations_dir = os.path.join(BASE_DIR, 'catalog', 'migrations')
migration_files = [f for f in os.listdir(migrations_dir) if f.startswith('00') and f.endswith('.py')]
migration_files.sort()
last_migration = migration_files[-1].replace('.py', '') if migration_files else '0001_initial'

print(f"Последна миграция: {last_migration}")

# Обнови dependencies
migration_content = migration_content.replace('0013_auto_20250124_1234', last_migration)

# Запиши новата миграция
new_migration_file = os.path.join(migrations_dir, '0014_product_validity_period.py')
with open(new_migration_file, 'w', encoding='utf-8') as f:
    f.write(migration_content)

print(f"✅ Създадена: {new_migration_file}")

# 3. Приложи миграцията
print("\n3. Прилагане на миграцията...")
print("-" * 60)

import subprocess

result = subprocess.run(
    ['python', 'manage.py', 'migrate', 'catalog'],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

if result.returncode == 0:
    print("\n✅ Миграцията е приложена успешно!")
    
    # 4. Рестартирай Passenger
    print("\n4. Рестартиране на Passenger...")
    print("-" * 60)
    
    tmp_dir = os.path.join(BASE_DIR, 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    restart_file = os.path.join(tmp_dir, 'restart.txt')
    
    with open(restart_file, 'w') as f:
        f.write('restart')
    
    print(f"✅ Създаден {restart_file}")
    print("\n" + "=" * 60)
    print("✅ ГОТОВО! Изчакай 30-60 секунди за Passenger restart.")
    print("=" * 60)
else:
    print("\n❌ ГРЕШКА при прилагане на миграцията!")
    print("=" * 60)
    sys.exit(1)
