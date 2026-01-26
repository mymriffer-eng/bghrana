import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from catalog.models import Category, Product, Region, City

# Очистване на старите данни
Product.objects.all().delete()
Category.objects.all().delete()

# Създаване на главни категории
vegetables = Category.objects.create(name='Зеленчуци', description='Пресни зеленчуци от локални производители')
fruits = Category.objects.create(name='Плодове', description='Свежи плодове - ябълки, портокали, банани и др.')
meat = Category.objects.create(name='Месо', description='Свинско,телешко,пилешко и други видове месо.')
fish = Category.objects.create(name='Риба', description='Свежа и замразена риба')
dairy = Category.objects.create(name='Млечни продукти', description='Мляко, сирене, йогурт и масло')
honey = Category.objects.create(name='Мед', description='Натурален пчелен мед')
winter = Category.objects.create(name='Зимнина', description='Консервирани продукти и заготовки')
other = Category.objects.create(name='Други', description='Други хранителни продукти')

# Създаване на подкатегории за зеленчуци
subcats_vegetables = [
    'Боб', 'Грах', 'Зелен лук', 'Зелена салата', 'Зелен фасул', 'Зеле', 'Картофи', 
    'Копър', 'Краставици', 'Лук', 'Магданоз', 'Мента', 'Морков', 'Патладжан', 
    'Пипер', 'Репички', 'Рукола', 'Ряпа', 'Спанак', 'Тиквички', 'Цвекло', 'Чесън', 'Домати'
]

for subcat_name in subcats_vegetables:
    Category.objects.create(name=subcat_name, parent=vegetables)

# Създаване на подкатегории за плодове
subcats_fruits = [
    'Авокадо', 'Ябълки', 'Боровинки', 'Вишни', 'Грозде', 'Дюли', 
    'Диня', 'Кайсии', 'Череши', 'Къпини', 'Круши', 
    'Малини', 'Нектарини', 'Пъпеш', 'Праскови', 'Сливи', 'Смокини', 'Черници'
]

for subcat_name in subcats_fruits:
    Category.objects.create(name=subcat_name, parent=fruits)

# Създаване на подкатегории за месо
subcats_meat = [
    'Агнешко', 'Говеждо', 'Дивеч', 'Заешко', 'Козе', 
    'Конско', 'Овче', 'Патешко', 'Пилешко', 'Пуешко', 'Свинско', 'Телешко'
]

for subcat_name in subcats_meat:
    Category.objects.create(name=subcat_name, parent=meat)

# Създаване на подкатегории за риба
subcats_fish = [
    'Бял амур', 'Бяла риба', 'Вилтица', 'Каракуда', 'Кефал', 
    'Костур', 'Лаврак', 'Лефер', 'Миди', 'Октопод', 
    'Попче', 'Пъстърва', 'Сафрид', 'Сом', 'Скариди', 
    'Толстолоб', 'Трицона', 'Щука', 'Черноморска врана', 'Чернокоп', 'Шаран'
]

for subcat_name in subcats_fish:
    Category.objects.create(name=subcat_name, parent=fish)

# Създаване на подкатегории за млечни продукти
subcats_dairy = [
    'Краве сирене', 'Овче сирене', 'Козе сирене', 'Кашкавал', 'Жълти сирена', 
    'Извара', 'Прясно краве мляко', 'Прясно овче мляко', 'Прясно козе мляко', 'Кисело мляко'
]

for subcat_name in subcats_dairy:
    Category.objects.create(name=subcat_name, parent=dairy)

# Създаване на подкатегории за мед
subcats_honey = [
    'Натурален мед', 'Медни продукти'
]

for subcat_name in subcats_honey:
    Category.objects.create(name=subcat_name, parent=honey)
# Създаване на подкатегории за зимнина
subcats_winter = [
    'Туршия', 'Зеленчукови', 'Компоти', 'Сладки', 'Месни'
]

for subcat_name in subcats_winter:
    Category.objects.create(name=subcat_name, parent=winter)

# Създаване на тестови продукти

# Създаване на области (Regions)
region_names = [
    'Благоевград', 'Бургас', 'Варна', 'Велико Търново', 'Видин', 'Враца', 'Габрово', 'Добрич',
    'Кърджали', 'Кюстендил', 'Ловеч', 'Монтана', 'Пазарджик', 'Перник', 'Плевен', 'Пловдив',
    'Разград', 'Русе', 'Силистра', 'Сливен', 'Смолян', 'София (област)', 'София-град', 'Стара Загора',
    'Търговище', 'Хасково', 'Шумен', 'Ямбол'
]

for rname in region_names:
    Region.objects.get_or_create(name=rname)

