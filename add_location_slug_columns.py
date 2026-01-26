#!/usr/bin/env python
"""
Директно добавяне на slug колони към таблиците catalog_region и catalog_city.
Използвай само ако Django migrations не работят правилно.
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.db import connection

def add_location_slug_columns():
    """Добавя slug колони към catalog_region и catalog_city ако не съществуват."""
    with connection.cursor() as cursor:
        # Проверка и добавяне на slug към catalog_region
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'catalog_region' 
            AND COLUMN_NAME = 'slug'
        """)
        
        region_has_slug = cursor.fetchone()[0] > 0
        
        if not region_has_slug:
            print("Добавяне на slug колона към catalog_region...")
            cursor.execute("""
                ALTER TABLE catalog_region 
                ADD COLUMN slug VARCHAR(100) NULL UNIQUE
                AFTER name
            """)
            print("✓ Slug колона добавена към catalog_region")
        else:
            print("✓ catalog_region вече има slug колона")
        
        # Проверка и добавяне на slug към catalog_city
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'catalog_city' 
            AND COLUMN_NAME = 'slug'
        """)
        
        city_has_slug = cursor.fetchone()[0] > 0
        
        if not city_has_slug:
            print("Добавяне на slug колона към catalog_city...")
            cursor.execute("""
                ALTER TABLE catalog_city 
                ADD COLUMN slug VARCHAR(100) NULL
                AFTER name
            """)
            print("✓ Slug колона добавена към catalog_city")
        else:
            print("✓ catalog_city вече има slug колона")
    
    print("\n✓ Всички промени са завършени!")

if __name__ == '__main__':
    print("=" * 60)
    print("Добавяне на slug колони към локации")
    print("=" * 60)
    add_location_slug_columns()
