from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from catalog.models import Product


class Command(BaseCommand):
    help = 'ТЕСТ: Изпраща email напомняния за ВСИЧКИ активни обяви (за тестване)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email адрес за тестване (вместо реалния owner email)',
        )

    def handle(self, *args, **options):
        test_email = options.get('email')
        
        # Намери ВСИЧКИ активни обяви с owner
        expiring_products = Product.objects.filter(
            is_active=True,
            owner__isnull=False,
        ).select_related('owner', 'category', 'city__region')[:3]  # Само първите 3 за тест
        
        count = expiring_products.count()
        sent_count = 0
        
        if count > 0:
            self.stdout.write(f'🧪 ТЕСТОВ РЕЖИМ: Намерени {count} обяви за тестване...')
            
            for product in expiring_products:
                try:
                    # Изчисли точните оставащи дни и дата на изтичане
                    days_remaining = product.days_remaining()
                    expiry_date = product.created_at + timezone.timedelta(days=30)
                    
                    # Използвай тестов email ако е зададен
                    recipient_email = test_email if test_email else product.owner.email
                    
                    if not recipient_email:
                        self.stdout.write(self.style.WARNING(f'⚠️  Пропускам "{product.title}" - няма email'))
                        continue
                    
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
                        subject=f'🧪 ТЕСТ ⏰ Обявата ти "{product.title[:40]}" изтича след {days_remaining} дни',
                        message=f'''🧪 ТОВА Е ТЕСТОВ EMAIL 🧪

Здравей {product.owner.first_name or product.owner.username},

Напомняме ти, че твоята обява "{product.title}" ще бъде автоматично изтрита след {days_remaining} дни (на {expiry_date.strftime("%d.m.%Y")}).

Ако все още предлагаш този продукт, можеш да редактираш обявата на:
https://bghrana.com/product/edit/{product.pk}/

Редактирането на обявата ще я актуализира и удължи валидността ѝ.

Поздрави,
Екипът на БГ Храна
https://bghrana.com
''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient_email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    
                    sent_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Изпратен ТЕСТОВ email до {recipient_email} за "{product.title}"')
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Грешка при изпращане до {recipient_email}: {str(e)}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Успешно изпратени {sent_count} от {count} ТЕСТОВИ email напомняния')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Няма активни обяви за тестване')
            )
