#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
sys.path.insert(0, '/home/bghranac/repositories/bghrana')

django.setup()

# Create superuser
from django.contrib.auth import get_user_model

User = get_user_model()

print("Creating superuser...")
print("=" * 60)

# Check if superuser already exists
if User.objects.filter(is_superuser=True).exists():
    print("✓ Superuser already exists!")
    superuser = User.objects.filter(is_superuser=True).first()
    print(f"  Username: {superuser.username}")
    print(f"  Email: {superuser.email}")
else:
    try:
        # Create superuser with default credentials
        username = 'admin'
        email = 'admin@bghrana.com'
        password = 'AdminPass2024!'
        
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print("✓ Superuser created successfully!")
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print("\n⚠ IMPORTANT: Change this password after first login!")
    except Exception as e:
        print(f"✗ ERROR: {e}")
        sys.exit(1)

print("=" * 60)
