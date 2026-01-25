#!/usr/bin/env python3
"""
Проверка за потребител с конкретен имейл във всички таблици
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

email = "mymriffer@mail.com"

print(f"🔍 Търсене на имейл: {email}\n")

# 1. Django User таблица
print("1️⃣ Django User таблица:")
users = User.objects.filter(email__iexact=email)
if users.exists():
    for user in users:
        print(f"   ✅ Намерен: {user.username} | Email: {user.email} | Active: {user.is_active}")
else:
    print("   ❌ Няма потребител в User таблицата")

# 2. Allauth EmailAddress таблица
print("\n2️⃣ Allauth EmailAddress таблица:")
email_addresses = EmailAddress.objects.filter(email__iexact=email)
if email_addresses.exists():
    for ea in email_addresses:
        print(f"   ✅ Намерен: User {ea.user.username} | Email: {ea.email}")
        print(f"      Verified: {ea.verified} | Primary: {ea.primary}")
else:
    print("   ❌ Няма в EmailAddress таблицата")

# 3. Social accounts (Google OAuth)
print("\n3️⃣ Social Accounts (Google):")
social_accounts = SocialAccount.objects.all()
for sa in social_accounts:
    extra_data = sa.extra_data
    if extra_data and extra_data.get('email', '').lower() == email.lower():
        print(f"   ✅ Google account: {sa.user.username} | Email: {extra_data.get('email')}")

if not social_accounts.exists():
    print("   ❌ Няма social accounts")

# 4. Проверка за неактивирани потребители
print("\n4️⃣ Неактивирани потребители с този имейл:")
inactive = User.objects.filter(email__iexact=email, is_active=False)
if inactive.exists():
    for user in inactive:
        print(f"   ⚠️ Неактивен: {user.username} | Регистриран на: {user.date_joined}")
else:
    print("   ✅ Няма неактивирани")

print("\n" + "="*50)
print("💡 Решение:")
print("="*50)
if email_addresses.exists() or users.exists():
    print("1. Изтрий стария запис от админ панела")
    print("2. Или пробвай Password Reset вместо регистрация")
else:
    print("Имейлът е свободен - опитай отново регистрация")
