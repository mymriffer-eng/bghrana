#!/usr/bin/env python
import os
import subprocess

print("Fixing file permissions...")
print("=" * 60)

files_to_fix = [
    '/home/bghranac/repositories/bghrana/Passengerfile.json',
    '/home/bghranac/repositories/bghrana/passenger_wsgi.py',
    '/home/bghranac/repositories/bghrana/manage.py'
]

for filepath in files_to_fix:
    if os.path.exists(filepath):
        try:
            os.chmod(filepath, 0o644)
            print(f"✓ Fixed permissions for: {filepath}")
        except Exception as e:
            print(f"✗ Error fixing {filepath}: {e}")
    else:
        print(f"⚠ File not found: {filepath}")

# Fix directory
try:
    os.chmod('/home/bghranac/repositories/bghrana', 0o755)
    print(f"✓ Fixed permissions for directory")
except Exception as e:
    print(f"✗ Error fixing directory: {e}")

print("=" * 60)
print("Done! Now restart the Python App.")
