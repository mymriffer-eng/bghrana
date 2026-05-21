#!/usr/bin/env python
"""
Скрипт за проверка на данните в Category seo полетата
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

from catalog.models import Category

print("Проверка на Category seo полета...")
print("=" * 60)

# Намери всички категории с дълги seo_title полета
categories = Category.objects.all()

print(f"\nОбщо категории: {categories.count()}")
print("\nКатегории с дълги SEO полета:")
print("-" * 60)

for i, cat in enumerate(categories, 1):
    seo_title_len = len(cat.seo_title) if cat.seo_title else 0
    seo_desc_len = len(cat.seo_description) if cat.seo_description else 0
    
    if seo_title_len > 60 or seo_desc_len > 160:
        print(f"\nКатегория #{i} (ID: {cat.id}): {cat.name}")
        
        if seo_title_len > 60:
            print(f"  ❌ seo_title: {seo_title_len} символа (макс: 60)")
            print(f"     Текст: {cat.seo_title[:80]}...")
        else:
            print(f"  ✅ seo_title: {seo_title_len} символа")
            
        if seo_desc_len > 160:
            print(f"  ❌ seo_description: {seo_desc_len} символа (макс: 160)")
            print(f"     Текст: {cat.seo_description[:80]}...")
        else:
            print(f"  ✅ seo_description: {seo_desc_len} символа")

print("\n" + "=" * 60)
print("Проверката завърши.")
