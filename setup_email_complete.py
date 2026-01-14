#!/usr/bin/env python
"""
All-in-one script: Update email config and diagnose
Copy and paste this entire script into cPanel Execute Python Script
"""
import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/home/bghranac/repositories/bghrana')

print("=" * 70)
print("STEP 1: UPDATE .ENV FILE WITH EMAIL CONFIGURATION")
print("=" * 70)

env_path = '/home/bghranac/repositories/bghrana/.env'

# Email configuration
email_lines = [
    "",
    "# Email Configuration",
    "EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend",
    "EMAIL_HOST=mail.bghrana.com",
    "EMAIL_PORT=465",
    "EMAIL_USE_TLS=False",
    "EMAIL_USE_SSL=True",
    "EMAIL_HOST_USER=noreply@bghrana.com",
    "EMAIL_HOST_PASSWORD=fFwYBtUlJi~",
    "DEFAULT_FROM_EMAIL=noreply@bghrana.com",
    ""
]

try:
    # Read existing .env
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
        print("! .env file not found, creating new one")
    
    # Remove old email settings
    email_keys = ['EMAIL_BACKEND', 'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS', 
                  'EMAIL_USE_SSL', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL']
    
    new_lines = []
    for line in lines:
        # Skip if line starts with any email key
        if not any(line.strip().startswith(key + '=') for key in email_keys):
            # Skip email comment lines
            if '# Email Configuration' not in line and '# email' not in line.lower():
                new_lines.append(line.rstrip())
    
    # Add email settings
    all_lines = new_lines + email_lines
    
    # Write back
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_lines))
    
    print("✓ Email configuration updated in .env")
    
except Exception as e:
    print(f"✗ Error updating .env: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("STEP 2: TEST EMAIL CONFIGURATION")
print("=" * 70)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')

try:
    import django
    django.setup()
    print("✓ Django initialized")
except Exception as e:
    print(f"✗ Error initializing Django: {e}")
    sys.exit(1)

from django.conf import settings
from django.core.mail import send_mail

print(f"\nEMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

print("\n" + "=" * 70)
print("STEP 3: SEND TEST EMAIL")
print("=" * 70)

try:
    send_mail(
        'Test Email - БГ Храна Password Reset',
        'This is a test email to verify email configuration works.',
        settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    print("✓ Test email sent successfully!")
    print(f"  Check inbox: {settings.EMAIL_HOST_USER}")
except Exception as e:
    print(f"✗ Error sending email:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("STEP 4: CHECK PASSENGER LOG FOR ERRORS")
print("=" * 70)

log_file = '/home/bghranac/repositories/bghrana/tmp/log/passenger.log'
try:
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # Find last traceback
    traceback_indices = [i for i, line in enumerate(lines) if 'Traceback' in line]
    
    if traceback_indices:
        last_idx = traceback_indices[-1]
        print("\n=== LAST ERROR IN PASSENGER LOG ===")
        error_lines = lines[max(0, last_idx-3):min(last_idx+35, len(lines))]
        print(''.join(error_lines))
    else:
        print("\n✓ No tracebacks found in log")
except Exception as e:
    print(f"Could not read log: {e}")

print("\n" + "=" * 70)
print("COMPLETED - Now restart Python App and test password reset")
print("=" * 70)
