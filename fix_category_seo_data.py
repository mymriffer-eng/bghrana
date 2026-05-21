#!/usr/bin/env python
"""
Скрипт за коригиране на прекалено дълги SEO полета в Category модела
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

print("Коригиране на дълги SEO полета в категории...")
print("=" * 60)

# Намери всички категории
categories = Category.objects.all()
fixed_count = 0

for cat in categories:
    modified = False
    
    # Провери seo_title (макс 60 символа)
    if cat.seo_title and len(cat.seo_title) > 60:
        print(f"\nКатегория: {cat.name} (ID: {cat.id})")
        print(f"  Стар seo_title ({len(cat.seo_title)} символа):")
        print(f"    {cat.seo_title}")
        
        cat.seo_title = cat.seo_title[:60]
        print(f"  Нов seo_title (60 символа):")
        print(f"    {cat.seo_title}")
        modified = True
    
    # Провери seo_description (макс 160 символа)
    if cat.seo_description and len(cat.seo_description) > 160:
        print(f"\nКатегория: {cat.name} (ID: {cat.id})")
        print(f"  Стар seo_description ({len(cat.seo_description)} символа):")
        print(f"    {cat.seo_description[:80]}...")
        
        cat.seo_description = cat.seo_description[:160]
        print(f"  Нов seo_description (160 символа):")
        print(f"    {cat.seo_description}")
        modified = True
    
    if modified:
        cat.save()
        fixed_count += 1
        print(f"  ✅ Категорията е записана")

print("\n" + "=" * 60)
print(f"Коригирани категории: {fixed_count}")
print("Готово!")
