import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Category, Product

# Очистване на старите данни
Product.objects.all().delete()
Category.objects.all().delete()

# Създаване на категории
categories = {
    'Зеленчуци': 'Пресни зеленчуци от локални производители',
    'Плодове': 'Свежи плодове - ябълки, портокали, банани и др.',
    'Месо': 'Свинско,телешко,пилешко и други видове месо.',
    'Риба': 'Свежа и замразена риба',
    'Млечни продукти': 'Мляко, сирене, йогурт и масло',
    'Мед': 'Натурален пчелен мед',
    'Зимнина': 'Консервирани продукти и заготовки',
    'Други': 'Други хранителни продукти',
}

cats = {}
for name, desc in categories.items():
    cat, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
    cats[name] = cat

# Създаване на тестови продукти
products_data = [
    # Зеленчуци
    {'title': 'Домати', 'description': 'Пресни домати, идеални за салати и готвене. Местни, без пестициди', 'price': 4.99, 'category': cats['Зеленчуци']},
    {'title': 'Краставици', 'description': 'Свежи краставици директно от градина', 'price': 3.50, 'category': cats['Зеленчуци']},
    {'title': 'Морков', 'description': 'Сладка морков, богата на витамини', 'price': 2.99, 'category': cats['Зеленчуци']},
    {'title': 'Капуста', 'description': 'Свежа белокочанка, идеална за салати', 'price': 3.99, 'category': cats['Зеленчуци']},
    
    # Плодове
    {'title': 'Ябълки Брaeburn', 'description': 'Хрупкави и сладки ябълки от местни градини', 'price': 5.99, 'category': cats['Плодове']},
    {'title': 'Портокали', 'description': 'Соковити портокали, богати на витамин C', 'price': 6.50, 'category': cats['Плодове']},
    {'title': 'Банани', 'description': 'Жълти банани, идеални за всяка възраст', 'price': 3.99, 'category': cats['Плодове']},
    {'title': 'Грозде', 'description': 'Свежо грозде без семки', 'price': 8.99, 'category': cats['Плодове']},
    
    # Месо
    {'title': 'Пилешки гърди', 'description': 'Нежно пилешко месо, богато на протеин', 'price': 12.99, 'category': cats['Месо']},
    {'title': 'Свинско месо', 'description': 'Качествено свинско месо за печене', 'price': 14.99, 'category': cats['Месо']},
    {'title': 'Говяжко месо', 'description': 'Премиум говяжко месо, идеално за стек', 'price': 19.99, 'category': cats['Месо']},
    {'title': 'Кифла', 'description': 'Традиционна българска кифла, фино подправена', 'price': 9.99, 'category': cats['Месо']},
    
    # Риба
    {'title': 'Пъстърва', 'description': 'Свежа пъстърва с нежно месо', 'price': 16.99, 'category': cats['Риба']},
    {'title': 'Скумрия', 'description': 'Скумрия, богата на омега-3 мастни киселини', 'price': 11.99, 'category': cats['Риба']},
    {'title': 'Сьомга', 'description': 'Норвежка сьомга, наситена с полезни вещества', 'price': 24.99, 'category': cats['Риба']},
    
    # Млечни продукти
    {'title': 'Свежо мляко', 'description': 'Пастеризирано говяжко мляко, богато на калций', 'price': 2.50, 'category': cats['Млечни продукти']},
    {'title': 'Кашкавал', 'description': 'Традиционен български кашкавал', 'price': 13.99, 'category': cats['Млечни продукти']},
    {'title': 'Йогурт натурален', 'description': 'Домашен йогурт без консерванти', 'price': 3.99, 'category': cats['Млечни продукти']},
    {'title': 'Масло', 'description': 'Кравско масло от локални производители', 'price': 7.99, 'category': cats['Млечни продукти']},
    
    # Мед
    {'title': 'Цветен мед', 'description': 'Натурален пчелен мед от диви цветя', 'price': 18.99, 'category': cats['Мед']},
    {'title': 'Липов мед', 'description': 'Чист липов мед с успокояващи свойства', 'price': 22.99, 'category': cats['Мед']},
    
    # Зимнина
    {'title': 'Компот ябълка-груша', 'description': 'Домашен компот от локални плодове', 'price': 5.99, 'category': cats['Зимнина']},
    {'title': 'Мариновани краставици', 'description': 'Традиционна консервирана зимнина', 'price': 4.50, 'category': cats['Зимнина']},
    {'title': 'Сок от ягода', 'description': 'Натурален сок от всички ягодови видове', 'price': 6.99, 'category': cats['Зимнина']},
]

for data in products_data:
    Product.objects.get_or_create(title=data['title'], defaults=data)

print("✅ Хранителни продукти са създадени успешно!")
