#!/usr/bin/env python
"""
Поправка на Facebook Login - изчистване на cache и проверка на конфигурация
"""
import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

# SSH Connection параметри
hostname = os.getenv('SSH_HOST', 'bghrana.com')
username = os.getenv('SSH_USER', 'bghranac')
password = os.getenv('SSH_PASSWORD')

print("=" * 70)
print("FIX FACEBOOK LOGIN - Почистване на cache и проверки")
print("=" * 70)

commands = """
cd ~/repositories/bghrana

echo "=== 1. Проверка на git версия ==="
git log --oneline -3

echo ""
echo "=== 2. Проверка на settings.py за Facebook ==="
grep -n "'facebook'" products/settings.py | head -5

echo ""
echo "=== 3. Изтриване на Python cache ==="
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
echo "✓ Cache изтрит"

echo ""
echo "=== 4. Рестартиране на app (3 пъти за сигурност) ==="
touch tmp/restart.txt
sleep 2
touch tmp/restart.txt
sleep 2
touch tmp/restart.txt
echo "✓ App рестартиран"

echo ""
echo "=== 5. Финална проверка на settings.py ==="
grep -A 10 "SOCIALACCOUNT_PROVIDERS" products/settings.py | grep -E "(google|facebook)"
"""

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"\n🔌 Connecting to {hostname}...")
    ssh.connect(hostname, username=username, password=password)
    
    stdin, stdout, stderr = ssh.exec_command(commands)
    
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    print(output)
    if error and 'No such file' not in error and 'warning' not in error.lower():
        print(f"\nERROR OUTPUT:\n{error}")
    
    ssh.close()
    
    print("\n" + "=" * 70)
    print("ГОТОВО! Изчакай 30 секунди и тествай:")
    print("1. https://bghrana.com/register - трябва да има Facebook бутон")
    print("2. Натисни Facebook бутона - трябва да отвори Facebook (не Google)")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Грешка: {e}")
    print("\nПроверка на .env файл - трябва да има:")
    print("SSH_HOST=bghrana.com")
    print("SSH_USER=твоето_потребителско_име")
    print("SSH_PASSWORD=твоята_парола")
