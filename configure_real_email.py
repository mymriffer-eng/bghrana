#!/usr/bin/env python
"""
Configure real email server for production
"""
import os

env_path = '/home/bghranac/repositories/bghrana/.env'

# Email configuration - update these values
EMAIL_CONFIG = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'mail.bghrana.com',  # Your email server
    'EMAIL_PORT': '587',  # 587 for TLS, 465 for SSL
    'EMAIL_USE_TLS': 'True',  # True for port 587
    'EMAIL_USE_SSL': 'False',  # True for port 465
    'EMAIL_HOST_USER': 'noreply@bghrana.com',  # Your email address
    'EMAIL_HOST_PASSWORD': 'YOUR_EMAIL_PASSWORD_HERE',  # Email password
    'DEFAULT_FROM_EMAIL': 'БГ Храна <noreply@bghrana.com>',
}

print("=" * 60)
print("EMAIL SERVER CONFIGURATION")
print("=" * 60)

# Read existing .env
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = []

# Remove old email settings
lines = [line for line in lines if not any(line.startswith(key + '=') for key in EMAIL_CONFIG.keys())]

# Add new email settings
print("\nAdding email configuration:")
for key, value in EMAIL_CONFIG.items():
    lines.append(f'{key}={value}\n')
    print(f"  {key}={value}")

# Write back
with open(env_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✓ Email configuration added to .env")
print("\n" + "=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("1. Edit this script and update:")
print("   - EMAIL_HOST: Your actual mail server")
print("   - EMAIL_HOST_USER: Your email address")
print("   - EMAIL_HOST_PASSWORD: Your email password")
print("   - EMAIL_PORT: 587 (TLS) or 465 (SSL)")
print("\n2. Run this script via cPanel 'Execute Python Script'")
print("\n3. Restart Python App")
print("\n4. Test password reset at /accounts/password/reset/")
print("=" * 60)
