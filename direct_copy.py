#!/usr/bin/env python
import os
import shutil

print("=" * 60)
print("Direct copy: Django project to public_html")
print("=" * 60)

source = '/home/bghranac/repositories/bghrana'
dest = '/home/bghranac/public_html'

# First, update passenger_wsgi.py manually
passenger_content = '''import os
import sys

# Logging for debugging
import logging
logging.basicConfig(
    filename='/home/bghranac/passenger_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s'
)

try:
    logging.info("=" * 60)
    logging.info("Passenger WSGI starting...")
    
    # Add project directory to the sys.path
    project_dir = os.path.dirname(__file__)
    sys.path.insert(0, project_dir)
    logging.info(f"Project directory: {project_dir}")
    logging.info(f"Python path: {sys.path[:3]}")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
    logging.info(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    
    # Import Django WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    logging.info("✓ Django WSGI application loaded successfully")
    logging.info("=" * 60)
    
except Exception as e:
    logging.error(f"✗ ERROR loading Django: {e}")
    logging.exception("Full traceback:")
    raise
'''

with open(os.path.join(source, 'passenger_wsgi.py'), 'w') as f:
    f.write(passenger_content)
print("  ✓ Updated passenger_wsgi.py in source")

# Files and directories to copy
items_to_copy = [
    'catalog',
    'products',
    'locale',
    'media',
    'staticfiles',
    'manage.py',
    'passenger_wsgi.py',
]

print("\nCopying files to public_html...")
for item in items_to_copy:
    src_path = os.path.join(source, item)
    dst_path = os.path.join(dest, item)
    
    try:
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                print(f"  ✓ Copied directory: {item}")
            else:
                shutil.copy2(src_path, dst_path)
                os.chmod(dst_path, 0o755)
                print(f"  ✓ Copied file: {item}")
        else:
            print(f"  ⚠ Not found: {item}")
    except Exception as e:
        print(f"  ✗ Error copying {item}: {e}")

print("\n" + "=" * 60)
print("CRITICAL STEPS:")
print("1. Setup Python App → EDIT existing app")
print("2. Change 'Application root' to: /home/bghranac/public_html")
print("3. Click 'Update'")
print("4. RESTART app")
print("5. Wait 30 seconds")
print("6. Open https://bghrana.com")
print("=" * 60)
