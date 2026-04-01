# 🔍 ОДИТ НА КОДА - bghrana.com (01.04.2026)

## ✅ ПРОВЕРЕНИ ФАЙЛОВЕ

1. **products/settings.py** - Django конфигурация
2. **catalog/models.py** - Database модели
3. **catalog/views.py** - Бизнес логика  
4. **catalog/forms.py** - Форми и валидация
5. **products/urls.py** + **catalog/urls.py** - URL routing
6. **catalog/templates/** - HTML темплейти
7. **catalog/migrations/** - Database migrations
8. **requirements.txt** - Python пакети

---

## ❌ КРИТИЧНИ ПРОБЛЕМИ

### 1. ❌ Form/Template несъответствие (ФИКСИРАНО)
**Статус:** ✅ Поправено в commit e6f3050  
**Проблем:** `register.html` показваше `form.username`, но `CustomUserCreationForm` има само `email` и `password1`  
**Ефект:** Регистрационната форма показваше невалидни полета  
**Решение:** Премахнато username поле от темплейта

### 2. ❌ Facebook Login SocialApp.DoesNotExist
**Статус:** 🔄 НЕ РЕШЕН - чака Passenger restart  
**Проблем:** Passenger кешира стара версия на allauth без Facebook provider  
**Ефект:** `/accounts/login/` краш при рендериране на Facebook бутон (премахнат временно)  
**Верификация:**
- ✅ INSTALLED_APPS съдържа 'allauth.socialaccount.providers.facebook'
- ✅ SOCIALACCOUNT_PROVIDERS има Facebook конфигурация
- ✅ База данни: SocialApp за Facebook съществува (client_id=1233729711819329)
- ❌ Passenger provider registry НЕ вижда Facebook

**Решение:**
```bash
# В cPanel → Setup Python App → STOP → Wait 10s → START
# ИЛИ contact cPanel support за Python process reload
```

### 3. ⚠️ Django версия в коментари
**Статус:** Незначително  
**Проблем:** settings.py коментар казва Django 6.0, но requirements.txt има 5.1.4  
**Ефект:** Подвеждащ коментар  

### 4. ⚠️ Email verification race condition
**Статус:** Потенциален риск  
**Проблем:** register view изтрива потребител при email failure, но може да има timing issues  
**Ефект:** Непредвидимо поведение при проблеми с SMTP  
**Препоръка:** Добави try/except wrapper и logging

---

## ✅ ВАЛИДНИ КОМПОНЕНТИ

### Models (catalog/models.py)
- ✅ Product model - всички полета правилни
- ✅ SEOPage model - CTA button fields добавени коректно
- ✅ Category/Region/City - slugs и relations OK
- ✅ Transliteration функции за Cyrillic filenames

### Forms (catalog/forms.py)
- ✅ CustomUserCreationForm - auto-username генериране работи
- ✅ ProductForm - валидации за XSS/HTML injection
- ✅ Password reduction на 6 chars (MinimumLengthValidator)

### Views (catalog/views.py)
- ✅ Product CRUD operations
- ✅ Registration flow с email verification
- ✅ Profile management
- ✅ Facebook data deletion endpoints (за Meta compliance)

### URLs
- ✅ products/urls.py - allauth integration правилна
- ✅ catalog/urls.py - django.contrib.auth.urls disabled (правилно)
- ✅ SEO URLs (robots.txt, sitemap.xml)

### Templates  
- ✅ Base layout и navigation
- ✅ Google OAuth buttons работят
- ❌ Facebook buttons премахнати временно (до Passenger restart)
- ✅ register.html ФИКСИРАН (премахнат username field)

### Migrations
- ✅ 0001-0013 migrations се прилагат последователно
- ✅ 0013 добавя CTA button fields
- ✅ Няма конфликти

### Configuration (settings.py)
- ✅ INSTALLED_APPS пълен списък
- ✅ SOCIALACCOUNT_PROVIDERS за Google + Facebook
- ✅ Database MySQL/MariaDB config
- ✅ WhiteNoise за static files
- ✅ Email SMTP правилно конфигуриран
- ✅ Security headers за production

---

## 📋 DEPLOY CHECKLIST (production)

След `git pull` на production:

1. ✅ `git pull origin master` - вече има commit e6f3050
2. ⚠️ **ВАЖНО:** Full Passenger restart (не touch tmp/restart.txt)
   ```bash
   # cPanel → Setup Python App → STOP → Wait 10s → START
   ```
3. ✅ Провери `/accounts/login/` работи ли (без Facebook бутон)
4. ✅ Тествай регистрация с email/password
5. ✅ Тествай Google Login
6. 🔄 След Passenger restart - върни Facebook бутоните и тествай

---

## 🔧 ТЕХНИЧЕСКИ ДЕТАЙЛИ

### Пакети (requirements.txt)
```
Django==5.1.4
django-allauth==65.0.2
Pillow==10.0.0
PyMySQL==1.1.0
whitenoise==6.6.0
python-decouple==3.8
```

### Database Schema
- auth_user (Django built-in)
- catalog_product (главен модел)
- catalog_productimage (1-to-many)
- catalog_category, catalog_region, catalog_city
- catalog_seopage (динамични SEO страници)
- catalog_userprofile (1-to-1 с User)
- socialaccount_socialapp (Google + Facebook)
- socialaccount_socialaccount (user social logins)

### URLs Schema
```
/                           → ProductListView
/register/                  → register view (custom)
/accounts/login/            → allauth login
/accounts/google/login/     → Google OAuth
/accounts/facebook/login/   → Facebook OAuth (BROKEN - Passenger cache)
/politika-za-poveritelnost/ → privacy_policy
/data-deletion/             → Facebook data deletion
```

---

## 📝 NEXT STEPS

1. **Спешно:** Full Passenger restart на production за да зареди Facebook provider
2. **След restart:** Върни Facebook бутоните в темплейтите
3. **Опционално:** Fix Django version коментар в settings.py
4. **Опционално:** Подобри error handling в register view

---

**Генериран:** 01.04.2026  
**Commits:** cb0ca9e (Facebook removal), e6f3050 (username fix)  
**Статус:** ✅ Код валиден, 🔄 Чака Passenger restart
