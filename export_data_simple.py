"""
Export data from local SQLite database using sqlite3 module
No Django required - pure Python
"""

import sqlite3
import json
import os

db_path = 'db.sqlite3'

if not os.path.exists(db_path):
    print(f"ERROR: {db_path} not found!")
    exit(1)

print("=" * 70)
print("EXPORTING DATA FROM LOCAL DATABASE")
print("=" * 70)

# Connect to SQLite database
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row  # Access columns by name
cursor = conn.cursor()

# Export Categories
print("\n1. Exporting Categories...")
cursor.execute("SELECT id, name, description, parent_id FROM catalog_category ORDER BY id")
categories = []
for row in cursor.fetchall():
    categories.append({
        'id': row['id'],
        'name': row['name'],
        'description': row['description'],
        'parent_id': row['parent_id'],
    })
print(f"✓ Found {len(categories)} categories")

# Export Regions
print("\n2. Exporting Regions...")
cursor.execute("SELECT id, name FROM catalog_region ORDER BY id")
regions = []
for row in cursor.fetchall():
    regions.append({
        'id': row['id'],
        'name': row['name'],
    })
print(f"✓ Found {len(regions)} regions")

# Export Cities
print("\n3. Exporting Cities...")
cursor.execute("SELECT id, name, region_id FROM catalog_city ORDER BY id")
cities = []
for row in cursor.fetchall():
    cities.append({
        'id': row['id'],
        'name': row['name'],
        'region_id': row['region_id'],
    })
print(f"✓ Found {len(cities)} cities")

conn.close()

# Create export data
export_data = {
    'categories': categories,
    'regions': regions,
    'cities': cities,
}

# Save to JSON file
output_file = 'exported_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print(f"\n✓ Data exported to: {output_file}")
print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)
print(f"Categories: {len(categories)}")
print(f"Regions: {len(regions)}")
print(f"Cities: {len(cities)}")
print("\nNEXT STEPS:")
print("1. Upload exported_data.json to /home/bghranac/")
print("2. Run import_data.py on the server")
