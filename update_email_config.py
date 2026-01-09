#!/usr/bin/env python
"""
Update .env file with email configuration
"""
import os

env_path = '/home/bghranac/repositories/bghrana/.env'

# Email configuration from local .env
EMAIL_SETTINGS = """
# Email Configuration (собствен домейн)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=bghrana.com
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=noreply@bghrana.com
EMAIL_HOST_PASSWORD=fFwYBtUlJi~
DEFAULT_FROM_EMAIL=noreply@bghrana.com
"""

print("=" * 60)
print("UPDATING EMAIL CONFIGURATION")
print("=" * 60)

# Read existing .env
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"\n✓ Found existing .env file")
except FileNotFoundError:
    content = ""
    print(f"\n! .env file not found, will create new one")

# Remove old email settings
lines = content.split('\n')
email_keys = ['EMAIL_BACKEND', 'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS', 
              'EMAIL_USE_SSL', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL']

# Filter out old email lines and empty lines around them
new_lines = []
skip_next_empty = False
for line in lines:
    # Check if this line starts with any email key
    is_email_line = any(line.strip().startswith(key + '=') for key in email_keys)
    # Check if this is an email comment
    is_email_comment = '# Email Configuration' in line or '# email' in line.lower()
    
    if is_email_line or is_email_comment:
        skip_next_empty = True
        continue
    
    # Skip empty line after email section
    if skip_next_empty and line.strip() == '':
        skip_next_empty = False
        continue
    
    skip_next_empty = False
    new_lines.append(line)

# Add email settings at the end
content = '\n'.join(new_lines).rstrip() + '\n' + EMAIL_SETTINGS.strip() + '\n'

# Write back
with open(env_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ Email configuration updated:")
print("  EMAIL_HOST=bghrana.com")
print("  EMAIL_PORT=465")
print("  EMAIL_USE_SSL=True")
print("  EMAIL_HOST_USER=noreply@bghrana.com")
print("  DEFAULT_FROM_EMAIL=noreply@bghrana.com")

print("\n" + "=" * 60)
print("NEXT STEP: Restart Python App")
print("=" * 60)
print("\nGo to cPanel → Setup Python App → RESTART")
print("Then test: https://bghrana.com/accounts/password/reset/")
print("=" * 60)
