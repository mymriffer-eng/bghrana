#!/usr/bin/env python3
"""
Изтриване на проблемни потребители
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.contrib.auth.models import User

print("🧹 Почистване на проблемни потребители...\n")

# 1. Изтрий празния потребител
empty_users = User.objects.filter(username='')
if empty_users.exists():
    print(f"❌ Изтриване на {empty_users.count()} празен потребител...")
    for u in empty_users:
        print(f"   Изтрит: '{u.username}' (email: '{u.email}')")
        u.delete()
    print("   ✅ Готово\n")
else:
    print("✅ Няма празни потребители\n")

# 2. Покажи всички потребители след почистване
print("📋 Потребители след почистване:")
all_users = User.objects.all()
for u in all_users:
    status = "✅" if u.is_active else "⚠️"
    print(f"   {status} {u.username} ({u.email}) - Active: {u.is_active}")

print("\n💡 За регистрация на mymriffer@mail.com:")
print("   Използвай РАЗЛИЧЕН username (не 'mymriffer')")
print("   Например: mymriffer2, mymriffer_mail, mymriffer_new и т.н.")
