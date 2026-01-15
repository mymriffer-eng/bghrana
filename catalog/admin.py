from django.contrib import admin
from .models import Category, Product, Region, City, ProductImage, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name']
    fieldsets = (
        ('Основна информация', {'fields': ('name', 'description')}),
        ('Йерархия', {'fields': ('parent',)}),
    )

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'city', 'owner', 'price', 'seller_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'city', 'seller_type', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основна информация', {'fields': ('title', 'description', 'price', 'category', 'city', 'owner')}),
        ('Контакти и информация', {'fields': ('phone', 'babh_number')}),
        ('Тип продавач и клиенти', {'fields': ('seller_type', 'sells_to')}),
        ('Статус', {'fields': ('is_active',)}),
    )
    inlines = [ProductImageInline]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5

admin.site.register(ProductImage)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'created_at']
    list_filter = ['region']
    search_fields = ['name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

