#!/usr/bin/env python3
"""
Скрипт за маркиране на миграцията като приложена без да я изпълнява
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.core.management import call_command

print("🔧 Маркиране на миграцията като приложена...")

try:
    # Fake migrate - маркира миграцията като приложена без да я изпълнява
    call_command('migrate', 'catalog', '--fake')
    print("✅ Миграцията е маркирана като приложена")
    print("\nСега създаваме чиста миграция само за SEOPage...")
    
except Exception as e:
    print(f"❌ Грешка: {e}")
