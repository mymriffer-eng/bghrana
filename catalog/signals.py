from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from .models import Product, ProductImage
import os


@receiver(pre_delete, sender=ProductImage)
def delete_image_file(sender, instance, **kwargs):
    """Изтрива физическия файл на снимката при изтриване на ProductImage обект"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_delete, sender=Product)
def delete_product_images(sender, instance, **kwargs):
    """Изтрива всички снимки на продукта при изтриване на Product обект"""
    for image in instance.images.all():
        if image.image:
            if os.path.isfile(image.image.path):
                os.remove(image.image.path)
