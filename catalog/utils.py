"""
Utility функции за catalog app
"""

from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta


def check_and_send_expiry_reminders():
    """
    Проверява за обяви които изтичат след 5 дни и изпраща email reminders.
    Вика се автоматично при зареждане на главната страница.
    """
    from .models import Product
    
    # Изчисли дати
    now = timezone.now()
    days_175_ago = now - timedelta(days=175)  # Обяви на 175 дни (остават 5)
    days_176_ago = now - timedelta(days=176)  # За да уловим точно този ден
    
    # Намери обяви които са точно на 175 дни И все още НЕ СА получили reminder
    expiring_products = Product.objects.filter(
        created_at__lte=days_175_ago,
        created_at__gt=days_176_ago,
        is_active=True,
        expiry_reminder_sent=False,  # Само тези които още не са получили email
        owner__isnull=False,
        owner__email__isnull=False
    ).exclude(owner__email='').select_related('owner', 'category', 'city__region')
    
    sent_count = 0
    
    for product in expiring_products:
        try:
            # Изчисли точните оставащи дни и дата на изтичане
            days_remaining = product.days_remaining()
            expiry_date = product.created_at + timedelta(days=180)
            
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
                fail_silently=True,  # Не спира сайта ако email service е down
            )
            
            # Маркирай че email-ът е изпратен
            product.expiry_reminder_sent = True
            product.save(update_fields=['expiry_reminder_sent'])
            
            sent_count += 1
            
        except Exception as e:
            # Log error но не спирай процеса
            print(f'Error sending expiry reminder for product {product.id}: {str(e)}')
            continue
    
    return sent_count
