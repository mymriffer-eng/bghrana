#!/usr/bin/env python
"""
Синхронизиране на миграциите - маркира съществуващи полета
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.db import connection

def main():
    print("=" * 60)
    print("Синхронизиране на миграциите")
    print("=" * 60)
    print()
    
    try:
        # Изтриваме конфликтни миграции
        import glob
        print("Стъпка 1: Почистване на конфликтни миграции...")
        for pattern in ['catalog/migrations/0009_*.py', 'catalog/migrations/__pycache__/0009_*.pyc']:
            files = glob.glob(pattern)
            for file in files:
                try:
                    os.remove(file)
                    print(f"  Изтрит: {file}")
                except:
                    pass
        print()
        
        # Проверка на базата
        print("Стъпка 2: Проверка на базата данни...")
        with connection.cursor() as cursor:
            cursor.execute("SHOW COLUMNS FROM catalog_product")
            columns = [row[0] for row in cursor.fetchall()]
            
            has_seller = 'seller_type' in columns
            has_sells = 'sells_to' in columns
            
            print(f"  seller_type: {'✓' if has_seller else '✗'}")
            print(f"  sells_to: {'✓' if has_sells else '✗'}")
        print()
        
        # Маркиране на миграция ако полетата съществуват
        if has_seller and has_sells:
            print("Стъпка 3: Маркиране на миграция...")
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM django_migrations 
                    WHERE app = 'catalog' AND name LIKE '0009_%'
                """)
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('catalog', '0009_product_fields', NOW())
                """)
                print("  ✓ Миграция маркирана")
        print()
        
        print("=" * 60)
        print("Готово! Рестартирай: touch tmp/restart.txt")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Грешка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
