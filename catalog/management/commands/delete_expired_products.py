from django.core.management.base import BaseCommand
from django.utils import timezone
from catalog.models import Product


class Command(BaseCommand):
    help = 'Изтрива обяви, които са изтекли преди повече от 180 дни (общо 360+ дни стари)'

    def handle(self, *args, **options):
        # Изчисли дата преди 360 дни (180 дни валидност + 180 дни grace period)
        deletion_date = timezone.now() - timezone.timedelta(days=360)
        
        # Намери всички обяви по-стари от 360 дни
        expired_products = Product.objects.filter(created_at__lt=deletion_date)
        count = expired_products.count()
        
        if count > 0:
            # Изтрий ги
            expired_products.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Успешно изтрити {count} изтекли обяви (по-стари от 360 дни)')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Няма изтекли обяви за изтриване (по-стари от 360 дни)')
            )
