#!/usr/bin/env python
"""
Try alternative email configuration (port 587 with TLS)
"""
import os
import sys

sys.path.insert(0, '/home/bghranac/repositories/bghrana')

print("=" * 70)
print("TRYING ALTERNATIVE EMAIL CONFIGURATIONS")
print("=" * 70)

# Configuration options to try
configs = [
    {
        'name': 'Config 1: mail.bghrana.com port 587 TLS',
        'host': 'mail.bghrana.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
    },
    {
        'name': 'Config 2: mail.bghrana.com port 465 SSL',
        'host': 'mail.bghrana.com',
        'port': 465,
        'use_tls': False,
        'use_ssl': True,
    },
    {
        'name': 'Config 3: localhost port 587 TLS',
        'host': 'localhost',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
    },
    {
        'name': 'Config 4: localhost port 465 SSL',
        'host': 'localhost',
        'port': 465,
        'use_tls': False,
        'use_ssl': True,
    },
]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')

import django
django.setup()

from django.core.mail import send_mail
from django.conf import settings
import smtplib

working_config = None

for config in configs:
    print(f"\n--- Testing: {config['name']} ---")
    
    # Update settings
    settings.EMAIL_HOST = config['host']
    settings.EMAIL_PORT = config['port']
    settings.EMAIL_USE_TLS = config['use_tls']
    settings.EMAIL_USE_SSL = config['use_ssl']
    
    try:
        # Try to connect
        send_mail(
            'Test - БГ Храна',
            'Test email',
            'noreply@bghrana.com',
            ['noreply@bghrana.com'],
            fail_silently=False,
        )
        print(f"✓ SUCCESS! This configuration works!")
        working_config = config
        break
    except Exception as e:
        print(f"✗ Failed: {type(e).__name__}: {str(e)[:100]}")

print("\n" + "=" * 70)
if working_config:
    print("WORKING CONFIGURATION FOUND:")
    print("=" * 70)
    print(f"EMAIL_HOST={working_config['host']}")
    print(f"EMAIL_PORT={working_config['port']}")
    print(f"EMAIL_USE_TLS={working_config['use_tls']}")
    print(f"EMAIL_USE_SSL={working_config['use_ssl']}")
    print("\nAdd these to your .env file!")
else:
    print("NO WORKING CONFIGURATION FOUND")
    print("=" * 70)
    print("\nPossible issues:")
    print("1. Email account noreply@bghrana.com doesn't exist")
    print("2. Password is incorrect")
    print("3. Email service not enabled in cPanel")
    print("\nCheck in cPanel:")
    print("  - Email Accounts → verify noreply@bghrana.com exists")
    print("  - Email Deliverability → check configuration")
print("=" * 70)
