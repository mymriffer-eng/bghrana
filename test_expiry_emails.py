#!/usr/bin/env python
"""
ТЕСТОВ standalone скрипт за изпращане на email напомняния.
Изпраща emails само на посочен тестов email адрес.

Използване: 
    python test_expiry_emails.py your.email@example.com
"""

import os
import sys
import django
from datetime import timedelta

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

# Now import Django models and utilities
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from catalog.models import Product


def test_send_reminders(test_email):
    """ТЕСТ: Изпраща email напомняния само на тестов email адрес"""
    
    print("=" * 60)
    print("🧪 ТЕСТОВ РЕЖИМ - Email Reminders")
    print("=" * 60)
    print(f"📧 Всички emails ще отидат на: {test_email}\n")
    
    # Намери ВСИЧКИ активни обяви с owner (само първите 3 за тест)
    expiring_products = Product.objects.filter(
        is_active=True,
        owner__isnull=False,
    ).select_related('owner', 'category', 'city__region')[:3]
    
    count = expiring_products.count()
    sent_count = 0
    error_count = 0
    
    print(f"📊 Намерени: {count} обяви за тестване\n")
    
    if count > 0:
        for product in expiring_products:
            try:
                # Изчисли точните оставащи дни и дата на изтичане
                days_remaining = product.days_remaining()
                expiry_date = product.created_at + timedelta(days=30)
                
                # Подготви контекста за email template
                context = {
                    'user': product.owner,
                    'product': product,
                    'days_remaining': days_remaining,
                    'expiry_date': expiry_date,
                    'site_url': 'https://bghrana.com',
                }
                
                # Рендирай HTML email
                html_message = render_to_string('catalog/email/product_expiring_soon.html', context)
                
                # Plain text version
                plain_message = f'''🧪 ТОВА Е ТЕСТОВ EMAIL 🧪

Здравей {product.owner.first_name or product.owner.username},

Напомняме ти, че твоята обява "{product.title}" ще бъде автоматично изтрита след {days_remaining} дни (на {expiry_date.strftime("%d.m.%Y")}).

Ако все още предлагаш този продукт, можеш да редактираш обявата на:
https://bghrana.com/product/edit/{product.pk}/

Редактирането на обявата ще я актуализира и удължи валидността ѝ.

Поздрави,
Екипът на БГ Храна
https://bghrana.com
'''
                
                # Изпрати email НА ТЕСТОВИЯ АДРЕС
                send_mail(
                    subject=f'🧪 ТЕСТ ⏰ Обявата ти "{product.title[:40]}" изтича след {days_remaining} дни',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[test_email],  # САМО НА ТЕСТОВИЯ EMAIL
                    html_message=html_message,
                    fail_silently=False,
                )
                
                sent_count += 1
                print(f'✅ Изпратен ТЕСТОВ email за обява "{product.title}"')
                
            except Exception as e:
                error_count += 1
                print(f'❌ Грешка при изпращане: {str(e)}')
        
        print("\n" + "=" * 60)
        print(f'📧 Резултат: {sent_count}/{count} успешни, {error_count} грешки')
        print(f'📬 Провери пощата на: {test_email}')
        print("=" * 60)
    else:
        print("ℹ️  Няма активни обяви за тестване")
        print("=" * 60)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ ГРЕШКА: Моля посочи email адрес за тестване")
        print("\nИзползване:")
        print("    python test_expiry_emails.py your.email@example.com")
        sys.exit(1)
    
    test_email = sys.argv[1]
    
    # Проста валидация на email
    if '@' not in test_email or '.' not in test_email:
        print(f"❌ ГРЕШКА: '{test_email}' не изглежда като валиден email адрес")
        sys.exit(1)
    
    try:
        test_send_reminders(test_email)
    except Exception as e:
        print(f"\n❌ КРИТИЧНА ГРЕШКА: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
