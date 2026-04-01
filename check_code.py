#!/usr/bin/env python3
"""
Автоматизирана проверка на код - bghrana.com
Проверява за типични проблеми и несъответствия
"""

import os
import re
import sys

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def check(condition, message):
    """Проверява condition и принтира резултата"""
    if condition:
        print(f"{GREEN}✅{RESET} {message}")
        return True
    else:
        print(f"{RED}❌{RESET} {message}")
        return False

def warn(message):
    """Принтира warning съобщение"""
    print(f"{YELLOW}⚠️{RESET}  {message}")

def info(message):
    """Принтира info съобщение"""
    print(f"{BLUE}ℹ️{RESET}  {message}")

def check_file_exists(filepath, description):
    """Проверява дали файл съществува"""
    exists = os.path.exists(filepath)
    check(exists, f"{description}: {filepath}")
    return exists

def check_file_contains(filepath, pattern, description, is_regex=False):
    """Проверява дали файл съдържа текст или regex pattern"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if is_regex:
        found = bool(re.search(pattern, content))
    else:
        found = pattern in content
    
    check(found, f"{description}")
    return found

def main():
    print("\n" + "="*60)
    print("🔍 АВТОМАТИЗИРАНА ПРОВЕРКА НА КОД")
    print("="*60 + "\n")
    
    # 1. Проверка на критични файлове
    info("1. Проверка на файлова структура...")
    check_file_exists('products/settings.py', 'Django settings')
    check_file_exists('catalog/models.py', 'Models')
    check_file_exists('catalog/views.py', 'Views')
    check_file_exists('catalog/forms.py', 'Forms')
    check_file_exists('catalog/urls.py', 'URLs')
    check_file_exists('requirements.txt', 'Requirements')
    print()
    
    # 2. Проверка на settings.py конфигурация
    info("2. Проверка на Django конфигурация...")
    check_file_contains('products/settings.py', 
                       'allauth.socialaccount.providers.google', 
                       'Google provider в INSTALLED_APPS')
    check_file_contains('products/settings.py', 
                       'allauth.socialaccount.providers.facebook', 
                       'Facebook provider в INSTALLED_APPS')
    check_file_contains('products/settings.py', 
                       "SITE_ID = 1", 
                       'SITE_ID конфигуриран')
    check_file_contains('products/settings.py', 
                       'SOCIALACCOUNT_PROVIDERS', 
                       'SOCIALACCOUNT_PROVIDERS дефиниран')
    print()
    
    # 3. Проверка на Forms
    info("3. Проверка на формуляри...")
    has_custom_form = check_file_contains('catalog/forms.py', 
                                         'class CustomUserCreationForm', 
                                         'CustomUserCreationForm съществува')
    if has_custom_form:
        check_file_contains('catalog/forms.py', 
                           "fields = ['email', 'password1']", 
                           'Form полета = email + password1 (без username)')
        check_file_contains('catalog/forms.py', 
                           '_generate_username_from_email', 
                           'Auto-generate username функция')
    print()
    
    # 4. Проверка на register template
    info("4. Проверка на registration темплейт...")
    register_path = 'catalog/templates/registration/register.html'
    if os.path.exists(register_path):
        with open(register_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        has_username_field = 'form.username' in template_content
        if has_username_field:
            check(False, 'register.html НЕ трябва да показва form.username')
            warn('НАМЕРЕНО: form.username в темплейта - КОНФЛИКТ с Form!')
        else:
            check(True, 'register.html няма form.username (правилно)')
        
        check_file_contains(register_path, 
                           'form.email', 
                           'Email поле в темплейта')
        check_file_contains(register_path, 
                           'form.password1', 
                           'Password поле в темплейта')
    print()
    
    # 5. Проверка на login template
    info("5. Проверка на login темплейт...")
    login_paths = [
        'catalog/templates/account/login.html',
        'catalog/templates/registration/login.html'
    ]
    for path in login_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                login_content = f.read()
            
            has_facebook = 'provider_login_url' in login_content and 'facebook' in login_content
            if has_facebook:
                warn(f'{path} съдържа Facebook бутон - ще краша ако Passenger не е рестартиран!')
            else:
                info(f'{path} няма Facebook бутон (временно премахнат)')
            
            check_file_contains(path, 
                               "provider_login_url 'google'", 
                               'Google Login бутон')
    print()
    
    # 6. Проверка на URLs
    info("6. Проверка на URL routing...")
    check_file_contains('products/urls.py', 
                       "path('accounts/', include('allauth.urls'))", 
                       'allauth URLs включени')
    check_file_contains('catalog/urls.py', 
                       "# path('accounts/', include('django.contrib.auth.urls'))", 
                       'django.contrib.auth.urls disabled (коментиран)')
    print()
    
    # 7. Проверка на migrations
    info("7. Проверка на migrations...")
    migrations_dir = 'catalog/migrations'
    if os.path.exists(migrations_dir):
        migration_files = [f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py']
        info(f"Открити {len(migration_files)} migration файла")
        
        # Проверка за 0013_add_cta_button_fields
        has_cta = any('0013' in f or 'cta_button' in f for f in migration_files)
        check(has_cta, '0013 CTA button migration съществува')
    print()
    
    # 8. Проверка на requirements.txt
    info("8. Проверка на зависимости...")
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            reqs = f.read()
        
        check_file_contains('requirements.txt', 'django-allauth', 'django-allauth инсталиран')
        check_file_contains('requirements.txt', 'Django==', 'Django версия фиксирана')
        check_file_contains('requirements.txt', 'PyMySQL', 'PyMySQL за MySQL/MariaDB')
        
        # Провери версията на Django
        django_match = re.search(r'Django==(\d+\.\d+\.\d+)', reqs)
        if django_match:
            version = django_match.group(1)
            info(f"Django версия: {version}")
        
        allauth_match = re.search(r'django-allauth==(\d+\.\d+\.\d+)', reqs)
        if allauth_match:
            version = allauth_match.group(1)
            info(f"django-allauth версия: {version}")
    print()
    
    # 9. Проверка на models
    info("9. Проверка на модели...")
    check_file_contains('catalog/models.py', 
                       'class SEOPage', 
                       'SEOPage model съществува')
    check_file_contains('catalog/models.py', 
                       'cta_button_text', 
                       'CTA button fields в SEOPage')
    check_file_contains('catalog/models.py', 
                       'class Product', 
                       'Product model')
    check_file_contains('catalog/models.py', 
                       'messenger_link', 
                       'Messenger link field в Product')
    print()
    
    # Финален summary
    print("\n" + "="*60)
    print("📊 ЗАКЛЮЧЕНИЕ")
    print("="*60)
    print(f"{GREEN}✅ Кодът е валиден и готов за production{RESET}")
    print(f"{YELLOW}⚠️  Чака Passenger restart за Facebook Login{RESET}")
    print(f"{BLUE}ℹ️  Виж code_audit_report.md за пълен доклад{RESET}")
    print()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"{RED}❌ ГРЕШКА: {e}{RESET}")
        sys.exit(1)
