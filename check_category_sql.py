#!/usr/bin/env python
"""
Директна SQL проверка на Category seo полета
"""
import os
import sys
import django

# Задай пътя на Django проекта
BASE_DIR = '/home/bghranac/public_html'
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

# Конфигурирай Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.db import connection

print("SQL проверка на catalog_category таблица...")
print("=" * 60)

with connection.cursor() as cursor:
    # Проверка на структурата на таблицата
    cursor.execute("DESCRIBE catalog_category")
    print("\nСтруктура на catalog_category:")
    print("-" * 60)
    for row in cursor.fetchall():
        if 'seo' in row[0]:
            print(f"  {row[0]}: {row[1]}")
    
    # Провери дължината на seo_title полета
    cursor.execute("""
        SELECT id, name, 
               CHAR_LENGTH(seo_title) as title_len,
               CHAR_LENGTH(seo_description) as desc_len,
               seo_title
        FROM catalog_category 
        WHERE CHAR_LENGTH(seo_title) > 60 
           OR CHAR_LENGTH(seo_description) > 160
        ORDER BY id
    """)
    
    rows = cursor.fetchall()
    
    print(f"\n\nКатегории с дълги SEO полета: {len(rows)}")
    print("-" * 60)
    
    if rows:
        for row in rows:
            print(f"\nID: {row[0]}")
            print(f"  Име: {row[1]}")
            print(f"  seo_title дължина: {row[2]} символа")
            print(f"  seo_description дължина: {row[3]} символа")
            if row[2] > 60:
                print(f"  seo_title текст: {row[4][:100]}...")
    else:
        print("Няма проблемни категории!")
    
    # Виж ред 9
    print("\n" + "=" * 60)
    print("Проверка на ред 9:")
    cursor.execute("""
        SELECT id, name, 
               CHAR_LENGTH(seo_title) as title_len,
               seo_title
        FROM catalog_category 
        ORDER BY id
        LIMIT 8, 1
    """)
    row = cursor.fetchone()
    if row:
        print(f"  ID: {row[0]}, Име: {row[1]}")
        print(f"  seo_title дължина: {row[2]} символа")
        print(f"  seo_title: {row[3]}")

print("\n" + "=" * 60)
print("Готово!")
