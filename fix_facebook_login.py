#!/usr/bin/env python
"""
Поправка на Facebook Login - изчистване на cache и рестартиране
Изпълнява се директно на production сървъра
"""
import subprocess
import os

def run_command(cmd, description):
    """Изпълнява команда и показва резултата"""
    print(f"\n{description}")
    print("-" * 70)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.path.expanduser('~/repositories/bghrana'))
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr and 'warning' not in result.stderr.lower():
            print(f"ERROR: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR: {e}")
        return False

print("=" * 70)
print("FIX FACEBOOK LOGIN - Почистване на cache и проверки")
print("=" * 70)

# 1. Проверка на git версия
run_command("git log --oneline -3", "=== 1. Проверка на git версия ===")

# 2. Проверка на settings.py за Facebook
print("\n=== 2. Проверка на settings.py за Facebook ===")
print("-" * 70)
try:
    with open(os.path.expanduser('~/repositories/bghrana/products/settings.py'), 'r', encoding='utf-8') as f:
        content = f.read()
        if "'facebook'" in content or '"facebook"' in content:
            print("✓ Facebook е в settings.py")
            for i, line in enumerate(content.split('\n'), 1):
                if 'facebook' in line.lower():
                    print(f"Line {i}: {line.strip()}")
                    break
        else:
            print("✗ Facebook ЛИПСВА в settings.py!")
except Exception as e:
    print(f"ERROR: {e}")

# 3. Изтриване на Python cache
print("\n=== 3. Изтриване на Python cache ===")
print("-" * 70)
base_path = os.path.expanduser('~/repositories/bghrana')
deleted_count = 0
for root, dirs, files in os.walk(base_path):
    # Изтрий __pycache__ директории
    if '__pycache__' in dirs:
        cache_dir = os.path.join(root, '__pycache__')
        try:
            import shutil
            shutil.rmtree(cache_dir)
            deleted_count += 1
        except:
            pass
    # Изтрий .pyc и .pyo файлове
    for file in files:
        if file.endswith(('.pyc', '.pyo')):
            try:
                os.remove(os.path.join(root, file))
                deleted_count += 1
            except:
                pass
print(f"✓ Изтрити {deleted_count} cache файла/директории")

# 4. Рестартиране на app
print("\n=== 4. Рестартиране на app (3 пъти за сигурност) ===")
print("-" * 70)
restart_file = os.path.expanduser('~/repositories/bghrana/tmp/restart.txt')
os.makedirs(os.path.dirname(restart_file), exist_ok=True)
for i in range(3):
    try:
        with open(restart_file, 'a') as f:
            f.write(f'restart {i+1}\n')
        print(f"✓ Restart {i+1}/3")
        if i < 2:
            import time
            time.sleep(2)
    except Exception as e:
        print(f"ERROR restart {i+1}: {e}")

# 5. Финална проверка
run_command("grep -A 15 'SOCIALACCOUNT_PROVIDERS' products/settings.py | grep -E '(google|facebook)'", 
            "=== 5. Финална проверка на SOCIALACCOUNT_PROVIDERS ===")

print("\n" + "=" * 70)
print("ГОТОВО! Изчакай 30 секунди и тествай:")
print("1. https://bghrana.com/register - трябва да има Facebook бутон")
print("2. Натисни Facebook бутона - трябва да отвори Facebook (не Google)")
print("=" * 70)
