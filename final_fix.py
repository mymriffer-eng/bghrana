#!/usr/bin/env python
import os
import sys

print("=" * 60)
print("FINAL FIX: Removing Passengerfile.json permanently")
print("=" * 60)

base = '/home/bghranac/repositories/bghrana'
passenger_file = f'{base}/Passengerfile.json'

# Remove the file
try:
    if os.path.exists(passenger_file):
        os.remove(passenger_file)
        print(f"✓ Deleted: {passenger_file}")
    else:
        print(f"✓ File already doesn't exist")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Create restart file
try:
    restart_file = f'{base}/tmp/restart.txt'
    os.makedirs(f'{base}/tmp', exist_ok=True)
    with open(restart_file, 'w') as f:
        f.write('force-restart\n')
    print(f"✓ Created restart trigger")
except Exception as e:
    print(f"⚠ Warning: {e}")

print("=" * 60)
print("NEXT STEPS IN CPANEL:")
print("=" * 60)
print("1. Go to 'Setup Python App'")
print("2. Make sure these are set:")
print("   - Application root: /home/bghranac/repositories/bghrana")
print("   - Application startup file: passenger_wsgi.py")
print("   - Application Entry point: application")
print("3. Click 'STOP APP'")
print("4. Wait 15 seconds")
print("5. Click 'START APP'")
print("6. Wait 20 seconds")
print("7. Open https://bghrana.com")
print("=" * 60)
print("\nPassengerfile.json is NOT needed for cPanel Python App!")
print("The app will work without it using cPanel's own config.")
