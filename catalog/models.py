from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def is_parent(self):
        return self.parent is None


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'region')
        ordering = ['name']

    def __str__(self):
        return self.name


from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.urls import reverse


class Product(models.Model):
    SELLER_TYPE_CHOICES = [
        ('individual', 'Частно лице'),
        ('producer', 'Производител/Фермер'),
        ('company', 'Фирма'),
    ]
    
    SELLS_TO_CHOICES = [
        ('end_customers', 'Крайни клиенти'),
        ('restaurants', 'Ресторанти'),
        ('stores', 'Магазини'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(validators=[MaxLengthValidator(500)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон за връзка')
    babh_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='БАБХ номер')
    seller_type = models.CharField(max_length=20, choices=SELLER_TYPE_CHOICES, blank=True, null=True, verbose_name='Тип продавач')
    sells_to = models.JSONField(default=list, blank=True, verbose_name='Продава на')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.pk})
    
    def get_first_image(self):
        """Връща първата снимка на продукта или None"""
        first_img = self.images.order_by('order').first()
        return first_img.image if first_img else None
    
    def days_remaining(self):
        """Връща броя дни оставащи до изтичане на обявата (30 дни от създаване)"""
        from django.utils import timezone
        expiry_date = self.created_at + timezone.timedelta(days=30)
        remaining = expiry_date - timezone.now()
        return max(0, remaining.days)
    
    def is_expired(self):
        """Проверява дали обявата е изтекла"""
        return self.days_remaining() == 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product_id} ({self.id})"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

