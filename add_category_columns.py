#!/usr/bin/env python3
"""
Добавя slug колоната директно в базата данни
"""
import os
import django
import pymysql

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.conf import settings

print("🔧 Добавяне на slug колона в catalog_category...")

# Връзка към базата данни
db_settings = settings.DATABASES['default']
connection = pymysql.connect(
    host=db_settings['HOST'],
    user=db_settings['USER'],
    password=db_settings['PASSWORD'],
    database=db_settings['NAME'],
    charset='utf8mb4'
)

try:
    with connection.cursor() as cursor:
        # Добави slug колоната
        sql = """
        ALTER TABLE catalog_category 
        ADD COLUMN slug VARCHAR(100) NULL,
        ADD COLUMN seo_title VARCHAR(60) NULL,
        ADD COLUMN seo_description TEXT NULL,
        ADD COLUMN seo_text LONGTEXT NULL
        """
        cursor.execute(sql)
        connection.commit()
        print("✅ Колоните са добавени успешно!")
        
        # Добави индекс за slug
        sql_index = "ALTER TABLE catalog_category ADD UNIQUE INDEX catalog_category_slug (slug)"
        cursor.execute(sql_index)
        connection.commit()
        print("✅ Индексът е създаден!")
        
except pymysql.err.OperationalError as e:
    if '1060' in str(e):  # Duplicate column
        print("⚠️ Колоните вече съществуват")
    else:
        raise
finally:
    connection.close()

print("\nСега изпълни: python populate_category_slugs.py")
