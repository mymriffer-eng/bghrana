from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from catalog.models import Product


class Command(BaseCommand):
    help = 'Изпраща email напомняния за обяви, които изтичат след 5 дни'

    def handle(self, *args, **options):
        # Изчисли дати
        now = timezone.now()
        days_25_ago = now - timezone.timedelta(days=25)  # Обяви на 25 дни (остават 5)
        days_26_ago = now - timezone.timedelta(days=26)  # За да уловим точно този ден
        
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
        
        if count > 0:
            self.stdout.write(f'Намерени {count} обяви за напомняне...')
            
            for product in expiring_products:
                try:
                    # Изчисли точните оставащи дни и дата на изтичане
                    days_remaining = product.days_remaining()
                    expiry_date = product.created_at + timezone.timedelta(days=30)
                    
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
                    
                    # Изпрати email
                    send_mail(
                        subject=f'⏰ Обявата ти "{product.title[:40]}" изтича след {days_remaining} дни',
                        message=f'''Здравей {product.owner.first_name or product.owner.username},

Напомняме ти, че твоята обява "{product.title}" ще бъде автоматично изтрита след {days_remaining} дни (на {expiry_date.strftime("%d.m.%Y")}).

Ако все още предлагаш този продукт, можеш да редактираш обявата на:
https://bghrana.com/product/edit/{product.pk}/

Редактирането на обявата ще я актуализира и удължи валидността ѝ.

Поздрави,
Екипът на БГ Храна
https://bghrana.com
''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[product.owner.email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    
                    sent_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Изпратен email до {product.owner.email} за "{product.title}"')
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Грешка при изпращане до {product.owner.email}: {str(e)}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Успешно изпратени {sent_count} от {count} email напомняния')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Няма обяви, които да изтичат след 5 дни')
            )
