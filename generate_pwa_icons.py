#!/usr/bin/env python
"""
Скрипт за генериране на PWA икони
Използва produkti_2025.jpg от media/products/
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Създай директория за икони
icons_dir = 'catalog/static/icons'
os.makedirs(icons_dir, exist_ok=True)

# Размери за генериране
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

# Опит 1: Използвай produkti_2025.jpg
try:
    img = Image.open('media/products/produkti_2025.jpg')
    
    # Направи квадратна (crop center)
    width, height = img.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    img_cropped = img.crop((left, top, left + size, top + size))
    
    for size in sizes:
        resized = img_cropped.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f'{icons_dir}/icon-{size}x{size}.png', 'PNG')
        print(f'✅ Създадена: icon-{size}x{size}.png')
    
    print('\n🎉 Всички икони са генерирани успешно от produkti_2025.jpg!')

except FileNotFoundError:
    # Опит 2: Създай прости икони със зелен фон и emoji
    print('❌ produkti_2025.jpg не е намерен. Създавам прости икони...')
    
    for size in sizes:
        # Създай нова снимка със зелен фон
        img = Image.new('RGB', (size, size), color='#0dd843')
        draw = ImageDraw.Draw(img)
        
        # Добави бял кръг в средата
        margin = size // 8
        draw.ellipse([margin, margin, size-margin, size-margin], 
                     fill='white', outline='#0dd843', width=size//20)
        
        # Опит да добавим текст
        try:
            font_size = size // 3
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Добави "🥬" или "Х" в центъра
        text = "🥬"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        try:
            draw.text(position, text, fill='#0dd843', font=font)
        except:
            # Ако emoji не работи, използвай "Х"
            text = "Х"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((size - text_width) // 2, (size - text_height) // 2)
            draw.text(position, text, fill='#0dd843', font=font)
        
        img.save(f'{icons_dir}/icon-{size}x{size}.png', 'PNG')
        print(f'✅ Създадена: icon-{size}x{size}.png')
    
    print('\n🎉 Генерирани простички икони със зелен фон!')
    print('💡 Съвет: Можеш да замениш иконите с по-добри от https://www.pwabuilder.com/imageGenerator')

print(f'\n📂 Иконите са в: {os.path.abspath(icons_dir)}')
