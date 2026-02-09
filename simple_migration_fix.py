#!/usr/bin/env python
"""
По-опростен fix - само приложи migration 0009
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.db import connection

print("=" * 60)
print("🔧 Прост Migration Fix")
print("=" * 60)

try:
    # Директно добави колоната в базата ако не съществува
    with connection.cursor() as cursor:
        print("\n1️⃣ Проверка дали колоната expiry_reminder_sent съществува...")
        
        # Провери дали колоната съществува
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'catalog_product' 
            AND COLUMN_NAME = 'expiry_reminder_sent'
        """)
        
        exists = cursor.fetchone()[0] > 0
        
        if exists:
            print("✅ Колоната вече съществува - нищо за правене!")
        else:
            print("📝 Колоната не съществува - добавяне...")
            cursor.execute("""
                ALTER TABLE catalog_product 
                ADD COLUMN expiry_reminder_sent TINYINT(1) NOT NULL DEFAULT 0
            """)
            print("✅ Колоната expiry_reminder_sent е добавена!")
        
        # Маркирай migration като applied
        print("\n2️⃣ Маркиране на migration 0009 като applied...")
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied) 
            VALUES ('catalog', '0009_product_expiry_reminder_sent', NOW())
            ON DUPLICATE KEY UPDATE applied = NOW()
        """)
        print("✅ Migration 0009 е маркирана като applied!")
    
    print("\n" + "=" * 60)
    print("✅ Готово! Системата е готова за работа!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ГРЕШКА: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
