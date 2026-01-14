#!/usr/bin/env python
"""
Export data from local SQLite database to JSON
Run this locally on your Windows machine
"""

import os
import sys
import django
import json

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Category, Region, City

print("=" * 70)
print("EXPORTING DATA FROM LOCAL DATABASE")
print("=" * 70)

# Export Categories
print("\n1. Exporting Categories...")
categories = Category.objects.all().order_by('id')
categories_data = []

for cat in categories:
    categories_data.append({
        'id': cat.id,
        'name': cat.name,
        'description': cat.description,
        'parent_id': cat.parent_id,
    })

print(f"✓ Found {len(categories_data)} categories")

# Export Regions
print("\n2. Exporting Regions...")
regions = Region.objects.all().order_by('id')
regions_data = []

for region in regions:
    regions_data.append({
        'id': region.id,
        'name': region.name,
    })

print(f"✓ Found {len(regions_data)} regions")

# Export Cities
print("\n3. Exporting Cities...")
cities = City.objects.all().order_by('id')
cities_data = []

for city in cities:
    cities_data.append({
        'id': city.id,
        'name': city.name,
        'region_id': city.region_id,
    })

print(f"✓ Found {len(cities_data)} cities")

# Create export data
export_data = {
    'categories': categories_data,
    'regions': regions_data,
    'cities': cities_data,
}

# Save to JSON file
output_file = 'exported_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print(f"\n✓ Data exported to: {output_file}")
print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)
print(f"Categories: {len(categories_data)}")
print(f"Regions: {len(regions_data)}")
print(f"Cities: {len(cities_data)}")
print("\nNEXT STEPS:")
print("1. Upload exported_data.json to /home/bghranac/")
print("2. Run import_data.py on the server")
