#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Check and fix static files configuration
"""

import os
import shutil

repo_path = '/home/bghranac/repositories/bghrana'
public_html = '/home/bghranac/public_html'
htaccess_path = os.path.join(public_html, '.htaccess')

print("=" * 70)
print("CHECKING STATIC FILES CONFIGURATION")
print("=" * 70)

# Check if staticfiles directory exists
staticfiles_dir = os.path.join(repo_path, 'staticfiles')
if os.path.exists(staticfiles_dir):
    files = os.listdir(staticfiles_dir)
    print(f"\n✓ staticfiles directory exists with {len(files)} items")
    
    # Check for logo.jpg
    if 'logo.jpg' in files:
        print(f"✓ logo.jpg found in staticfiles/")
        logo_size = os.path.getsize(os.path.join(staticfiles_dir, 'logo.jpg'))
        print(f"  Size: {logo_size} bytes")
    else:
        print(f"✗ logo.jpg NOT found in staticfiles/")
        print(f"  Files present: {files[:10]}")
else:
    print(f"✗ staticfiles directory does not exist!")

# Check .htaccess file
print(f"\n{'='*70}")
print("CHECKING .htaccess CONFIGURATION")
print("=" * 70)

if os.path.exists(htaccess_path):
    print(f"\n✓ .htaccess exists")
    with open(htaccess_path, 'r') as f:
        content = f.read()
    
    print("\nCurrent .htaccess content:")
    print("-" * 70)
    print(content)
    print("-" * 70)
    
    # Check if static alias exists
    if 'Alias /static' in content or 'AliasMatch /static' in content:
        print("\n✓ Static files alias found")
    else:
        print("\n⚠ WARNING: No static files alias found!")
        print("\nRecommended .htaccess content:")
        print("-" * 70)
        recommended = '''# Static files
Alias /static /home/bghranac/repositories/bghrana/staticfiles
<Directory /home/bghranac/repositories/bghrana/staticfiles>
    Require all granted
    Options -Indexes
</Directory>

# Media files
Alias /media /home/bghranac/repositories/bghrana/media
<Directory /home/bghranac/repositories/bghrana/media>
    Require all granted
    Options -Indexes
</Directory>

# Passenger configuration
PassengerAppRoot /home/bghranac/repositories/bghrana
PassengerBaseURI /
PassengerPython /home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py

# Environment variables from Python App settings
'''
        print(recommended)
        print("-" * 70)
else:
    print(f"\n✗ .htaccess does NOT exist at {htaccess_path}")

print("\n" + "=" * 70)
print("RECOMMENDATIONS:")
print("=" * 70)
print("1. Run run_collectstatic_new.py to collect static files")
print("2. Update .htaccess with Alias directives for /static and /media")
print("3. Restart Python App")
print("4. Test: https://bghrana.com/static/logo.jpg")
