#!/usr/bin/env python
import os
import shutil

print("Deploying .htaccess to correct locations...")
print("=" * 60)

htaccess_content = """PassengerAppRoot /home/bghranac/repositories/bghrana
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py
PassengerPython /home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python3.11
"""

locations = [
    '/home/bghranac/public_html',
    '/home/bghranac/public_html/bghrana.com',
    '/home/bghranac/repositories/bghrana'
]

for location in locations:
    try:
        if os.path.exists(location):
            htaccess_path = os.path.join(location, '.htaccess')
            with open(htaccess_path, 'w') as f:
                f.write(htaccess_content)
            os.chmod(htaccess_path, 0o644)
            print(f"✓ Created: {htaccess_path}")
        else:
            print(f"⚠ Directory doesn't exist: {location}")
    except Exception as e:
        print(f"✗ Error at {location}: {e}")

print("=" * 60)
print("Now:")
print("1. STOP Python App")
print("2. Wait 15 seconds")
print("3. START Python App")
print("4. Wait 20 seconds")
print("5. Try https://bghrana.com")
