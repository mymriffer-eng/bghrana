#!/usr/bin/env python3
"""
Проверка дали бутоните за споделяне са в темплейта
"""

template_path = 'catalog/templates/catalog/product_detail.html'

try:
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '📤 Сподели обявата:' in content:
        print("✅ Бутоните за споделяне СА в темплейта")
        print("\nТова означава че локално промените са налични.")
        print("\n🔧 На сървъра трябва да направиш:")
        print("   1. git pull")
        print("   2. touch tmp/restart.txt")
        print("   3. Изчакай 10-15 секунди")
        print("   4. Refresh страницата с Ctrl+Shift+R")
    else:
        print("❌ Бутоните за споделяне НЕ СА в темплейта")
        print("\nНещо се е объркало в кода.")
        
    # Покажи секцията с бутоните
    if 'Social Share Buttons' in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Social Share Buttons' in line:
                print("\n📋 Намерена секция на ред", i+1)
                print("Показвам 5 реда преди и след:")
                for j in range(max(0, i-5), min(len(lines), i+15)):
                    print(f"{j+1:4d}: {lines[j]}")
                break
                
except Exception as e:
    print(f"❌ Грешка: {e}")
