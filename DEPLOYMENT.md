# 🚀 Deployment Guide - Food Products Marketplace

## Преди да качите сайта онлайн

### 1️⃣ Подготовка на локална среда

#### Инсталирайте новите пакети:
```bash
poetry add pillow python-decouple gunicorn whitenoise psycopg2-binary
```

#### Създайте `.env` файл (копирайте от `.env.example`):
```bash
cp .env.example .env
```

#### Редактирайте `.env` файла:
- Генерирайте нов SECRET_KEY: https://djecrety.ir/
- Задайте `DEBUG=False` за production
- Добавете вашия домейн в `ALLOWED_HOSTS`

### 2️⃣ Тестване локално в production режим

```bash
# Съберете статични файлове
poetry run python manage.py collectstatic --no-input

# Проверете конфигурацията
poetry run python manage.py check --deploy

# Стартирайте с gunicorn
poetry run gunicorn products.wsgi:application --bind 0.0.0.0:8000
```

### 3️⃣ Подготовка на база данни

#### За production използвайте PostgreSQL:
```sql
CREATE DATABASE foodproducts_db;
CREATE USER foodproducts_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE foodproducts_db TO foodproducts_user;
```

#### Приложете миграциите:
```bash
poetry run python manage.py migrate
```

#### Създайте superuser:
```bash
poetry run python manage.py createsuperuser
```

### 4️⃣ Email конфигурация

За Gmail използвайте App Password:
1. Отидете на https://myaccount.google.com/security
2. Включете 2-Step Verification
3. Генерирайте App Password
4. Добавете в `.env`:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

### 5️⃣ Deployment Options

#### Option A: PythonAnywhere (Безплатно за начало)
1. Качете кода във PythonAnywhere
2. Конфигурирайте Web app с WSGI файл
3. Задайте environment variables в Web tab
4. Добавете media файлове в static files mappings

#### Option B: DigitalOcean / Heroku
1. Създайте Droplet/App
2. Инсталирайте PostgreSQL
3. Конфигурирайте Nginx + Gunicorn
4. Задайте SSL с Let's Encrypt

#### Option C: Railway.app (Лесен deployment)
```bash
# Инсталирайте Railway CLI
npm install -g @railway/cli

# Login и deploy
railway login
railway init
railway up
```

### 6️⃣ Security Checklist

- [ ] `DEBUG=False` в production
- [ ] Нов `SECRET_KEY` (не хардкоднат)
- [ ] `ALLOWED_HOSTS` съдържа само вашия домейн
- [ ] PostgreSQL вместо SQLite
- [ ] SSL сертификат активиран (HTTPS)
- [ ] Email с реален SMTP (не console)
- [ ] `.env` файл не е в Git
- [ ] Media файлове с proper permissions
- [ ] Backups настроени

### 7️⃣ След deployment

```bash
# Проверете health
curl https://yourdomain.com/

# Мониторинг на логове
tail -f /var/log/gunicorn/error.log

# Проверка на грешки
poetry run python manage.py check --deploy
```

### 8️⃣ Редовна поддръжка

- Backup на базата данни всяка седмица
- Обновявайте Django и пакетите редовно
- Мониторинг на disk space за media файлове
- Проверка на security updates

### 📞 Контакт за проблеми
Email: galinpavloveto@gmail.com

---

## Полезни команди

### Локално тестване:
```bash
# Рестартиране на dev server
poetry run python manage.py runserver

# Проверка на миграции
poetry run python manage.py showmigrations

# Създаване на dump на базата
poetry run python manage.py dumpdata > backup.json
```

### Production:
```bash
# Collectstatic
poetry run python manage.py collectstatic --no-input --clear

# Проверка на deployment settings
poetry run python manage.py check --deploy

# Рестартиране на gunicorn
sudo systemctl restart gunicorn
```
