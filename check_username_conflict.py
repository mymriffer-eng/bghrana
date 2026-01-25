#!/usr/bin/env python3
"""
Проверка за username конфликт
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.contrib.auth.models import User

username = "mymriffer"

print(f"🔍 Търсене на username: {username}\n")

users = User.objects.filter(username__iexact=username)
if users.exists():
    for user in users:
        print(f"✅ Намерен потребител:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Active: {user.is_active}")
        print(f"   Регистриран: {user.date_joined}")
        print(f"\n💡 За да изтриеш: python manage.py shell")
        print(f"   >>> from django.contrib.auth.models import User")
        print(f"   >>> User.objects.filter(username='{user.username}').delete()")
else:
    print("❌ Няма потребител с това username")

# Покажи всички потребители
print("\n📋 Всички потребители в системата:")
all_users = User.objects.all()
for u in all_users:
    print(f"   - {u.username} ({u.email}) - Active: {u.is_active}")
