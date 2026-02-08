#!/usr/bin/env python
"""
Standalone скрипт за изпращане на email напомняния за изтичащи обяви.
Може да се изпълни директно: python send_expiry_emails.py
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


def send_expiry_reminders():
    """Изпраща email напомняния за обяви, които изтичат след 5 дни"""
    
    print("=" * 60)
    print("🚀 Стартиране на email reminder система...")
    print("=" * 60)
    
    # Изчисли дати
    now = timezone.now()
    days_25_ago = now - timedelta(days=25)  # Обяви на 25 дни (остават 5)
    days_26_ago = now - timedelta(days=26)  # За да уловим точно този ден
    
    print(f"📅 Търсене на обяви публикувани между {days_26_ago.strftime('%d.%m.%Y')} и {days_25_ago.strftime('%d.%m.%Y')}")
    
    # Намери обяви които са точно на 25 дни (между 25 и 26 дни)
    expiring_products = Product.objects.filter(
        created_at__lte=days_25_ago,
        created_at__gt=days_26_ago,
        is_active=True,
        owner__isnull=False,
        owner__email__isnull=False
    ).exclude(owner__email='').select_related('owner', 'category', 'city__region')
    
    count = expiring_products.count()
    sent_count = 0
    error_count = 0
    
    print(f"📊 Намерени: {count} обяви за напомняне\n")
    
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
                plain_message = f'''Здравей {product.owner.first_name or product.owner.username},

Напомняме ти, че твоята обява "{product.title}" ще бъде автоматично изтрита след {days_remaining} дни (на {expiry_date.strftime("%d.m.%Y")}).

Ако все още предлагаш този продукт, можеш да редактираш обявата на:
https://bghrana.com/product/edit/{product.pk}/

Редактирането на обявата ще я актуализира и удължи валидността ѝ.

Поздрави,
Екипът на БГ Храна
https://bghrana.com
'''
                
                # Изпрати email
                send_mail(
                    subject=f'⏰ Обявата ти "{product.title[:40]}" изтича след {days_remaining} дни',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[product.owner.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                sent_count += 1
                print(f'✅ Изпратен email до {product.owner.email} за "{product.title}"')
                
            except Exception as e:
                error_count += 1
                print(f'❌ Грешка при изпращане до {product.owner.email}: {str(e)}')
        
        print("\n" + "=" * 60)
        print(f'📧 Резултат: {sent_count}/{count} успешни, {error_count} грешки')
        print("=" * 60)
    else:
        print("ℹ️  Няма обяви, които да изтичат след 5 дни")
        print("=" * 60)


if __name__ == '__main__':
    try:
        send_expiry_reminders()
    except Exception as e:
        print(f"\n❌ КРИТИЧНА ГРЕШКА: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
