from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL slug', help_text='Пример: mlechni-produkti, meso-i-kolebasi')
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    
    # SEO Fields
    seo_title = models.CharField(max_length=60, blank=True, verbose_name='SEO Заглавие', help_text='Оптимално: до 60 символа')
    seo_description = models.TextField(max_length=160, blank=True, verbose_name='SEO Описание', help_text='Оптимално: до 160 символа')
    seo_text = models.TextField(blank=True, verbose_name='SEO Текст', help_text='Описание на категорията 300-500 думи за по-добро SEO')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def is_parent(self):
        return self.parent is None
    
    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL slug', help_text='Пример: sofia, plovdiv, varna')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:region_detail', kwargs={'slug': self.slug})


class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True, verbose_name='URL slug', help_text='Пример: sofia, plovdiv, varna')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'region')
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:city_detail', kwargs={'region_slug': self.region.slug, 'slug': self.slug})


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
    expiry_reminder_sent = models.BooleanField(default=False, verbose_name='Email напомняне изпратено')
    
    # SEO Fields
    meta_title = models.CharField(max_length=60, blank=True, null=True, verbose_name='SEO Заглавие', help_text='Оптимално: до 60 символа')
    meta_description = models.TextField(max_length=160, blank=True, null=True, verbose_name='SEO Описание', help_text='Оптимално: до 160 символа')
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name='SEO Ключови думи', help_text='Разделени със запетая')

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
    
    def is_new(self):
        """Проверява дали обявата е нова (публикувана в последните 48 часа)"""
        from django.utils import timezone
        age = timezone.now() - self.created_at
        return age.total_seconds() < (48 * 60 * 60)  # 48 часа в секунди


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


class SEOPage(models.Model):
    """Модел за статични SEO страници, редактируеми от админ панела"""
    title = models.CharField(max_length=200, verbose_name='Заглавие')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL slug', help_text='Пример: za-nas, kontakti, obshti-usloviya')
    content = models.TextField(verbose_name='Съдържание', help_text='Може да използвате HTML форматиране')
    meta_title = models.CharField(max_length=60, blank=True, verbose_name='SEO Заглавие', help_text='Оптимално: до 60 символа')
    meta_description = models.TextField(max_length=160, blank=True, verbose_name='SEO Описание', help_text='Оптимално: до 160 символа')
    meta_keywords = models.CharField(max_length=255, blank=True, verbose_name='SEO Ключови думи', help_text='Разделени със запетая')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'SEO Страница'
        verbose_name_plural = 'SEO Страници'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:seo_page', kwargs={'slug': self.slug})

