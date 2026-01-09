#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Import data from exported_data.json to production MySQL database
"""

import os
import sys
import django
import json

# Setup Django
repo_path = '/home/bghranac/repositories/bghrana'
sys.path.insert(0, repo_path)
os.chdir(repo_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Category, Region, City

print("=" * 70)
print("IMPORTING DATA TO PRODUCTION DATABASE")
print("=" * 70)

# Read JSON file
json_file = os.path.join(repo_path, 'exported_data.json')
if not os.path.exists(json_file):
    print(f"✗ ERROR: {json_file} not found!")
    print("Please make sure exported_data.json is in the repository")
    exit(1)

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"\n✓ Loaded data from {json_file}")
print(f"  Categories: {len(data['categories'])}")
print(f"  Regions: {len(data['regions'])}")
print(f"  Cities: {len(data['cities'])}")

# Import Regions first (no dependencies)
print("\n1. Importing Regions...")
regions_created = 0
regions_skipped = 0

for region_data in data['regions']:
    region, created = Region.objects.get_or_create(
        id=region_data['id'],
        defaults={'name': region_data['name']}
    )
    if created:
        regions_created += 1
    else:
        regions_skipped += 1

print(f"✓ Created: {regions_created}, Skipped (already exist): {regions_skipped}")

# Import Categories (handle parent relationships)
print("\n2. Importing Categories...")
categories_created = 0
categories_skipped = 0

# First pass - create all categories without parent
for cat_data in data['categories']:
    cat, created = Category.objects.get_or_create(
        id=cat_data['id'],
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description'],
        }
    )
    if created:
        categories_created += 1
    else:
        categories_skipped += 1

# Second pass - set parent relationships
for cat_data in data['categories']:
    if cat_data['parent_id']:
        try:
            cat = Category.objects.get(id=cat_data['id'])
            cat.parent_id = cat_data['parent_id']
            cat.save(update_fields=['parent'])
        except Exception as e:
            print(f"  Warning: Could not set parent for category {cat_data['id']}: {e}")

print(f"✓ Created: {categories_created}, Skipped (already exist): {categories_skipped}")

# Import Cities
print("\n3. Importing Cities...")
cities_created = 0
cities_skipped = 0

for city_data in data['cities']:
    try:
        city, created = City.objects.get_or_create(
            id=city_data['id'],
            defaults={
                'name': city_data['name'],
                'region_id': city_data['region_id']
            }
        )
        if created:
            cities_created += 1
        else:
            cities_skipped += 1
    except Exception as e:
        print(f"  Warning: Could not create city {city_data['name']}: {e}")

print(f"✓ Created: {cities_created}, Skipped (already exist): {cities_skipped}")

print("\n" + "=" * 70)
print("✓ IMPORT COMPLETE")
print("=" * 70)
print(f"\nTotal imported:")
print(f"  Regions: {regions_created}")
print(f"  Categories: {categories_created}")
print(f"  Cities: {cities_created}")
print("\nYou can now use these in your products!")
