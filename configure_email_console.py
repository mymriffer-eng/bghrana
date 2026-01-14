#!/usr/bin/env python
"""
Configure email backend to use console for testing password reset
This will print emails to console instead of sending them
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
from decouple import config

print("=" * 60)
print("EMAIL CONFIGURATION CHECK")
print("=" * 60)

print(f"\nCurrent EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
print("\nFor testing, add to your .env file:")
print("EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend")
print("\nThis will print password reset emails to the console/logs")
print("instead of actually sending them.")
print("\nFor production, you need to configure:")
print("EMAIL_HOST=mail.bghrana.com")
print("EMAIL_HOST_USER=your-email@bghrana.com")
print("EMAIL_HOST_PASSWORD=your-password")
print("EMAIL_PORT=587 (or 465 for SSL)")
print("EMAIL_USE_TLS=True")
print("\n" + "=" * 60)
