#!/usr/bin/env python
"""
Force update .env and verify email works
"""
import os
import sys

print("=" * 70)
print("STEP 1: FORCE UPDATE .ENV FILE")
print("=" * 70)

env_path = '/home/bghranac/repositories/bghrana/.env'

# Read current .env
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        current_content = f.read()
    print("Current .env email settings:")
    for line in current_content.split('\n'):
        if 'EMAIL_' in line or 'DEFAULT_FROM_EMAIL' in line:
            print(f"  {line}")
except Exception as e:
    print(f"Error reading .env: {e}")
    current_content = ""

# Remove ALL email-related lines
lines = current_content.split('\n')
new_lines = []
skip_next_empty = False

for line in lines:
    # Skip email lines
    if any(key in line for key in ['EMAIL_BACKEND', 'EMAIL_HOST', 'EMAIL_PORT', 
                                     'EMAIL_USE_TLS', 'EMAIL_USE_SSL', 
                                     'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 
                                     'DEFAULT_FROM_EMAIL']):
        skip_next_empty = True
        continue
    
    # Skip email comment
    if '# Email Configuration' in line or '# email' in line.lower():
        skip_next_empty = True
        continue
    
    # Skip empty line after email section
    if skip_next_empty and line.strip() == '':
        skip_next_empty = False
        continue
    
    skip_next_empty = False
    new_lines.append(line)

# Add working email configuration
working_config = """
# Email Configuration (Working: mail.bghrana.com port 587 TLS)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.bghrana.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=noreply@bghrana.com
EMAIL_HOST_PASSWORD=fFwYBtUlJi~
DEFAULT_FROM_EMAIL=noreply@bghrana.com
"""

final_content = '\n'.join(new_lines).rstrip() + working_config + '\n'

# Write back
with open(env_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("\n✓ .env updated with working configuration")

# Verify it was written
with open(env_path, 'r', encoding='utf-8') as f:
    verify_content = f.read()

print("\nVerifying new .env email settings:")
for line in verify_content.split('\n'):
    if 'EMAIL_' in line or 'DEFAULT_FROM_EMAIL' in line:
        print(f"  {line}")

print("\n" + "=" * 70)
print("STEP 2: TEST EMAIL WITH NEW SETTINGS")
print("=" * 70)

# Clear any cached settings
if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

# Force fresh import
sys.path.insert(0, '/home/bghranac/repositories/bghrana')
os.environ['DJANGO_SETTINGS_MODULE'] = 'products.settings'

# Clear module cache
import importlib
if 'django' in sys.modules:
    del sys.modules['django']
if 'django.conf' in sys.modules:
    del sys.modules['django.conf']
if 'products.settings' in sys.modules:
    del sys.modules['products.settings']

# Fresh import
import django
django.setup()

from django.conf import settings
from django.core.mail import send_mail

print(f"\nDjango loaded settings:")
print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"  EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")

print("\nAttempting to send test email...")
try:
    send_mail(
        'БГ Храна - Password Reset Test',
        'If you receive this, email configuration is working!',
        settings.DEFAULT_FROM_EMAIL,
        ['noreply@bghrana.com'],
        fail_silently=False,
    )
    print("✓✓✓ SUCCESS! Email sent!")
except Exception as e:
    print(f"✗ Failed: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
print("NOW: Restart Python App and test at /accounts/password/reset/")
print("=" * 70)
