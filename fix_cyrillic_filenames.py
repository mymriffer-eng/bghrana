#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Преименува кирилски имена на файлове на латиница
Използвай: python fix_cyrillic_filenames.py <product_id>
"""

import os
import sys
import django
import re

# Setup Django
os.chdir('/home/bghranac/repositories/bghrana')
sys.path.insert(0, '/home/bghranac/repositories/bghrana')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Product, ProductImage
from django.conf import settings

# Транслитерационна таблица (ако библиотеката липсва)
CYRILLIC_TO_LATIN = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh', 'з': 'z',
    'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
    'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
    'ш': 'sh', 'щ': 'sht', 'ъ': 'a', 'ь': 'y', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ж': 'Zh', 'З': 'Z',
    'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
    'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
    'Ш': 'Sh', 'Щ': 'Sht', 'Ъ': 'A', 'Ь': 'Y', 'Ю': 'Yu', 'Я': 'Ya'
}

def transliterate_filename(filename):
    """Транслитерира кирилско име на файл на латиница"""
    name, ext = os.path.splitext(filename)
    
    # Преобразувай всяка буква
    transliterated = ''.join(CYRILLIC_TO_LATIN.get(char, char) for char in name)
    
    # Почисти специални символи (освен - и _)
    transliterated = re.sub(r'[^\w\-_]', '_', transliterated)
    
    return transliterated + ext

def fix_product_images(product_id, dry_run=True):
    print(f"\n{'='*60}")
    print(f"ПРЕИМЕНУВАНЕ НА ФАЙЛОВЕ ЗА ОБЯВА #{product_id}")
    print(f"{'='*60}\n")
    
    if dry_run:
        print("⚠️  DRY RUN MODE - само преглед, без промени")
        print("За реално изпълнение: python fix_cyrillic_filenames.py <id> --execute\n")
    
    try:
        product = Product.objects.get(pk=product_id)
        print(f"✓ Обява: {product.title}\n")
    except Product.DoesNotExist:
        print(f"✗ Обява #{product_id} не съществува!")
        return
    
    images = ProductImage.objects.filter(product=product).order_by('order')
    
    if not images.exists():
        print("✗ Няма снимки за тази обява!")
        return
    
    changes_made = 0
    
    for idx, img in enumerate(images, 1):
        old_filename = os.path.basename(img.image.name)
        
        # Провери дали има кирилица в името
        has_cyrillic = any(char in CYRILLIC_TO_LATIN for char in old_filename)
        
        if not has_cyrillic:
            print(f"[{idx}] ✓ {old_filename} - вече е на латиница")
            continue
        
        new_filename = transliterate_filename(old_filename)
        old_path = os.path.join(settings.MEDIA_ROOT, img.image.name)
        new_path = os.path.join(settings.MEDIA_ROOT, 'products', new_filename)
        
        print(f"\n[{idx}] Промяна:")
        print(f"  Старо: {old_filename}")
        print(f"  Нов:   {new_filename}")
        
        if not dry_run:
            if os.path.exists(old_path):
                # Преименувай файла
                os.rename(old_path, new_path)
                
                # Обнови БД
                img.image.name = f'products/{new_filename}'
                img.save()
                
                print(f"  ✓ Файлът е преименуван")
                print(f"  ✓ БД е обновена")
                changes_made += 1
            else:
                print(f"  ✗ Файлът не съществува: {old_path}")
        else:
            print(f"  → Ще се преименува на: {new_path}")
    
    print(f"\n{'='*60}")
    if dry_run:
        print("DRY RUN завърши успешно.")
        print("За реално изпълнение добави --execute")
    else:
        print(f"✓ Готово! Променени файлове: {changes_made}")
        print(f"\nПроверете обявата: https://bghrana.com/product/{product_id}/")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Използвай: python fix_cyrillic_filenames.py <product_id> [--execute]")
        print("Пример: python fix_cyrillic_filenames.py 54 --execute")
        sys.exit(1)
    
    product_id = int(sys.argv[1])
    execute = '--execute' in sys.argv
    
    fix_product_images(product_id, dry_run=not execute)
