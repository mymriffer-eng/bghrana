#!/usr/bin/env python
import os
import shutil

print("=" * 60)
print("Fixing public_html for Django")
print("=" * 60)

public_html = '/home/bghranac/public_html'

# Step 1: Backup and remove index.html
index_html = os.path.join(public_html, 'index.html')
if os.path.exists(index_html):
    backup = os.path.join(public_html, 'index.html.backup')
    shutil.move(index_html, backup)
    print(f"✓ Moved index.html to index.html.backup")

# Step 2: Clean .htaccess and keep only cPanel config
htaccess = os.path.join(public_html, '.htaccess')
new_content = """# DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION BEGIN
PassengerAppRoot "/home/bghranac/repositories/bghrana"
PassengerBaseURI "/"
PassengerPython "/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python"
PassengerStartupFile "passenger_wsgi.py"
PassengerAppType "wsgi"
# DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION END
"""

with open(htaccess, 'w') as f:
    f.write(new_content)
os.chmod(htaccess, 0o644)
print(f"✓ Updated .htaccess with clean config")

print("\n" + "=" * 60)
print("Done! Now:")
print("1. RESTART Python App")
print("2. Wait 20 seconds")
print("3. Open https://bghrana.com")
print("=" * 60)
