from django.contrib import admin
from .models import Category, Product, Region, City, ProductImage, UserProfile, SEOPage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основна информация', {'fields': ('name', 'slug', 'description')}),
        ('Йерархия', {'fields': ('parent',)}),
        ('SEO Оптимизация', {
            'fields': ('seo_title', 'seo_description', 'seo_text'),
            'classes': ('collapse',),
            'description': 'Персонализирайте SEO за категорийната страница'
        }),
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
        ('SEO Оптимизация', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
            'description': 'Персонализирайте SEO заглавие, описание и ключови думи за по-добро представяне в търсачките'
        }),
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
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'region', 'created_at']
    list_filter = ['region']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SEOPage)
class SEOPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'slug', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основна информация', {
            'fields': ('title', 'slug', 'content', 'is_active')
        }),
        ('SEO Оптимизация', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'description': 'Персонализирайте SEO заглавие, описание и ключови думи за по-добро представяне в търсачките'
        }),
        ('Информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

