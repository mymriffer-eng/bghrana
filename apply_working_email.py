#!/usr/bin/env python
"""
Apply working email configuration
"""
import os

env_path = '/home/bghranac/repositories/bghrana/.env'

print("=" * 70)
print("APPLYING WORKING EMAIL CONFIGURATION")
print("=" * 70)

# Working configuration from tests
email_config = """
# Email Configuration (Working: port 587 TLS)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.bghrana.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=noreply@bghrana.com
EMAIL_HOST_PASSWORD=fFwYBtUlJi~
DEFAULT_FROM_EMAIL=noreply@bghrana.com
"""

# Read existing .env
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = []
    print("! Creating new .env file")

# Remove old email settings
email_keys = ['EMAIL_BACKEND', 'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS', 
              'EMAIL_USE_SSL', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL']

new_lines = []
for line in lines:
    if not any(line.strip().startswith(key + '=') for key in email_keys):
        if '# Email Configuration' not in line and '# email' not in line.lower():
            new_lines.append(line.rstrip())

# Add working config
all_lines = new_lines + email_config.strip().split('\n') + ['']

# Write back
with open(env_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_lines))

print("✓ Working email configuration applied:")
print("  EMAIL_HOST=mail.bghrana.com")
print("  EMAIL_PORT=587")
print("  EMAIL_USE_TLS=True")

print("\n" + "=" * 70)
print("NEXT: Restart Python App, then test password reset!")
print("=" * 70)
