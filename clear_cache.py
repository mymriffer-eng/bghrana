#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Clear Python cache and force reload
"""

import os
import shutil

repo_path = '/home/bghranac/repositories/bghrana'

print("=" * 70)
print("CLEARING PYTHON CACHE")
print("=" * 70)

# Find and remove all __pycache__ directories
cache_dirs = []
for root, dirs, files in os.walk(repo_path):
    if '__pycache__' in dirs:
        cache_path = os.path.join(root, '__pycache__')
        cache_dirs.append(cache_path)

print(f"\nFound {len(cache_dirs)} __pycache__ directories")

for cache_dir in cache_dirs:
    try:
        shutil.rmtree(cache_dir)
        print(f"✓ Removed: {cache_dir}")
    except Exception as e:
        print(f"✗ Error removing {cache_dir}: {e}")

# Also remove .pyc files
print("\nRemoving .pyc files...")
pyc_count = 0
for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.pyc'):
            pyc_path = os.path.join(root, file)
            try:
                os.remove(pyc_path)
                pyc_count += 1
            except Exception as e:
                print(f"✗ Error removing {pyc_path}: {e}")

print(f"✓ Removed {pyc_count} .pyc files")

# Touch restart file
restart_file = os.path.join(repo_path, 'tmp', 'restart.txt')
os.makedirs(os.path.dirname(restart_file), exist_ok=True)
with open(restart_file, 'a'):
    os.utime(restart_file, None)

print(f"\n✓ Forced restart via {restart_file}")

print("\n" + "=" * 70)
print("✓ CACHE CLEARED")
print("=" * 70)
print("\nWait 20 seconds, then test: https://bghrana.com/register/")
