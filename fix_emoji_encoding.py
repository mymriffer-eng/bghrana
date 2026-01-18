#!/usr/bin/env python
"""
Проверка и промяна на кодировката на таблиците за поддръжка на емоджи
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
    print("Проверка и промяна на кодировката за поддръжка на емоджи")
    print("=" * 60)
    print()
    
    try:
        with connection.cursor() as cursor:
            # Проверка на текущата кодировка
            print("Стъпка 1: Проверка на таблицата catalog_product...")
            cursor.execute("""
                SELECT CCSA.character_set_name 
                FROM information_schema.`TABLES` T,
                     information_schema.`COLLATION_CHARACTER_SET_APPLICABILITY` CCSA
                WHERE CCSA.collation_name = T.table_collation
                  AND T.table_schema = DATABASE()
                  AND T.table_name = 'catalog_product'
            """)
            result = cursor.fetchone()
            charset = result[0] if result else 'unknown'
            print(f"  Текуща кодировка: {charset}")
            
            if charset != 'utf8mb4':
                print(f"\n  ⚠️ Таблицата използва {charset}, трябва да се промени на utf8mb4")
                print()
                
                # Промяна на кодировката
                print("Стъпка 2: Промяна на кодировката на таблицата...")
                cursor.execute("""
                    ALTER TABLE catalog_product 
                    CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                """)
                print("  ✓ Таблицата е преобразувана в utf8mb4")
                print()
                
                # Промяна на базата данни
                print("Стъпка 3: Промяна на кодировката на базата данни...")
                cursor.execute("SELECT DATABASE()")
                db_name = cursor.fetchone()[0]
                cursor.execute(f"""
                    ALTER DATABASE `{db_name}` 
                    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                """)
                print("  ✓ Базата данни е преобразувана в utf8mb4")
            else:
                print("  ✓ Таблицата вече използва utf8mb4")
            print()
            
            # Проверка на description колоната
            print("Стъпка 4: Проверка на description колоната...")
            cursor.execute("""
                SELECT CHARACTER_SET_NAME, COLLATION_NAME
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'catalog_product'
                  AND COLUMN_NAME = 'description'
            """)
            result = cursor.fetchone()
            if result:
                col_charset, col_collation = result
                print(f"  description: {col_charset} / {col_collation}")
                
                if col_charset != 'utf8mb4':
                    cursor.execute("""
                        ALTER TABLE catalog_product 
                        MODIFY description LONGTEXT 
                        CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                    """)
                    print("  ✓ Колоната description е преобразувана")
            print()
            
        print("=" * 60)
        print("Готово! Сега можеш да използваш емоджи в описанията")
        print("Рестартирай: touch tmp/restart.txt")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Грешка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
