#!/usr/bin/env python
import os
import json

print("Creating Passengerfile.json...")
print("=" * 60)

config = {
    "app_type": "wsgi",
    "startup_file": "passenger_wsgi.py",
    "python": "/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python3.11"
}

filepath = '/home/bghranac/repositories/bghrana/Passengerfile.json'

try:
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Set permissions
    os.chmod(filepath, 0o644)
    
    print(f"✓ Created: {filepath}")
    print(f"✓ Permissions set to 644")
    print("\nFile contents:")
    print(json.dumps(config, indent=2))
except Exception as e:
    print(f"✗ ERROR: {e}")

print("=" * 60)
print("Done! Now restart the Python App.")
