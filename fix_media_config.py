#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Fix media files - check and configure everything
"""

import os
import shutil

print("=" * 70)
print("FIXING MEDIA FILES CONFIGURATION")
print("=" * 70)

# Paths
repo_path = '/home/bghranac/repositories/bghrana'
media_dir = os.path.join(repo_path, 'media', 'products')
htaccess_path = '/home/bghranac/public_html/.htaccess'

# Step 1: Create media/products directory
print("\n1. Creating media directories...")
os.makedirs(media_dir, exist_ok=True)
print(f"✓ Created: {media_dir}")

# Step 2: Check if tomatos.jpg exists
tomatos_path = os.path.join(media_dir, 'tomatos.jpg')
if os.path.exists(tomatos_path):
    size = os.path.getsize(tomatos_path)
    print(f"✓ tomatos.jpg exists ({size:,} bytes)")
else:
    print(f"✗ tomatos.jpg NOT found at {tomatos_path}")
    print("  You need to upload it manually via File Manager")

# Step 3: Fix .htaccess
print(f"\n2. Checking .htaccess at {htaccess_path}")

if os.path.exists(htaccess_path):
    with open(htaccess_path, 'r') as f:
        current_content = f.read()
    
    print("✓ .htaccess exists")
    
    # Check if media alias exists
    if 'Alias /media' not in current_content:
        print("⚠ Media alias not found, adding it...")
        
        # Add media configuration at the beginning
        new_content = '''# Media files
Alias /media /home/bghranac/repositories/bghrana/media
<Directory /home/bghranac/repositories/bghrana/media>
    Require all granted
    Options -Indexes
</Directory>

# Static files
Alias /static /home/bghranac/repositories/bghrana/staticfiles
<Directory /home/bghranac/repositories/bghrana/staticfiles>
    Require all granted
    Options -Indexes
</Directory>

''' + current_content
        
        # Backup and write
        backup_path = htaccess_path + '.backup'
        shutil.copy2(htaccess_path, backup_path)
        print(f"✓ Backup created: {backup_path}")
        
        with open(htaccess_path, 'w') as f:
            f.write(new_content)
        print("✓ .htaccess updated with media alias")
    else:
        print("✓ Media alias already exists")
else:
    print(f"✗ .htaccess not found, creating it...")
    content = '''# Media files
Alias /media /home/bghranac/repositories/bghrana/media
<Directory /home/bghranac/repositories/bghrana/media>
    Require all granted
    Options -Indexes
</Directory>

# Static files
Alias /static /home/bghranac/repositories/bghrana/staticfiles
<Directory /home/bghranac/repositories/bghrana/staticfiles>
    Require all granted
    Options -Indexes
</Directory>

# Passenger configuration
PassengerAppRoot /home/bghranac/repositories/bghrana
PassengerBaseURI /
PassengerPython /home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py
'''
    with open(htaccess_path, 'w') as f:
        f.write(content)
    print("✓ .htaccess created")

print("\n" + "=" * 70)
print("✓ CONFIGURATION COMPLETE")
print("=" * 70)

print("\nNEXT STEPS:")
print("1. Upload tomatos.jpg to: /home/bghranac/repositories/bghrana/media/products/")
print("   (Use File Manager if not already there)")
print("2. Restart Python App in cPanel")
print("3. Test: https://bghrana.com/media/products/tomatos.jpg")
print("4. Refresh main page: https://bghrana.com")
