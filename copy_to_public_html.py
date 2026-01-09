#!/usr/bin/env python
import os
import shutil
import subprocess

print("=" * 60)
print("Copying Django project to public_html")
print("=" * 60)

source = '/home/bghranac/repositories/bghrana'
dest = '/home/bghranac/public_html'

# Files and directories to copy
items_to_copy = [
    'catalog',
    'products',
    'locale',
    'media',
    'staticfiles',
    'manage.py',
    'passenger_wsgi.py',
    'requirements.txt',
    'pyproject.toml',
    'README.md'
]

print("\nCopying files...")
for item in items_to_copy:
    src_path = os.path.join(source, item)
    dst_path = os.path.join(dest, item)
    
    try:
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                print(f"  ✓ Copied directory: {item}")
            else:
                shutil.copy2(src_path, dst_path)
                print(f"  ✓ Copied file: {item}")
        else:
            print(f"  ⚠ Not found: {item}")
    except Exception as e:
        print(f"  ✗ Error copying {item}: {e}")

# Fix permissions
print("\nFixing permissions...")
try:
    os.chmod(os.path.join(dest, 'manage.py'), 0o755)
    os.chmod(os.path.join(dest, 'passenger_wsgi.py'), 0o755)
    print("  ✓ Set executable permissions")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print("Done! Now:")
print("1. Go to Setup Python App")
print("2. EDIT the existing app (don't delete)")
print("3. Change Application root to: /home/bghranac/public_html")
print("4. Click 'Update'")
print("5. RESTART the app")
print("6. Wait 30 seconds")
print("7. Open https://bghrana.com")
print("=" * 60)
