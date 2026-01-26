#!/usr/bin/env python
"""
Скрипт за автоматично генериране на slugs за всички области и градове.
Използва unidecode за транслитерация от кирилица към латиница.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Region, City
from django.utils.text import slugify
from unidecode import unidecode


def generate_region_slugs():
    """Генерира slugs за всички области."""
    regions = Region.objects.all()
    updated_count = 0
    
    for region in regions:
        if not region.slug:
            # Транслитерация от кирилица към латиница
            transliterated = unidecode(region.name)
            # Създаване на slug
            slug = slugify(transliterated)
            
            # Проверка за уникалност
            original_slug = slug
            counter = 1
            while Region.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            region.slug = slug
            region.save()
            updated_count += 1
            print(f"✓ Област: {region.name} → {slug}")
    
    return updated_count


def generate_city_slugs():
    """Генерира slugs за всички градове."""
    cities = City.objects.all()
    updated_count = 0
    
    for city in cities:
        if not city.slug:
            # Транслитерация от кирилица към латиница
            transliterated = unidecode(city.name)
            # Създаване на slug
            slug = slugify(transliterated)
            
            # Проверка за уникалност в рамките на областта
            original_slug = slug
            counter = 1
            while City.objects.filter(slug=slug, region=city.region).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            city.slug = slug
            city.save()
            updated_count += 1
            print(f"✓ Град: {city.name} ({city.region.name}) → {slug}")
    
    return updated_count


if __name__ == '__main__':
    print("=" * 60)
    print("Генериране на URL slugs за области и градове")
    print("=" * 60)
    
    print("\n1. Генериране на slugs за области...")
    regions_updated = generate_region_slugs()
    print(f"\n✓ Обновени {regions_updated} области")
    
    print("\n2. Генериране на slugs за градове...")
    cities_updated = generate_city_slugs()
    print(f"\n✓ Обновени {cities_updated} града")
    
    print("\n" + "=" * 60)
    print(f"Готово! Общо обновени: {regions_updated + cities_updated}")
    print("=" * 60)
    
    # Проверка
    regions_without_slug = Region.objects.filter(slug__isnull=True).count()
    cities_without_slug = City.objects.filter(slug__isnull=True).count()
    
    if regions_without_slug > 0 or cities_without_slug > 0:
        print(f"\n⚠️  ВНИМАНИЕ: Остават {regions_without_slug} области и {cities_without_slug} града без slug!")
    else:
        print("\n✓ Всички области и градове имат slugs!")