# Създаване на градове (Cities) по области
blagoevgrad_region = Region.objects.get(name='Благоевград')
blagoevgrad_cities = [
    'Благоевград', 'Банско', 'Гоце Делчев', 'Петрич', 'Сандански', 'Разлог', 'Якоруда',
    'Белица', 'Симитли', 'Хаджидимово', 'Кресна', 'Струмяни', 'Сатовча', 'Гърмен'
]

for city_name in blagoevgrad_cities:
    City.objects.get_or_create(name=city_name, region=blagoevgrad_region)

# Бургас градове
burgas_region = Region.objects.get(name='Бургас')
burgas_cities = [
    'Айтос', 'Бургас', 'Карнобат', 'Камено', 'Несебър', 'Поморие', 'Приморско', 'Созопол',
    'Средец', 'Сунгурларе', 'Царево', 'Руен', 'Малко Търново'
]

for city_name in burgas_cities:
    City.objects.get_or_create(name=city_name, region=burgas_region)

# Варна градове
varna_region = Region.objects.get(name='Варна')
varna_cities = [
    'Аксаково', 'Варна', 'Белослав', 'Бяла', 'Ветрино', 'Вълчи дол', 'Девня', 'Долни чифлик',
    'Дългопол', 'Провадия', 'Суворово', 'Аврен'
]

for city_name in varna_cities:
    City.objects.get_or_create(name=city_name, region=varna_region)

# Велико Търново градове
veliko_tarnovo_region = Region.objects.get(name='Велико Търново')
veliko_tarnovo_cities = [
    'Велико Търново', 'Горна Оряховица', 'Елена', 'Златарица', 'Лясковец', 'Павликени',
    'Полски тръмбеш', 'Свищов', 'Стражица', 'Сухиндол'
]

for city_name in veliko_tarnovo_cities:
    City.objects.get_or_create(name=city_name, region=veliko_tarnovo_region)

# Видин градове
vidin_region = Region.objects.get(name='Видин')
vidin_cities = [
    'Видин', 'Белоградчик', 'Бойница', 'Брегово', 'Грамада', 'Димово', 'Кула', 'Макреш',
    'Ново село', 'Ружинци', 'Чупрене'
]

for city_name in vidin_cities:
    City.objects.get_or_create(name=city_name, region=vidin_region)

# Враца градове
vraca_region = Region.objects.get(name='Враца')
vraca_cities = [
    'Враца', 'Бяла слатина', 'Козлодуй', 'Криводол', 'Мездра', 'Оряхово', 'Роман', 'Мизия',
    'Борован', 'Хайредин'
]

for city_name in vraca_cities:
    City.objects.get_or_create(name=city_name, region=vraca_region)

# Габрово градове
gabrovo_region = Region.objects.get(name='Габрово')
gabrovo_cities = [
    'Габрово', 'Трявна', 'Севлиево', 'Дряново'
]

for city_name in gabrovo_cities:
    City.objects.get_or_create(name=city_name, region=gabrovo_region)

# Добрич градове
dobrich_region = Region.objects.get(name='Добрич')
dobrich_cities = [
    'Добрич', 'Балчик', 'Каварна', 'Генерал Тошево', 'Шабла', 'Крушари', 'Тервел'
]

for city_name in dobrich_cities:
    City.objects.get_or_create(name=city_name, region=dobrich_region)

# Кърджали градове
kardzhali_region = Region.objects.get(name='Кърджали')
kardzhali_cities = [
    'Кърджали', 'Момчилград', 'Ардино', 'Джебел', 'Крумовград', 'Кирково', 'Черноочене'
]

for city_name in kardzhali_cities:
    City.objects.get_or_create(name=city_name, region=kardzhali_region)

# Кюстендил градове
kyustendil_region = Region.objects.get(name='Кюстендил')
kyustendil_cities = [
    'Кюстендил', 'Бобов дол', 'Бобошево', 'Дупница', 'Кочериново', 'Невестино', 'Рила',
    'Сапарева баня', 'Трекляно'
]

for city_name in kyustendil_cities:
    City.objects.get_or_create(name=city_name, region=kyustendil_region)

# Ловеч градове
lovech_region = Region.objects.get(name='Ловеч')
lovech_cities = [
    'Ловеч', 'Троян', 'Тетевен', 'Луковит', 'Ябланица', 'Априлци', 'Летница', 'Угърчин',
    'Плачковци'
]

for city_name in lovech_cities:
    City.objects.get_or_create(name=city_name, region=lovech_region)

# Монтана градове
montana_region = Region.objects.get(name='Монтана')
montana_cities = [
    'Монтана', 'Берковица', 'Бойчиновци', 'Вълчедръм', 'Лом', 'Медковец', 'Мизия', 'Якимово',
    'Чипровци', 'Георги Дамяново', 'Владимирово'
]

for city_name in montana_cities:
    City.objects.get_or_create(name=city_name, region=montana_region)

