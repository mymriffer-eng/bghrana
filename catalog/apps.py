from django.apps import AppConfig


class CatalogConfig(AppConfig):
    name = 'catalog'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import catalog.signals  # Импорт на signals за автоматично изтриване на снимки
