#!/usr/bin/env python
"""
Fix migration conflicts - приложи само нова migration 0009
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.core.management import call_command

print("=" * 60)
print("🔧 Fix Migration Conflicts")
print("=" * 60)

try:
    # Маркирай всички съществуващи migrations като applied (fake)
    print("\n1️⃣ Маркиране на съществуващи migrations като applied...")
    call_command('migrate', 'catalog', '0008', '--fake')
    print("✅ Migration 0008 маркирана като applied")
    
    # Сега приложи само новата migration 0009
    print("\n2️⃣ Прилагане на нова migration 0009...")
    call_command('migrate', 'catalog', '0009')
    print("✅ Migration 0009 приложена успешно!")
    
    print("\n" + "=" * 60)
    print("✅ Всички migrations са в синхрон!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ГРЕШКА: {str(e)}")
    print("\n📝 Ръчно решение:")
    print("1. Влез в сървъра")
    print("2. Изпълни: python manage.py migrate catalog 0009 --fake")
    print("=" * 60)
    sys.exit(1)