# Пазарджик градове
pazardzhik_region = Region.objects.get(name='Пазарджик')
pazardzhik_cities = [
    'Пазарджик', 'Велинград', 'Пещера', 'Батак', 'Брацигово', 'Лесичово',
    'Панагюрище', 'Септември', 'Стрелча', 'Ракитово'
]

for city_name in pazardzhik_cities:
    City.objects.get_or_create(name=city_name, region=pazardzhik_region)

# Перник градове
pernik_region = Region.objects.get(name='Перник')
pernik_cities = [
    'Перник', 'Радомир', 'Брезник', 'Трън', 'Земен', 'Ковачевци', 'Трекляно'
]

for city_name in pernik_cities:
    City.objects.get_or_create(name=city_name, region=pernik_region)

# Плевен градове
pleven_region = Region.objects.get(name='Плевен')
pleven_cities = [
    'Плевен', 'Долна Митрополия', 'Гулянци', 'Кнежа', 'Левски', 'Никопол',
    'Пордим', 'Червен бряг', 'Искър', 'Белене'
]

for city_name in pleven_cities:
    City.objects.get_or_create(name=city_name, region=pleven_region)

# Създаване на тестови продукти
products_data = [
    # Зеленчуци
    {'title': 'Домати', 'description': 'Пресни домати, идеални за салати и готвене. Местни, без пестициди', 'price': 4.99, 'category': vegetables},
    {'title': 'Краставици', 'description': 'Свежи краставици директно от градина', 'price': 3.50, 'category': vegetables},
    {'title': 'Морков', 'description': 'Сладка морков, богата на витамини', 'price': 2.99, 'category': vegetables},
    {'title': 'Капуста', 'description': 'Свежа белокочанка, идеална за салати', 'price': 3.99, 'category': vegetables},
    
    # Плодове
    {'title': 'Ябълки Braeburn', 'description': 'Хрупкави и сладки ябълки от местни градини', 'price': 5.99, 'category': fruits},
    {'title': 'Портокали', 'description': 'Соковити портокали, богати на витамин C', 'price': 6.50, 'category': fruits},
    {'title': 'Банани', 'description': 'Жълти банани, идеални за всяка възраст', 'price': 3.99, 'category': fruits},
    {'title': 'Грозде', 'description': 'Свежо грозде без семки', 'price': 8.99, 'category': fruits},
    
    # Месо
    {'title': 'Пилешки гърди', 'description': 'Нежно пилешко месо, богато на протеин', 'price': 12.99, 'category': meat},
    {'title': 'Свинско месо', 'description': 'Качествено свинско месо за печене', 'price': 14.99, 'category': meat},
    {'title': 'Говяжко месо', 'description': 'Премиум говяжко месо, идеално за стек', 'price': 19.99, 'category': meat},
    {'title': 'Кифла', 'description': 'Традиционна българска кифла, фино подправена', 'price': 9.99, 'category': meat},
    
    # Риба
    {'title': 'Пъстърва', 'description': 'Свежа пъстърва с нежно месо', 'price': 16.99, 'category': fish},
    {'title': 'Скумрия', 'description': 'Скумрия, богата на омега-3 мастни киселини', 'price': 11.99, 'category': fish},
    {'title': 'Сьомга', 'description': 'Норвежка сьомга, наситена с полезни вещества', 'price': 24.99, 'category': fish},
    
    # Млечни продукти
    {'title': 'Свежо мляко', 'description': 'Пастеризирано говяжко мляко, богато на калций', 'price': 2.50, 'category': dairy},
    {'title': 'Кашкавал', 'description': 'Традиционен български кашкавал', 'price': 13.99, 'category': dairy},
    {'title': 'Йогурт натурален', 'description': 'Домашен йогурт без консерванти', 'price': 3.99, 'category': dairy},
    {'title': 'Масло', 'description': 'Кравско масло от локални производители', 'price': 7.99, 'category': dairy},
    
    # Мед
    {'title': 'Цветен мед', 'description': 'Натурален пчелен мед от диви цветя', 'price': 18.99, 'category': honey},
    {'title': 'Липов мед', 'description': 'Чист липов мед с успокояващи свойства', 'price': 22.99, 'category': honey},
    
    # Зимнина
    {'title': 'Компот ябълка-груша', 'description': 'Домашен компот от локални плодове', 'price': 5.99, 'category': winter},
    {'title': 'Мариновани краставици', 'description': 'Традиционна консервирана зимнина', 'price': 4.50, 'category': winter},
    {'title': 'Сок от ягода', 'description': 'Натурален сок от всички ягодови видове', 'price': 6.99, 'category': winter},
]

for data in products_data:
    Product.objects.get_or_create(title=data['title'], defaults=data)

print("✅ Хранителни продукти със подкатегории са създадени успешно!")
