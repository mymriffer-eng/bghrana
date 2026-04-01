"""
Финален фикс за Facebook Login - пълен reboot на Passenger
"""
import subprocess
import time
import os

print("=" * 70)
print("ФИНАЛЕН FIX ЗА FACEBOOK LOGIN - HARD REBOOT")
print("=" * 70)

base_path = os.path.expanduser('~/repositories/bghrana')

# 1. Stop всички Python процеси (ако можем)
print("\n1. Изтриване на всички cache файлове...")
subprocess.run('find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true', 
               shell=True, cwd=base_path)
subprocess.run('find . -name "*.pyc" -delete 2>/dev/null || true', 
               shell=True, cwd=base_path)
print("   ✓ Cache изтрит")

# 2. Създай специален passenger_wsgi.py който форсира reload
print("\n2. Модифициране на passenger_wsgi.py...")
wsgi_content = """
import sys
import os

# IMPORTANT: Clear all cached modules
for module in list(sys.modules.keys()):
    if 'allauth' in module or 'socialaccount' in module:
        del sys.modules[module]

# Setup paths
INTERP = os.path.expanduser("~/virtualenv/repositories/bghrana/3.11/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.expanduser('~/repositories/bghrana'))
sys.path.insert(0, os.path.expanduser('~/virtualenv/repositories/bghrana/3.11/bin'))
sys.path.insert(0, os.path.expanduser('~/virtualenv/repositories/bghrana/3.11/lib/python3.11/site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'products.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""

wsgi_path = os.path.join(base_path, 'passenger_wsgi.py')
with open(wsgi_path, 'w') as f:
    f.write(wsgi_content)
print("   ✓ passenger_wsgi.py обновен")

# 3. Множество restarts
print("\n3. Рестартиране на Passenger (10 пъти)...")
restart_file = os.path.join(base_path, 'tmp/restart.txt')
os.makedirs(os.path.dirname(restart_file), exist_ok=True)

for i in range(10):
    with open(restart_file, 'w') as f:
        f.write(f'HARD RESTART {i+1} at {time.time()}\n')
    print(f"   Restart {i+1}/10...")
    time.sleep(2)

print("\n" + "=" * 70)
print("ГОТОВО!")
print("=" * 70)
print("\nПОВАЖНО:")
print("1. Изчакай 2 МИНУТИ преди да тестваш!")
print("2. Отвори НАПЪЛНО НОВ браузър (затвори всички прозорци)")
print("3. Отиди на https://bghrana.com/register")
print("4. Провери дали има Facebook бутон")
print("5. Ако НЯМА - изчисти browser cache и презареди")
print("=" * 70)
