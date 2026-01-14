#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Check Passenger and Django logs for errors
"""

import os

log_files = [
    '/home/bghranac/repositories/bghrana/passenger.log',
    '/home/bghranac/passenger_debug.log',
    '/home/bghranac/logs/bghrana.com.error.log',
]

print("=" * 70)
print("CHECKING LOG FILES FOR ERRORS")
print("=" * 70)

for log_path in log_files:
    if os.path.exists(log_path):
        print(f"\n{'='*70}")
        print(f"LOG: {log_path}")
        print("=" * 70)
        
        try:
            with open(log_path, 'r') as f:
                lines = f.readlines()
                # Get last 50 lines
                last_lines = lines[-50:] if len(lines) > 50 else lines
                print(''.join(last_lines))
        except Exception as e:
            print(f"✗ ERROR reading log: {e}")
    else:
        print(f"\n⚠ Log file not found: {log_path}")

print("\n" + "=" * 70)
print("CHECKING IF FIX WAS APPLIED")
print("=" * 70)

# Check database
import sys
import django

repo_path = '/home/bghranac/repositories/bghrana'
sys.path.insert(0, repo_path)
os.chdir(repo_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.contrib.sites.models import Site

try:
    site = Site.objects.get(id=1)
    print(f"\nCurrent Site: {site.domain}")
    
    if site.domain == 'bghrana.com':
        print("✓ Site is correctly configured")
    else:
        print(f"✗ Site domain is still: {site.domain}")
        print("  Updating now...")
        site.domain = 'bghrana.com'
        site.name = 'БГ Храна'
        site.save()
        print("✓ Updated!")
except Exception as e:
    print(f"✗ ERROR: {e}")
