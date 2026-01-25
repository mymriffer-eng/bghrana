#!/usr/bin/env python3
"""
Скрипт за генериране на slug-ове за съществуващите категории
"""
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Category

print("🔧 Генериране на slug-ове за категориите...")

categories = Category.objects.all()
for category in categories:
    if not hasattr(category, 'slug') or not category.slug:
        # Транслитерация на българско към латиница за slug
        slug_base = slugify(category.name)
        slug = slug_base
        counter = 1
        
        # Проверка за уникалност
        while Category.objects.filter(slug=slug).exists():
            slug = f"{slug_base}-{counter}"
            counter += 1
        
        print(f"  {category.name} -> {slug}")
        # Ще запишем след миграцията

print("\n✅ Готово! Сега изпълни:")
print("   python manage.py migrate")
print("   python fix_category_slugs_final.py")
