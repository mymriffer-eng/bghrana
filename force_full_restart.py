#!/usr/bin/env python
"""
Пълен restart на Python app - убива всички кеширани модули
"""
import subprocess
import os
import time

print("=" * 70)
print("ПЪЛЕН RESTART НА PYTHON APP")
print("=" * 70)

base_path = os.path.expanduser('~/repositories/bghrana')

# 1. Изтрий всички cache файлове
print("\n1. Изтриване на Python cache...")
deleted = 0
for root, dirs, files in os.walk(base_path):
    if '__pycache__' in dirs:
        cache_dir = os.path.join(root, '__pycache__')
        try:
            import shutil
            shutil.rmtree(cache_dir)
            deleted += 1
        except:
            pass
    for file in files:
        if file.endswith(('.pyc', '.pyo')):
            try:
                os.remove(os.path.join(root, file))
                deleted += 1
            except:
                pass
print(f"   ✓ Изтрито {deleted} cache файла")

# 2. Рестартирай app 5 пъти за сигурност
print("\n2. Рестартиране на app (5 пъти)...")
restart_file = os.path.join(base_path, 'tmp/restart.txt')
os.makedirs(os.path.dirname(restart_file), exist_ok=True)

for i in range(5):
    with open(restart_file, 'w') as f:
        f.write(f'Force restart {i+1} at {time.time()}\n')
    print(f"   ✓ Restart {i+1}/5")
    time.sleep(3)

print("\n3. Финален restart...")
# Създай нов файл за финален restart
with open(restart_file, 'w') as f:
    f.write(f'FINAL RESTART at {time.time()}\n')

print("\n" + "=" * 70)
print("ГОТОВО!")
print("=" * 70)
print("\nИзчакай 60 СЕКУНДИ преди да тестваш!")
print("Passenger трябва да reload-не всички Python модули.")
print("\nСлед 60 секунди:")
print("1. Отвори НОВ Incognito прозорец")
print("2. Отиди на https://bghrana.com/register")
print("3. Натисни Facebook бутона")
print("4. Трябва да отвори FACEBOOK OAuth (не Google!)")
print("=" * 70)
