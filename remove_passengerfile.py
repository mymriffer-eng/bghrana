#!/usr/bin/env python
import os

print("Removing Passengerfile.json...")
print("=" * 60)

filepath = '/home/bghranac/repositories/bghrana/Passengerfile.json'

try:
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"✓ Removed: {filepath}")
        print("\nPassengerfile.json is not needed.")
        print("cPanel Python App uses its own configuration.")
    else:
        print(f"File doesn't exist: {filepath}")
except Exception as e:
    print(f"✗ Error: {e}")

print("=" * 60)
print("Now restart the Python App.")
print("\nThe app should work without Passengerfile.json")
print("using the cPanel Python App interface settings.")
