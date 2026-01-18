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
        # Първо проверяваме дали има несинхронизирани миграции
        print("Стъпка 1: Проверка на състоянието на миграциите...")
        call_command('showmigrations', 'catalog')
        print()
        
        # Маркираме всички съществуващи миграции като приложени
        print("Стъпка 2: Синхронизиране на съществуващи миграции...")
        try:
            # Опитваме се да маркираме миграция 0008 като приложена ако съществува
            call_command('migrate', 'catalog', '0008', '--fake')
            print("✓ Миграция 0008 маркирана като приложена")
        except:
            print("  Миграция 0008 не съществува или вече е приложена")
        print()
        
        # Изтриваме евентуално създадената миграция 0009
        import glob
        migration_files = glob.glob('catalog/migrations/0009_*.py')
        if migration_files:
            print("Стъпка 3: Изтриване на конфликтна миграция 0009...")
            for file in migration_files:
                os.remove(file)
                print(f"  Изтрит: {file}")
            print()
        
        # Създаване на нова миграция само за описанието
        print("Стъпка 4: Създаване на миграция за увеличаване на лимита...")
        call_command('makemigrations', 'catalog', '--name', 'increase_description_limit')
        print("✓ Миграцията е създадена успешно")
        print()
        
        # Прилагане на новата миграция
        print("Стъпка 5: Прилагане на миграцията...")
        call_command('migrate', 'catalog')
        print("✓ Миграцията е приложена успешно")
        print()
        
        print("=" * 60)
        print("Актуализацията завърши успешно!")
        print("Сега полето за описание приема до 500 символа")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Грешка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
