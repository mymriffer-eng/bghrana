#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Restore .htaccess from backup and use simpler configuration
"""

import os
import shutil

htaccess_path = '/home/bghranac/public_html/.htaccess'
backup_path = htaccess_path + '.backup'

print("=" * 70)
print("RESTORING .htaccess FROM BACKUP")
print("=" * 70)

# Restore from backup
if os.path.exists(backup_path):
    shutil.copy2(backup_path, htaccess_path)
    print(f"✓ Restored .htaccess from backup")
else:
    print(f"✗ Backup not found at {backup_path}")

print("\n" + "=" * 70)
print("CURRENT .htaccess CONTENT:")
print("=" * 70)

if os.path.exists(htaccess_path):
    with open(htaccess_path, 'r') as f:
        content = f.read()
    print(content)
else:
    print("File does not exist")

print("\n" + "=" * 70)
print("✓ COMPLETE")
print("=" * 70)
print("\nNEXT STEPS:")
print("1. Restart Python App")
print("2. Test if site works again: https://bghrana.com")
print("3. We'll use a different approach for media files")
