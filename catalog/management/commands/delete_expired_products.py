from django.core.management.base import BaseCommand
from django.utils import timezone
from catalog.models import Product


class Command(BaseCommand):
    help = 'Изтрива обяви, които са по-стари от 30 дни'

    def handle(self, *args, **options):
        # Изчисли дата преди 30 дни
        expiry_date = timezone.now() - timezone.timedelta(days=30)
        
        # Намери всички обяви по-стари от 30 дни
        expired_products = Product.objects.filter(created_at__lt=expiry_date)
        count = expired_products.count()
        
        if count > 0:
            # Изтрий ги
            expired_products.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Успешно изтрити {count} изтекли обяви')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Няма изтекли обяви за изтриване')
            )
