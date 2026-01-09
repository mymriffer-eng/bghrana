#!/usr/bin/env python
import os

print("=" * 60)
print("Setting 777 permissions on Passengerfile.json")
print("=" * 60)

passenger_file = '/home/bghranac/repositories/bghrana/Passengerfile.json'

try:
    if os.path.exists(passenger_file):
        # Set 777 (rwxrwxrwx)
        os.chmod(passenger_file, 0o777)
        
        # Verify
        stat = os.stat(passenger_file)
        perms = oct(stat.st_mode)[-3:]
        
        print(f"✓ Set permissions to: {perms}")
        print(f"  Owner: {stat.st_uid}")
        print(f"  Group: {stat.st_gid}")
        print(f"  Size: {stat.st_size} bytes")
        
        # Force restart
        restart_file = '/home/bghranac/repositories/bghrana/tmp/restart.txt'
        with open(restart_file, 'w') as f:
            f.write('restart\n')
        print(f"✓ Created restart trigger")
        
    else:
        print("✗ Passengerfile.json not found!")
        print("  Creating it now...")
        
        import json
        config = {
            "app_type": "wsgi",
            "startup_file": "passenger_wsgi.py",
            "python": "/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python"
        }
        
        with open(passenger_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        os.chmod(passenger_file, 0o777)
        print("✓ Created and set to 777")
        
except Exception as e:
    print(f"✗ Error: {e}")

print("=" * 60)
print("Now:")
print("1. Wait 15 seconds")
print("2. RESTART Python App")
print("3. Wait 20 seconds")
print("4. Open https://bghrana.com")
print("=" * 60)
