#!/usr/bin/env python3
"""
Финален скрипт - попълва slug-овете на категориите
"""
import os
import django
from django.utils.text import slugify
import subprocess
import sys

# Инсталирай unidecode ако го няма
try:
    from unidecode import unidecode
except ImportError:
    print("📦 Инсталиране на unidecode...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'unidecode'])
    from unidecode import unidecode

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Category

print("🔧 Попълване на slug-ове за категориите...")

categories = Category.objects.filter(slug__isnull=True) | Category.objects.filter(slug='')

for category in categories:
    # Транслитерация на кирилица към латиница
    name_latin = unidecode(category.name)
    slug_base = slugify(name_latin)
    slug = slug_base
    counter = 1
    
    # Проверка за уникалност
    while Category.objects.filter(slug=slug).exclude(id=category.id).exists():
        slug = f"{slug_base}-{counter}"
        counter += 1
    
    category.slug = slug
    category.save()
    print(f"  ✅ {category.name} -> {slug}")

print("\n✅ Всички категории имат slug-ове!")
