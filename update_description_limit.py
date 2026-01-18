#!/usr/bin/env python
"""
Скрипт за актуализиране на лимита на описанието от 250 на 500 символа
"""
import os
import sys
import django

# Добави пътя до проекта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Настрой Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from django.core.management import call_command

def main():
    print("=" * 60)
    print("Актуализиране на лимита на описанието от 250 на 500 символа")
    print("=" * 60)
    print()
    
    try:
        # Създаване на миграции
        print("Стъпка 1: Създаване на миграции...")
        call_command('makemigrations')
        print("✓ Миграциите са създадени успешно")
        print()
        
        # Прилагане на миграции
        print("Стъпка 2: Прилагане на миграциите...")
        call_command('migrate')
        print("✓ Миграциите са приложени успешно")
        print()
        
        print("=" * 60)
        print("Актуализацията завърши успешно!")
        print("Сега полето за описание приема до 500 символа")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Грешка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
