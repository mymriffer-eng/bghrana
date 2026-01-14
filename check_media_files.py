#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Check media files configuration and directory structure
"""

import os

repo_path = '/home/bghranac/repositories/bghrana'
media_dir = os.path.join(repo_path, 'media')
products_dir = os.path.join(media_dir, 'products')
tomatos_file = os.path.join(products_dir, 'tomatos.jpg')

print("=" * 70)
print("CHECKING MEDIA FILES")
print("=" * 70)

# Check media directory
if os.path.exists(media_dir):
    print(f"\n✓ media directory exists: {media_dir}")
    items = os.listdir(media_dir)
    print(f"  Contents: {items}")
else:
    print(f"\n✗ media directory does NOT exist: {media_dir}")
    print("  Creating media directory...")
    os.makedirs(media_dir, exist_ok=True)
    print("  ✓ Created")

# Check products subdirectory
if os.path.exists(products_dir):
    print(f"\n✓ products directory exists: {products_dir}")
    items = os.listdir(products_dir)
    print(f"  Contents ({len(items)} files): {items}")
else:
    print(f"\n✗ products directory does NOT exist: {products_dir}")
    print("  Creating products directory...")
    os.makedirs(products_dir, exist_ok=True)
    print("  ✓ Created")

# Check tomatos.jpg
if os.path.exists(tomatos_file):
    size = os.path.getsize(tomatos_file)
    print(f"\n✓ tomatos.jpg exists!")
    print(f"  Path: {tomatos_file}")
    print(f"  Size: {size:,} bytes")
    
    # Check permissions
    import stat
    st = os.stat(tomatos_file)
    mode = stat.filemode(st.st_mode)
    octal = oct(st.st_mode)[-3:]
    print(f"  Permissions: {mode} ({octal})")
else:
    print(f"\n✗ tomatos.jpg does NOT exist: {tomatos_file}")

# Check .htaccess in public_html
htaccess_path = '/home/bghranac/public_html/.htaccess'
print(f"\n{'='*70}")
print("CHECKING .htaccess FOR MEDIA ALIAS")
print("=" * 70)

if os.path.exists(htaccess_path):
    with open(htaccess_path, 'r') as f:
        content = f.read()
    
    if 'Alias /media' in content:
        print("\n✓ Media alias found in .htaccess")
    else:
        print("\n✗ Media alias NOT found in .htaccess")
        print("\nYou need to add this to .htaccess:")
        print("-" * 70)
        print('''# Media files
Alias /media /home/bghranac/repositories/bghrana/media
<Directory /home/bghranac/repositories/bghrana/media>
    Require all granted
    Options -Indexes
</Directory>''')
        print("-" * 70)
else:
    print(f"\n✗ .htaccess not found at {htaccess_path}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("\nTo fix media files:")
print("1. Upload tomatos.jpg to /home/bghranac/repositories/bghrana/media/products/")
print("2. Add media Alias to .htaccess in public_html")
print("3. Test: https://bghrana.com/media/products/tomatos.jpg")
