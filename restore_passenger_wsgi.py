"""
RESTORE оригиналния passenger_wsgi.py
"""
import os

print("=" * 70)
print("ВЪЗСТАНОВЯВАНЕ НА ОРИГИНАЛЕН passenger_wsgi.py")
print("=" * 70)

original_content = """import sys, os

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

wsgi_path = os.path.expanduser('~/repositories/bghrana/passenger_wsgi.py')

print(f"\nВъзстановяване на {wsgi_path}...")
with open(wsgi_path, 'w') as f:
    f.write(original_content)
print("✓ Файлът е възстановен")

# Restart
import time
restart_file = os.path.expanduser('~/repositories/bghrana/tmp/restart.txt')
os.makedirs(os.path.dirname(restart_file), exist_ok=True)

print("\nРестартиране на app...")
for i in range(3):
    with open(restart_file, 'w') as f:
        f.write(f'restore restart {i+1}\n')
    print(f"  Restart {i+1}/3...")
    time.sleep(2)

print("\n" + "=" * 70)
print("ГОТОВО! Изчакай 30 секунди и провери https://bghrana.com")
print("=" * 70)
