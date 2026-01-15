#!/usr/bin/env python
"""
Скрипт за създаване и прилагане на миграции на production сървъра
"""
import os
import sys
import django

# Настройка на Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.core.management import call_command

def main():
    print("=" * 60)
    print("Създаване и прилагане на миграции")
    print("=" * 60)
    
    try:
        # Стъпка 1: Създаване на миграции
        print("\n[1/2] Създаване на миграции...")
        call_command('makemigrations')
        print("✓ Миграциите са създадени успешно!")
        
        # Стъпка 2: Прилагане на миграциите
        print("\n[2/2] Прилагане на миграциите...")
        call_command('migrate')
        print("✓ Миграциите са приложени успешно!")
        
        print("\n" + "=" * 60)
        print("Готово! Всички миграции са приложени.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Грешка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
