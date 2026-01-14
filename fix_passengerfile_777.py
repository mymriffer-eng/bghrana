#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Fix Passengerfile.json permissions - try 777 as last resort for CloudLinux CageFS
"""

import os
import stat

repo_path = '/home/bghranac/repositories/bghrana'
passenger_file = os.path.join(repo_path, 'Passengerfile.json')

print("=" * 70)
print("FIXING PASSENGERFILE.JSON PERMISSIONS")
print("=" * 70)

# Create Passengerfile.json if missing
if not os.path.exists(passenger_file):
    print(f"\n✓ Creating {passenger_file}")
    content = '''{
  "app_type": "wsgi",
  "startup_file": "passenger_wsgi.py",
  "python": "/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python"
}
'''
    try:
        with open(passenger_file, 'w') as f:
            f.write(content)
        print(f"✓ File created")
    except Exception as e:
        print(f"✗ ERROR creating file: {e}")
        exit(1)
else:
    print(f"\n✓ File exists: {passenger_file}")

# Set 777 permissions
print(f"\nSetting 777 permissions (rwxrwxrwx)...")
try:
    os.chmod(passenger_file, 0o777)
    print(f"✓ Permissions set to 777")
except Exception as e:
    print(f"✗ ERROR setting permissions: {e}")
    exit(1)

# Verify permissions
try:
    file_stat = os.stat(passenger_file)
    mode = stat.filemode(file_stat.st_mode)
    octal = oct(file_stat.st_mode)[-3:]
    print(f"✓ Current permissions: {mode} ({octal})")
    print(f"✓ Owner UID: {file_stat.st_uid}")
    print(f"✓ Group GID: {file_stat.st_gid}")
except Exception as e:
    print(f"✗ ERROR checking permissions: {e}")

# Touch restart file
restart_file = os.path.join(repo_path, 'tmp', 'restart.txt')
os.makedirs(os.path.dirname(restart_file), exist_ok=True)
try:
    with open(restart_file, 'a'):
        os.utime(restart_file, None)
    print(f"\n✓ Touched {restart_file}")
except Exception as e:
    print(f"✗ WARNING: Could not touch restart file: {e}")

print("\n" + "=" * 70)
print("✓ COMPLETE")
print("=" * 70)
print("\nNEXT STEPS:")
print("1. Go to cPanel Python App")
print("2. Click 'RESTART' button")
print("3. Wait 20 seconds")
print("4. Test: https://bghrana.com")
print("\nIf still fails: Contact SuperHosting.BG support about CloudLinux CageFS")
