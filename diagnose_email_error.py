#!/usr/bin/env python
"""
Diagnose password reset error by checking logs and testing email
"""
import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/home/bghranac/repositories/bghrana')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')

import django
django.setup()

from django.conf import settings
from django.core.mail import send_mail

print("=" * 60)
print("EMAIL CONFIGURATION TEST")
print("=" * 60)

# Check settings
print(f"\nEMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# Test email sending
print("\n" + "=" * 60)
print("TESTING EMAIL SEND")
print("=" * 60)

try:
    print("\nAttempting to send test email...")
    send_mail(
        'Test Email from БГ Храна',
        'This is a test email to verify email configuration.',
        settings.DEFAULT_FROM_EMAIL,
        ['admin@bghrana.com'],
        fail_silently=False,
    )
    print("✓ Email sent successfully!")
except Exception as e:
    print(f"✗ Error sending email: {e}")
    print(f"Error type: {type(e).__name__}")

# Check passenger log for errors
print("\n" + "=" * 60)
print("CHECKING PASSENGER LOG")
print("=" * 60)

log_file = '/home/bghranac/repositories/bghrana/tmp/log/passenger.log'
try:
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # Find last traceback
    traceback_indices = [i for i, line in enumerate(lines) if 'Traceback' in line]
    
    if traceback_indices:
        last_idx = traceback_indices[-1]
        print("\n=== LAST ERROR IN LOG ===")
        print(''.join(lines[max(0, last_idx-5):min(last_idx+40, len(lines))]))
    else:
        print("\nNo tracebacks found in log")
except Exception as e:
    print(f"Could not read log: {e}")

print("\n" + "=" * 60)
