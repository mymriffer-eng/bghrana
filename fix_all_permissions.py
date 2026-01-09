#!/usr/bin/env python
import os
import subprocess

print("Checking and fixing all permissions...")
print("=" * 60)

base_dir = '/home/bghranac/repositories/bghrana'

# Check current permissions and ownership
print(f"\nChecking: {base_dir}/Passengerfile.json")
try:
    stat_info = os.stat(f'{base_dir}/Passengerfile.json')
    print(f"  Current permissions: {oct(stat_info.st_mode)[-3:]}")
    print(f"  Owner UID: {stat_info.st_uid}")
    print(f"  Group GID: {stat_info.st_gid}")
except Exception as e:
    print(f"  Error: {e}")

print(f"\nChecking: {base_dir}")
try:
    stat_info = os.stat(base_dir)
    print(f"  Current permissions: {oct(stat_info.st_mode)[-3:]}")
    print(f"  Owner UID: {stat_info.st_uid}")
    print(f"  Group GID: {stat_info.st_gid}")
except Exception as e:
    print(f"  Error: {e}")

# Try to fix permissions recursively
print("\n" + "=" * 60)
print("Attempting to fix permissions...")

try:
    # Set directory permissions
    for root, dirs, files in os.walk(base_dir):
        # Set directory to 755
        try:
            os.chmod(root, 0o755)
        except:
            pass
        
        # Set files to 644
        for file in files:
            filepath = os.path.join(root, file)
            try:
                if file.endswith('.py') or file == 'manage.py':
                    os.chmod(filepath, 0o755)
                else:
                    os.chmod(filepath, 0o644)
            except:
                pass
    
    print("✓ Permissions updated")
except Exception as e:
    print(f"✗ Error: {e}")

# Special handling for critical files
critical_files = [
    'Passengerfile.json',
    'passenger_wsgi.py',
    'manage.py'
]

print("\nSetting critical files to 755...")
for filename in critical_files:
    filepath = f'{base_dir}/{filename}'
    try:
        os.chmod(filepath, 0o755)
        print(f"✓ {filename}: 755")
    except Exception as e:
        print(f"✗ {filename}: {e}")

print("=" * 60)
print("Done! Now restart the Python App.")
