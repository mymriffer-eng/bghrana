#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Проверка на снимки за конкретна обява
Използвай: python check_product_images.py 54
"""

import os
import sys
import django

# Setup Django
os.chdir('/home/bghranac/repositories/bghrana')
sys.path.insert(0, '/home/bghranac/repositories/bghrana')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Product, ProductImage
from django.conf import settings

def check_product_images(product_id):
    print(f"\n{'='*60}")
    print(f"ПРОВЕРКА НА СНИМКИ ЗА ОБЯВА #{product_id}")
    print(f"{'='*60}\n")
    
    try:
        product = Product.objects.get(pk=product_id)
        print(f"✓ Обява намерена: {product.title}")
        print(f"  Собственик: {product.owner.username if product.owner else 'N/A'}")
        print(f"  Активна: {product.is_active}")
        print(f"\n")
    except Product.DoesNotExist:
        print(f"✗ Обява #{product_id} не съществува в базата данни!")
        return
    
    images = ProductImage.objects.filter(product=product).order_by('order')
    
    if not images.exists():
        print("✗ Няма регистрирани снимки в базата данни за тази обява!")
        return
    
    print(f"Брой снимки в БД: {images.count()}\n")
    
    for idx, img in enumerate(images, 1):
        print(f"--- Снимка #{idx} ---")
        print(f"  ID: {img.id}")
        print(f"  Order: {img.order}")
        print(f"  DB Path: {img.image.name}")
        print(f"  URL: {img.image.url}")
        
        # Проверка дали файлът съществува
        full_path = os.path.join(settings.MEDIA_ROOT, img.image.name)
        print(f"  Full Path: {full_path}")
        
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            file_perms = oct(os.stat(full_path).st_mode)[-3:]
            print(f"  ✓ Файлът съществува")
            print(f"  Размер: {file_size:,} bytes")
            print(f"  Права: {file_perms}")
        else:
            print(f"  ✗ ФАЙЛЪТ НЕ СЪЩЕСТВУВА!")
        
        print()
    
    print(f"{'='*60}")
    print("ПРЕПОРЪКИ:")
    print(f"{'='*60}")
    print("Ако файловете липсват:")
    print("1. Провери дали са били изтрити случайно")
    print("2. Провери backup-ите")
    print("3. Поискай собственика да качи снимките отново")
    print("\nАко файловете са с грешни права:")
    print("  chmod 644 /home/bghranac/repositories/bghrana/media/products/*")
    print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Използвай: python check_product_images.py <product_id>")
        print("Пример: python check_product_images.py 54")
        sys.exit(1)
    
    product_id = int(sys.argv[1])
    check_product_images(product_id)
