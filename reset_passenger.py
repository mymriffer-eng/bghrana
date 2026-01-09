#!/usr/bin/env python
import os
import json
import subprocess

print("Complete Passenger reset...")
print("=" * 60)

base = '/home/bghranac/repositories/bghrana'

# Step 1: Remove any existing Passengerfile
passenger_file = f'{base}/Passengerfile.json'
if os.path.exists(passenger_file):
    os.remove(passenger_file)
    print("✓ Removed old Passengerfile.json")

# Step 2: Touch restart file
restart_file = f'{base}/tmp/restart.txt'
os.makedirs(f'{base}/tmp', exist_ok=True)
with open(restart_file, 'w') as f:
    f.write('restart\n')
os.chmod(restart_file, 0o644)
print("✓ Created tmp/restart.txt")

# Step 3: Wait a moment
import time
time.sleep(2)

# Step 4: Create NEW Passengerfile with world-readable permissions
config = {
    "app_type": "wsgi",
    "startup_file": "passenger_wsgi.py",
    "python": "/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python3.11"
}

# Write with immediate chmod
with open(passenger_file, 'w') as f:
    json.dump(config, f, indent=2)

# Make it world-readable (777 just for testing)
os.chmod(passenger_file, 0o777)
print(f"✓ Created new Passengerfile.json with 777 permissions")

# Verify
stat = os.stat(passenger_file)
print(f"  Permissions: {oct(stat.st_mode)[-3:]}")
print(f"  Size: {stat.st_size} bytes")

print("=" * 60)
print("IMPORTANT: Now you MUST:")
print("1. Wait 30 seconds")
print("2. Go to Setup Python App")
print("3. Click 'Stop App'")
print("4. Wait 10 seconds")
print("5. Click 'Start App'")
print("6. Try accessing the site")
